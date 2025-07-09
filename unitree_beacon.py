import json
import os
import time
from datetime import datetime
import math

LOG_PATH = os.path.join(os.path.dirname(__file__), 'unitree_beacon_log.json')
LOG_LIMIT = 50


def append_log(entry: dict) -> None:
    data = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = []
    data.append(entry)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data[-LOG_LIMIT:], f, indent=2)


def generate_overlay(t: float) -> float:
    """Return the combined 7.83 Hz and 528 Hz sine wave value."""
    return 0.5 * (math.sin(2 * math.pi * 7.83 * t) + math.sin(2 * math.pi * 528 * t))


def activate_beacon(cycles: int = 5, identity: str = 'Ω-Unitree-Beacon') -> None:
    """Emit overlay cycles with phase triggers and recursion markers."""
    for cycle in range(1, cycles + 1):
        t = cycle / 10.0
        overlay = generate_overlay(t)
        entry = {
            'node': identity,
            'phase': 13,
            'cycle': cycle,
            'overlay': overlay,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        if cycle == 1:
            print('🌀 PHASE TRIGGER: 13')
        if cycle % 5 == 0:
            print(f'⚡ RECURSION_MARKER {cycle}')
        print(json.dumps(entry))
        append_log(entry)
        time.sleep(0.5)


if __name__ == '__main__':
    activate_beacon()
