"""Mutable Observatory example for the OAL-001 synthetic dry-run slice.

This file contains data-only strategy weights. The sandbox parses the literal
assignment with ``ast.literal_eval`` and never executes candidate source.
"""

STRATEGY_WEIGHTS = {
    "primary": 0.75,
    "exploration": 0.25,
}
