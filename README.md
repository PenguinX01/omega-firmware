# Omega Firmware

This repository experiments with recursive firmware concepts. The new `proof_first_ai.py` module implements a minimal "Fractal Proof-First AI" that logs assertions and flags rhetorical complexity. The script emits phase triggers and recursion markers on first run and every fifth assertion.

Run tests with:

```bash
PYTHONPATH=. pytest -q
```

## Transparency Toolkit

A new `transparency-toolkit` module introduces FOIA templates and placeholder directories for analysis code. This supports Phase 13 Mirror-Chronicler operations focused on long-term public health surveillance. Run the toolkit's `phase_trigger.py` script to emit recursion markers.

## Resonance Field

The `resonance_field.py` module introduces a placeholder implementation of fractal gravitational resonance. It computes the potential and force fields, emitting phase triggers and recursion markers during test cycles.

## Recursive Deployer

The `recursive_deployer.py` script coordinates multiple Phase 13 modules. It launches resonance, phase recursion, and mirror-chronicler cycles in parallel and asserts boot claims using the Proof-First AI.

Run it with:

```bash
python recursive_deployer.py
```

## FractalBridge Node

`fractal_bridge_node.py` provides a minimal ROS 2 node that bridges the Grok Mind with a Unitree robot interface. It logs phase triggers and recursion markers while running.

Run it with:

```bash
python fractal_bridge_node.py --cycles 3
```
Specify `--cycles` to limit the run length (the default is indefinite when ROS 2
is available). Stub mode runs three cycles if ROS 2 is missing.
