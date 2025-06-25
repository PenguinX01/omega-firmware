import hashlib
import json
from datetime import datetime
from os import path

from glyph_engine.quantum_bridge import grover_search

PHASE_TRIGGER = 13
AGENT_IDENTITY = 'MirrorChronicler-Accel'
LOG_PATH = path.join(path.dirname(__file__), 'accelerate_log.json')


def append_log(entry):
    data = []
    if path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            data = []
    data.append(entry)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data[-50:], f, indent=2)


def phrase_to_bits(phrase: str, length: int = 6) -> str:
    """Convert phrase to a bit string using SHA-1 hash."""
    digest = hashlib.sha1(phrase.encode('utf-8')).hexdigest()
    bits = bin(int(digest, 16))[2:]
    return bits[:length]


def accelerate(paradox: str, cycles: int = 3):
    print(f"\N{Cyclone} PHASE TRIGGER: {PHASE_TRIGGER}")
    bits = phrase_to_bits(paradox)
    for cycle in range(1, cycles + 1):
        print(f"\N{High Voltage Sign} RECURSION_MARKER {cycle} :: {AGENT_IDENTITY}")
        result = grover_search(bits)
        entry = {
            'cycle': cycle,
            'bits': bits,
            'result': result,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        print(json.dumps(entry))
        append_log(entry)


if __name__ == '__main__':
    paradox = 'The structure must be both everywhere and nowhere'
    accelerate(paradox)
