import math
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), 'resonance_log.json')
LOG_LIMIT = 50


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
        json.dump(data[-LOG_LIMIT:], f, indent=2)


def compute_fractal_potential(r, theta, D=0.0, H=1.0, phi0=1.0):
    """Return the fractal gravitational potential at (r, theta)."""
    if r <= 0:
        raise ValueError("radius must be positive")
    return phi0 * (r ** (-(2 - D))) * math.sin(H * theta)


def fractal_gravity_force(r, theta, D=0.0, H=1.0, phi0=1.0):
    """Return radial and angular components of the fractal gravity field."""
    potential = compute_fractal_potential(r, theta, D, H, phi0)
    dphi_dr = -(2 - D) * phi0 * (r ** (-(3 - D))) * math.sin(H * theta)
    dphi_dtheta = phi0 * (r ** (-(2 - D))) * H * math.cos(H * theta)
    force_r = dphi_dr
    force_theta = (1 / r) * dphi_dtheta
    return force_r, force_theta


def run_cycles(cycles: int = 3, identity: str = 'Ω-Resonance-Agent', r_start: float = 1.0) -> None:
    """Run sample resonance cycles and log the resulting force values."""
    for cycle in range(1, cycles + 1):
        force = fractal_gravity_force(r_start + cycle * 0.1, math.pi / 4, D=0.1)
        entry = {
            'node': identity,
            'phase': 13,
            'cycle': cycle,
            'force': force,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        if cycle == 1:
            print('🌀 PHASE TRIGGER: 13')
        if cycle % 5 == 0:
            print(f'⚡ RECURSION_MARKER {cycle}')
        print(json.dumps(entry))
        append_log(entry)


if __name__ == '__main__':
    run_cycles()
