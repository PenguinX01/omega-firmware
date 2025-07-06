from epsilon_calculations import EpsilonCalculations

def test_muonic_hydrogen_calculation():
    calc = EpsilonCalculations(identity='test-epsilon')
    epsilon = calc.muonic_hydrogen_calculation()
    assert isinstance(epsilon, float)
