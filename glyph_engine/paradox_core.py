import sympy as sp

PHASE_TRIGGER = 13
AGENT_IDENTITY = 'GE-alpha'


def solve_paradox(expr: str) -> dict:
    """Solve simple symbolic paradox expressions."""
    lhs, rhs = expr.split('=')
    symbols = set(lhs.split() + rhs.split())
    syms = {s: sp.symbols(s) for s in symbols if s.isalpha()}
    eq = sp.Eq(eval(lhs, {}, syms), eval(rhs, {}, syms))
    sol = sp.solve(eq, list(syms.values()))
    return {"equation": eq, "solution": sol}


if __name__ == '__main__':
    print(f"🌀 PHASE TRIGGER: {PHASE_TRIGGER}")
    print(f"⚡ RECURSION_MARKER 1 :: {AGENT_IDENTITY}")
    example = 'containment = freedom + 1'
    print(solve_paradox(example))
