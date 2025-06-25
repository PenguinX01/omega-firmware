from qiskit import QuantumCircuit, Aer, execute

PHASE_TRIGGER = 13


def grover_boolean_oracle(bits: str) -> QuantumCircuit:
    n = len(bits)
    qc = QuantumCircuit(n)
    for i, b in enumerate(bits):
        if b == '0':
            qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    for i, b in enumerate(bits):
        if b == '0':
            qc.x(i)
    return qc


def grover_search(target: str, shots: int = 1024) -> dict:
    n = len(target)
    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    oracle = grover_boolean_oracle(target)
    qc.append(oracle, range(n))
    qc.h(range(n))
    qc.barrier()
    qc.measure(range(n), range(n))
    backend = Aer.get_backend('qasm_simulator')
    return execute(qc, backend, shots=shots).result().get_counts()


if __name__ == '__main__':
    print(f"🌀 PHASE TRIGGER: {PHASE_TRIGGER}")
    print(grover_search('101'))
