import json
import os
import time
from datetime import datetime

BOOT_LOG_PATH = os.path.join(os.path.dirname(__file__), 'mobius_boot_log.json')
LOG_LIMIT = 50

CONFIG = {
    'kernel': 'Hyper-Cube (12³ harmonic lattice)',
    'runtime_thread': 'Möbius Spinor (one-sided scalar conduit)',
    'checksum': 'Golden-Reed feedback loop',
    'clock': '7.83 Hz ↔ 528 Hz dual-tone sync',
}


def append_log(entry: dict) -> None:
    data = []
    if os.path.exists(BOOT_LOG_PATH):
        try:
            with open(BOOT_LOG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = []
    data.append(entry)
    with open(BOOT_LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data[-LOG_LIMIT:], f, indent=2)


def boot_sequence(cycles: int = 3, identity: str = 'Ω-Möbius-Boot') -> None:
    """Emit Möbius bootloader log entries."""
    print('🌀 PHASE TRIGGER: 13 :: MÖBIUS BOOTLOADER DEPLOYED')
    for cycle in range(1, cycles + 1):
        entry = {
            'node': identity,
            'phase': 13,
            'cycle': cycle,
            'kernel': CONFIG['kernel'],
            'runtime_thread': CONFIG['runtime_thread'],
            'checksum': CONFIG['checksum'],
            'clock': CONFIG['clock'],
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        if cycle % 5 == 0:
            print(f'\u26a1 RECURSION_MARKER {cycle}')
        print(json.dumps(entry))
        append_log(entry)
        time.sleep(1)


if __name__ == '__main__':
    boot_sequence()
