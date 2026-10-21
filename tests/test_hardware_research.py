"""Research bookkeeping is not physical verification or expanded CLI support."""
import copy
import json
from pathlib import Path
import unittest

from hardware.research.validation import validate_catalog

ROOT = Path(__file__).resolve().parent.parent


class HardwareResearchTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'hardware/research/catalog.json').read_text())

    def test_catalog_structure_and_explicit_external_evidence_boundary(self):
        result = validate_catalog(self.data, ROOT)
        self.assertGreaterEqual(result['sources'], 10)
        self.assertGreaterEqual(result['claims'], 20)
        # This pass deliberately adds no local verification or executable profiles.
        self.assertEqual(result['verified_here'], 0)
        registry = json.loads((ROOT / 'hardware/registry.json').read_text())
        self.assertEqual(registry['research_catalog'], 'research/catalog.json')
        self.assertEqual({b['recovery_profile'] for b in registry['boards']}, {'mir63a0-revp21'})

    def test_bad_references_duplicates_and_paths_are_rejected(self):
        mutations = [
            lambda d: d['claims'][0].update(sources=['missing']),
            lambda d: d['claims'][0].update(subject='missing'),
            lambda d: d['claims'][0].update(related_entities=['missing']),
            lambda d: d['sources'].append(copy.deepcopy(d['sources'][0])),
            lambda d: d['entities'][0].update(record='../../../../outside.md'),
            lambda d: d['entities'][0].update(recovery_profile='imaginary-profile'),
            lambda d: d['claims'][0].update(limits=''),
        ]
        for mutate in mutations:
            data = copy.deepcopy(self.data)
            mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                validate_catalog(data, ROOT)

    def test_external_claim_cannot_be_promoted_by_changing_its_label(self):
        claim = self.data['claims'][0]
        claim['validation'] = 'verified-here'
        with self.assertRaisesRegex(ValueError, 'External research'):
            validate_catalog(self.data, ROOT)
        claim['basis'] = 'project-observation'
        with self.assertRaisesRegex(ValueError, 'evidence record'):
            validate_catalog(self.data, ROOT)

    def test_unread_regulatory_photos_do_not_become_a_chip_claim(self):
        claim = self.data['claims'][0]
        claim.update(sources=['fcc-2018'], basis='external-primary-report')
        with self.assertRaisesRegex(ValueError, 'Unread exhibit'):
            validate_catalog(self.data, ROOT)

    def test_inference_and_disagreement_need_explicit_explanation(self):
        claim = self.data['claims'][0]
        claim['basis'] = 'inference'
        with self.assertRaisesRegex(ValueError, 'reasoning'):
            validate_catalog(self.data, ROOT)
        claim['reasoning'] = 'Fixture hypothesis only; no hardware conclusion.'
        claim['validation'] = 'disputed'
        with self.assertRaisesRegex(ValueError, 'conflict'):
            validate_catalog(self.data, ROOT)
        claim['conflict'] = 'Fixture conflicting observations; not a real disputed claim.'
        self.assertEqual(validate_catalog(self.data, ROOT)['verified_here'], 0)
