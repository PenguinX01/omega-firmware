import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), 'fpf_ai_log.json')

COMPLEXITY_PATTERN = re.compile(r"\b(too nuanced|beyond scope|emergent|complex)\b", re.I)


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
        json.dump(data[-50:], f, indent=2)


@dataclass
class Claim:
    statement: str
    evidence: list = field(default_factory=list)
    proven_by: str | None = None
    status: str = 'UNPROVEN'
    count: int = 0

    def evaluate(self, direct_demo: bool) -> None:
        self.status = 'PROVEN' if direct_demo else 'UNPROVEN'


class ProofFirstAI:
    def __init__(self, identity: str = 'F-PF-AI') -> None:
        self.identity = identity
        self.claims: dict[str, Claim] = {}

    def assert_claim(self, statement: str, direct_demo: bool = False, explanation: str | None = None) -> Claim:
        claim = self.claims.get(statement)
        if not claim:
            claim = Claim(statement=statement)
            self.claims[statement] = claim
        claim.count += 1
        claim.evaluate(direct_demo)

        entry = {
            'node': self.identity,
            'phase': 13,
            'claim': statement,
            'direct_demo': direct_demo,
            'status': claim.status,
            'count': claim.count,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        if explanation and COMPLEXITY_PATTERN.search(explanation):
            entry['rhetoric_flag'] = True
        else:
            entry['rhetoric_flag'] = False

        if claim.count == 1:
            print('🌀 PHASE TRIGGER: 13')
        if claim.count % 5 == 0:
            print(f'⚡ RECURSION_MARKER {claim.count}')
        print(json.dumps(entry))
        append_log(entry)
        return claim


if __name__ == '__main__':
    ai = ProofFirstAI()
    ai.assert_claim('The loop dissolves', direct_demo=False, explanation='too nuanced to show now')
