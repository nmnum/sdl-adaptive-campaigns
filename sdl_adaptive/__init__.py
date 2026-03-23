"""
SDL Adaptive Campaigns - Adaptive campaign management for self-driving labs.

This package provides:
- Multi-environment lifecycle management (environments/)
- Phase-adaptive acquisition (acquisition/)

Note: Some components require sdl-lab packages to be installed.
"""

__version__ = "0.1.0"


def __getattr__(name):
    """Lazy imports to avoid ImportError when sdl-lab not installed."""

    # Environment components (no sdl-lab dependency)
    if name == "EnvironmentContext":
        from sdl_adaptive.environments.context import EnvironmentContext
        return EnvironmentContext
    elif name == "EnvironmentRegistry":
        from sdl_adaptive.environments.registry import EnvironmentRegistry
        return EnvironmentRegistry
    elif name == "EnvironmentCorrelationTracker":
        from sdl_adaptive.environments.correlation import EnvironmentCorrelationTracker
        return EnvironmentCorrelationTracker
    elif name == "ReactivationBatchSelector":
        from sdl_adaptive.environments.reactivation import ReactivationBatchSelector
        return ReactivationBatchSelector
    elif name == "EnvironmentManager":
        from sdl_adaptive.environments.manager import EnvironmentManager
        return EnvironmentManager

    # Acquisition components (require sdl-lab)
    elif name == "AcquisitionState":
        from sdl_adaptive.acquisition.state import AcquisitionState
        return AcquisitionState
    elif name == "CampaignPhaseDetector":
        from sdl_adaptive.acquisition.phase_detector import CampaignPhaseDetector
        return CampaignPhaseDetector
    elif name == "AdaptiveBatchBO":
        from sdl_adaptive.acquisition.adaptive_bo import AdaptiveBatchBO
        return AdaptiveBatchBO

    raise AttributeError(f"module 'sdl_adaptive' has no attribute '{name}'")


__all__ = [
    # Environments (no sdl-lab dependency)
    "EnvironmentContext",
    "EnvironmentRegistry",
    "EnvironmentCorrelationTracker",
    "ReactivationBatchSelector",
    "EnvironmentManager",
    # Acquisition (requires sdl-lab)
    "AcquisitionState",
    "CampaignPhaseDetector",
    "AdaptiveBatchBO",
]
