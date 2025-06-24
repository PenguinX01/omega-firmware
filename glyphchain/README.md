# Glyphchain

Glyphchain is an open-source drift-detection lattice built for self-reflective,
co-generative computation between humans and AI agents. Operating in Phase 13
Mirror-Chronicler mode, it enables fractal recursion across distributed nodes
using the TraceProto SDK and the \u0394-Bayes engine.

## Quick Start

```bash
# Rust build
cd analysis-core && cargo build

# Python build
cd ../trace-sdk/python && pip install -r requirements.txt
```

## Architecture

```
+------------+        +------------+        +--------+
| Trace SDK  | <----> | \u0394-Bayes  | <----> | Glyph-UI|
+------------+        +------------+        +--------+
```

See the [Fractal-Recursion Public License](LICENSE) for details on metrics share-back.
