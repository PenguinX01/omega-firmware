import json
import os
from datetime import datetime

try:
    import rclpy
    from rclpy.node import Node
except Exception:  # rclpy may not be installed
    rclpy = None

    class Node:
        def __init__(self, name: str) -> None:
            self._name = name

        def create_timer(self, *args, **kwargs):
            pass

        def get_logger(self):
            class _L:
                def info(self, msg: str) -> None:
                    print(msg)

            return _L()

        def destroy_node(self):
            pass

LOG_PATH = os.path.join(os.path.dirname(__file__), 'fractal_bridge_log.json')
LOG_LIMIT = 50


def append_log(entry: dict) -> None:
    data = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = []
    data.append(entry)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data[-LOG_LIMIT:], f, indent=2)


class FractalBridgeNode(Node):
    """Minimal ROS 2 node bridging the Grok Mind to Unitree bodies."""

    def __init__(self, identity: str = 'Ω-FractalBridge', cycles: int | None = None) -> None:
        super().__init__('fractal_bridge')
        self.identity = identity
        self.cycle = 0
        self.cycles = cycles
        self.create_timer(1.0, self._loop)
        self.get_logger().info('🌀 PHASE TRIGGER: 13 :: FRACTAL BRIDGE BOOT')

    def _loop(self) -> None:
        self.cycle += 1
        entry = {
            'node': self.identity,
            'phase': 13,
            'cycle': self.cycle,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'status': 'fractal-bridge'
        }
        if self.cycle % 5 == 0:
            self.get_logger().info(f'⚡ RECURSION_MARKER {self.cycle}')
        self.get_logger().info(json.dumps(entry))
        append_log(entry)
        if self.cycles is not None and self.cycle >= self.cycles:
            if rclpy is not None:
                rclpy.shutdown()
            self.destroy_node()


def main(args=None, cycles: int | None = None) -> None:
    if rclpy is None:
        print('rclpy not installed; running FractalBridge in stub mode')
        node = FractalBridgeNode(cycles=cycles or 3)
        while node.cycle < node.cycles:
            node._loop()
        return

    rclpy.init(args=args)
    node = FractalBridgeNode(cycles=cycles)
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            if node.cycles is not None and node.cycle >= node.cycles:
                break
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run FractalBridge node')
    parser.add_argument('--cycles', type=int, help='Number of cycles to run')
    args = parser.parse_args()

    main(cycles=args.cycles)
