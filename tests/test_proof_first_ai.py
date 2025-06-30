from proof_first_ai import ProofFirstAI


def test_assert_claim_unproven():
    ai = ProofFirstAI(identity='test-node')
    claim = ai.assert_claim('Unproven claim', direct_demo=False)
    assert claim.status == 'UNPROVEN'
    assert claim.count == 1
