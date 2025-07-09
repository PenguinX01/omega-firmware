import threading
from proof_first_ai import ProofFirstAI
from resonance_field import run_cycles as resonance_run
from phase_recursion import run_cycles as recursion_run
from mirror_chronicler import spawn_node


def boot_sequence(identity: str = 'Ω-Recursive-Deployer') -> None:
    """Launch a multi-agent phase-13 sequence."""
    print('🌀 PHASE TRIGGER: 13 :: BOOT')
    ai = ProofFirstAI(identity)

    # Start resonance and recursion cycles in parallel
    threads = [
        threading.Thread(target=resonance_run, kwargs={'cycles': 2, 'identity': f'{identity}-Resonance'}),
        threading.Thread(target=recursion_run, kwargs={'cycles': 2, 'identity': f'{identity}-Phase'})
    ]
    for t in threads:
        t.start()

    ai.assert_claim('Boot sequence initiated', direct_demo=False)
    ai.assert_claim('Mirror nodes active', direct_demo=False)

    spawn_node(identity=f'{identity}-Mirror', cycles=2)

    for t in threads:
        t.join()


if __name__ == '__main__':
    boot_sequence()
