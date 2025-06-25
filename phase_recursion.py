import hashlib
import json
import os
import time
from datetime import datetime

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), 'phase13-manifesto.txt')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'phase_recursion_log.json')


def compute_manifest_hash():
    try:
        with open(MANIFEST_PATH, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def append_log(entry):
    data = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = []
    data.append(entry)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data[-50:], f, indent=2)


def run_cycles(cycles=3, identity='Ω-Recursive-Agent'):
    manifest_hash = compute_manifest_hash()
    for cycle in range(1, cycles + 1):
        entry = {
            'node': identity,
            'phase': 13,
            'cycle': cycle,
            'manifest_hash': manifest_hash,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        if cycle == 1:
            print('🌀 PHASE TRIGGER: 13')
        print(f'⚡ RECURSION_MARKER {cycle}')
        print(json.dumps(entry))
        append_log(entry)
        time.sleep(1)


if __name__ == '__main__':
    run_cycles()
