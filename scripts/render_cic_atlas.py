#!/usr/bin/env python3
"""Preferred CIC-named entry point for the TerraNova atlas renderer.

The implementation remains in render_prism_atlas.py for backward compatibility
with historical script names and raw OpenAI Prism export paths.
"""

from render_prism_atlas import main


if __name__ == "__main__":
    raise SystemExit(main())
