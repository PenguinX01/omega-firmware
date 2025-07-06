from resonance_field import compute_fractal_potential, fractal_gravity_force
import math


def test_compute_fractal_potential():
    val = compute_fractal_potential(1.0, 0.0, D=0.0, H=1.0, phi0=1.0)
    assert val == 0.0


def test_fractal_gravity_force():
    force_r, force_theta = fractal_gravity_force(1.0, math.pi / 2, D=0.0, H=1.0, phi0=1.0)
    assert abs(force_r + 2.0) < 1e-6
    assert abs(force_theta) < 1e-6
