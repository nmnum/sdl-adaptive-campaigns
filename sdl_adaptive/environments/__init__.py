"""
Multi-environment lifecycle management.

Extends sdl-core's FormulationSimulator with:
- EnvironmentContext: Per-environment state
- EnvironmentRegistry: Track multiple environments
- EnvironmentCorrelationTracker: Cross-environment correlations
- ReactivationBatchSelector: Select environments for reactivation
- EnvironmentManager: Orchestrate multi-environment campaigns
"""

from sdl_adaptive.environments.context import EnvironmentContext
from sdl_adaptive.environments.registry import EnvironmentRegistry
from sdl_adaptive.environments.correlation import EnvironmentCorrelationTracker
from sdl_adaptive.environments.reactivation import ReactivationBatchSelector
from sdl_adaptive.environments.manager import EnvironmentManager

__all__ = [
    "EnvironmentContext",
    "EnvironmentRegistry",
    "EnvironmentCorrelationTracker",
    "ReactivationBatchSelector",
    "EnvironmentManager",
]
