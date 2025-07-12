from mobius_bootloader import boot_sequence


def test_boot_sequence_output(capsys):
    boot_sequence(cycles=1, identity='test-mobius')
    out = capsys.readouterr().out
    assert 'PHASE TRIGGER' in out
    assert 'Hyper-Cube' in out
