"""
Phase-adaptive acquisition functions.

Extends sdl-strategies' BatchBO with:
- AcquisitionState: Per-environment β management
- CampaignPhaseDetector: Detect exploration/exploitation phases
- AdaptiveBatchBO: Dynamic β adjustment
"""

from sdl_adaptive.acquisition.state import AcquisitionState
from sdl_adaptive.acquisition.phase_detector import CampaignPhaseDetector
from sdl_adaptive.acquisition.adaptive_bo import AdaptiveBatchBO

__all__ = [
    "AcquisitionState",
    "CampaignPhaseDetector",
    "AdaptiveBatchBO",
]
