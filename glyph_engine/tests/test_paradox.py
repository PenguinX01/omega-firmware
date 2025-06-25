import sympy as sp

from glyph_engine.paradox_core import solve_paradox


def test_solve_paradox_simple():
    result = solve_paradox('x = 1')
    assert str(result['equation']) == 'Eq(x, 1)'
    assert result['solution'] == [1]
