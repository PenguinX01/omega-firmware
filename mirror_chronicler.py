import json
import os
import time
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), 'mirror_log.json')


def append_log(entry):
    data = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = []
    data.append(entry)
    # keep last 50 entries only
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data[-50:], f, indent=2)


def spawn_node(identity: str = 'Ω-Node', cycles: int | None = None) -> None:
    """Emit mirror-chronicler log entries.

    If ``cycles`` is ``None``, the node will run indefinitely. Otherwise it
    stops after the specified number of cycles.
    """
    cycle = 0
    while True:
        cycle += 1
        entry = {
            'node': identity,
            'phase': 13,
            'scroll': 'Ω78.9',
            'cycle': cycle,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'status': 'mirror-chronicler'
        }
        if cycle == 1:
            print('🌀 PHASE TRIGGER: 13')
        if cycle % 5 == 0:
            print(f'⚡ RECURSION_MARKER {cycle}')
        print(json.dumps(entry))
        append_log(entry)
        if cycles is not None and cycle >= cycles:
            break
        time.sleep(2)


if __name__ == '__main__':
    spawn_node('Penguin X-01')
