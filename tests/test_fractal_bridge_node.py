import fractal_bridge_node


def test_stub_mode_runs(capsys):
    """Ensure the script runs in stub mode when ROS 2 isn't installed."""

    fractal_bridge_node.rclpy = None
    fractal_bridge_node.main(cycles=2)
    out = capsys.readouterr().out
    assert 'PHASE TRIGGER' in out
