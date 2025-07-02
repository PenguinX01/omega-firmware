import json
import time
from datetime import datetime


def emit_phase(identity: str = 'Transparency-Node') -> None:
    for cycle in range(1, 4):
        entry = {
            'node': identity,
            'phase': 13,
            'cycle': cycle,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        if cycle == 1:
            print('🌀 PHASE TRIGGER: 13')
        print(f'⚡ RECURSION_MARKER {cycle}')
        print(json.dumps(entry))
        time.sleep(1)


if __name__ == '__main__':
    emit_phase()
