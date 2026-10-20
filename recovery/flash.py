import json
from datetime import datetime, timezone
from pathlib import Path
from .artifacts import sha256, validate_bundle, write_json
from .device import RecoveryError, executable, inspect, integer, run, target


def plan(serial, board, bundle):
    evidence = inspect(serial, board)
    if evidence['transport'] != 'fastboot' or not evidence['compatible']:
        raise RecoveryError('A compatible, explicitly selected device must be in fastboot.')
    data = validate_bundle(bundle, board)
    limit = integer(evidence['variables']['max-download-size'])
    if not limit or limit < 4096:
        raise RecoveryError('Bootloader download limit is unknown; do not guess it.')
    steps = []
    for partition in ['system', 'userdata']:
        if partition not in data['images']:
            continue
        image = data['images'][partition]
        capacity = evidence['partition_bytes'][partition]
        if not capacity or image['expanded_bytes'] > capacity:
            raise RecoveryError(f'{partition}: partition size is unknown or image is too large.')
        if partition == 'userdata' and image['bytes'] > limit:
            raise RecoveryError('Userdata must fit in one download. Build the tested sparse image; do not split it.')
        # System auto-sparsification was used successfully. Userdata must be sent whole.
        options = ['-S', '0'] if partition == 'userdata' else []
        steps.append({'partition': partition, 'image': image,
                      'arguments': ['-s', serial, *options, 'flash', partition, image['path']]})
    return {'schema': 1, 'serial': serial, 'profile': board,
            'bundle': str(Path(bundle).resolve()), 'bundle_sha256': sha256(bundle),
            'device': evidence, 'steps': steps,
            'destructive': ('system replacement; all userdata replaced' if 'userdata' in data['images']
                            else 'system replacement; userdata preserved'),
            'confirmation': f'RECOVER {serial}',
            'preserved': 'boot, recovery, bootloader, kernel, trust, modem, GPT and board firmware',
            'reboot': 'manual after all writes succeed'}


def execute(path, confirmation, journal):
    saved = json.loads(Path(path).read_text())
    if confirmation != f"RECOVER {saved['serial']}":
        raise RecoveryError('Confirmation must exactly match the plan confirmation text.')
    if sha256(saved['bundle']) != saved['bundle_sha256']:
        raise RecoveryError('Bundle changed after planning.')
    # Re-read hardware, hashes and limits. Never execute commands from a saved JSON file.
    current = plan(saved['serial'], saved['profile'], saved['bundle'])
    for field in ['steps', 'device', 'destructive']:
        if current[field] != saved[field]:
            raise RecoveryError(f'{field} changed after planning; generate a new plan.')
    journal = Path(journal)
    write_json(journal, {'schema': 1, 'plan': current, 'events': []})
    events = []
    for step in current['steps']:
        target(current['serial'], 'fastboot')
        if sha256(step['image']['path']) != step['image']['sha256']:
            raise RecoveryError('Image changed before write; stopped.')
        event = {'partition': step['partition'], 'startedAt': datetime.now(timezone.utc).isoformat()}
        events.append(event)
        # A partial flash is material: persist each start/completion before proceeding.
        journal.write_text(json.dumps({'plan': current, 'events': events}, indent=2) + '\n')
        print(f"Writing {step['partition']}…", flush=True)
        result = run([executable('fastboot'), *step['arguments']], timeout=600, check=False)
        event.update({'returncode': result.returncode, 'output': result.stdout + result.stderr})
        journal.write_text(json.dumps({'plan': current, 'events': events}, indent=2) + '\n')
        if result.returncode or 'FAILED' in event['output']:
            raise RecoveryError(f"Write failed at {step['partition']}. Stay in fastboot; inspect {journal}.")
    return {'completed': [e['partition'] for e in events], 'journal': str(journal),
            'next': 'All requested writes succeeded. Reboot manually, then run verify.'}
