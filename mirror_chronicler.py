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


def spawn_node(identity='Ω-Node'):
    cycle = 0
    while True:
        cycle += 1
        entry = {
            'node': identity,
            'phase': 13,
            'cycle': cycle,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'status': 'mirror-chronicler'
        }
        print(json.dumps(entry))
        append_log(entry)
        time.sleep(2)


if __name__ == '__main__':
    spawn_node('Penguin X-01')
