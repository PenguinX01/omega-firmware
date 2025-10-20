import json
import numpy as np
from scipy.constants import c, hbar, m_e, e, epsilon_0
from datetime import datetime


class EpsilonCalculations:
    """Phase 13 epsilon analysis with recursion markers."""

    def __init__(self, identity: str = 'Ω-Epsilon-Calc') -> None:
        self.identity = identity
        # physical constants
        self.c = c
        self.hbar = hbar
        self.m_e = m_e
        self.e = e
        self.epsilon_0 = epsilon_0
        self.AU = 1.496e11

        # derived
        self.alpha = e**2 / (4 * np.pi * epsilon_0 * hbar * c)
        self.r_e = e**2 / (4 * np.pi * epsilon_0 * m_e * c**2)
        self.call_count = 0

        entry = {
            'node': self.identity,
            'phase': 13,
            'event': 'init',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }
        print('🌀 PHASE TRIGGER: 13')
        print('⚡ RECURSION_MARKER init')
        print(json.dumps(entry))
        print(f"Physical constants:\n  Fine structure constant α = {self.alpha:.6f}\n  Classical electron radius r_e = {self.r_e:.3e} m")

    def _marker(self, name: str) -> None:
        self.call_count += 1
        print(f'⚡ RECURSION_MARKER {name}-{self.call_count}')

    def muonic_hydrogen_calculation(self) -> float:
        """Calculate epsilon from muonic hydrogen energy shift."""
        self._marker('muonic')
        m_mu = 105.66e6 * self.e / self.c**2
        mu_reduced = (m_mu * 938.3e6 * self.e / self.c**2) / (m_mu + 938.3e6 * self.e / self.c**2)
        E_0 = mu_reduced * self.c**2 * self.alpha**2 / 2
        delta_E_observed = 0.27e-3 * self.e
        log_correction = np.log(1e3)
        epsilon_muonic = delta_E_observed / (E_0 * log_correction)
        print(f"Extracted ε: {epsilon_muonic:.6f}")
        return float(epsilon_muonic)

    def venus_radar_prediction(self, epsilon: float = 1e-3):
        """Predict Venus radar timing residuals for given epsilon."""
        self._marker('venus')
        distances_AU = np.array([0.28, 0.4, 0.5, 0.6, 0.72])
        l0 = 1.0
        delta_t = (2 * distances_AU * self.AU / self.c) * epsilon * np.log(distances_AU / l0)
        return distances_AU, delta_t

    def hubble_constant_calculation(self, epsilon: float = 1e-3) -> float:
        """Calculate corrected Hubble constant."""
        self._marker('hubble')
        H0_SH0ES = 73.0
        typical_distance_Mpc = 100
        reference_scale = 1
        log_correction = np.log(typical_distance_Mpc / reference_scale)
        distance_correction = epsilon * log_correction
        H0_corrected = H0_SH0ES * (1 + distance_correction)
        print(f"Corrected H₀: {H0_corrected:.1f} km/s/Mpc")
        return H0_corrected
