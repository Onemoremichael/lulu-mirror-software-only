"""Catalog integrity checks only: no network, device, or truth attestation."""
from datetime import date
from pathlib import Path
import re
from urllib.parse import urlparse


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_index(items, name):
    result = {}
    require(isinstance(items, list) and items, name + ' must be a nonempty list')
    for item in items:
        identifier = item.get('id', '')
        require(bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', identifier)), 'Invalid ' + name + ' ID')
        require(identifier not in result, 'Duplicate ' + name + ' ID: ' + identifier)
        result[identifier] = item
    return result


def local_record(root, relative):
    require(isinstance(relative, str) and bool(relative), 'Missing local evidence record')
    require(not Path(relative).is_absolute(), 'Evidence paths must be repository-relative')
    target = (root / relative).resolve()
    require(target.is_relative_to(root.resolve()) and target.is_file(), 'Missing/outside record: ' + relative)


def validate_catalog(data, root):
    root = Path(root)
    require(data.get('schema') == 1, 'Unsupported research catalog schema')
    date.fromisoformat(data['reviewed_on'])
    sources = unique_index(data['sources'], 'source')
    entities = unique_index(data['entities'], 'entity')
    claims = unique_index(data['claims'], 'claim')
    source_types = {'maintainer-report', 'first-person-report', 'manufacturer-document',
                    'regulatory-index', 'project-record'}
    access_types = {'full-text', 'indexed-thread-excerpts', 'partial-text',
                    'metadata-only', 'selected-sections'}
    for source in sources.values():
        parsed = urlparse(source['url'])
        require(parsed.scheme == 'https' and bool(parsed.netloc), 'Source URL must be HTTPS')
        require(source.get('type') in source_types, 'Unknown source type')
        require(source.get('access') in access_types, 'Unknown source access extent')
        require(bool(source.get('title')) and bool(source.get('origin_group')), 'Source attribution required')
    kinds = {'compute-family', 'reported-unit', 'firmware', 'board-lead', 'panel',
             'reference-platform', 'regulatory-model', 'excluded-lookalike'}
    for entity in entities.values():
        require(entity.get('kind') in kinds and bool(entity.get('name')), 'Invalid entity kind/name')
        require('recovery_profile' not in entity, 'Research entities cannot grant recovery profiles')
        local_record(root, 'hardware/research/' + entity['record'])
    states = {'researched', 'verified-here', 'disputed'}
    bases = {'external-primary-report', 'manufacturer-document', 'regulatory-metadata',
             'project-observation', 'inference'}
    for claim in claims.values():
        require(claim.get('subject') in entities, 'Unknown claim subject')
        require(claim.get('basis') in bases and claim.get('validation') in states, 'Invalid claim evidence state')
        for field in ('attribute', 'value', 'locator', 'limits', 'validation_needed'):
            require(isinstance(claim.get(field), str) and bool(claim[field].strip()), 'Missing claim ' + field)
        require(isinstance(claim.get('sources'), list) and bool(claim['sources']), 'Claim needs sources')
        for identifier in claim['sources']:
            require(identifier in sources, 'Unknown claim source')
            if sources[identifier]['access'] == 'metadata-only':
                require(claim['basis'] == 'regulatory-metadata', 'Unread exhibit cannot support a component claim')
        for identifier in claim.get('related_entities', []):
            require(identifier in entities, 'Unknown related entity')
        if claim['basis'] == 'inference':
            require(bool(claim.get('reasoning')), 'Inference needs explicit reasoning')
        if claim['validation'] == 'disputed':
            require(bool(claim.get('conflict')), 'Disputed claim needs conflict explanation')
        if claim['validation'] == 'verified-here':
            require(claim['basis'] == 'project-observation', 'External research is not local verification')
            verification = claim.get('verification', {})
            local_record(root, verification.get('record'))
            date.fromisoformat(verification['observed_on'])
            require(bool(verification.get('scope')), 'Local verification needs scope')
    return {'sources': len(sources), 'entities': len(entities), 'claims': len(claims),
            'verified_here': sum(c['validation'] == 'verified-here' for c in claims.values()),
            'note': 'Structural validation only; no hardware truth, recovery support or write authorization inferred.'}
