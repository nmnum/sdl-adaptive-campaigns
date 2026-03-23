"""
Campaign phase detection for adaptive acquisition.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional
import numpy as np


class CampaignPhase(Enum):
    """Campaign phases."""
    EXPLORATION = "exploration"
    TRANSITION = "transition"
    EXPLOITATION = "exploitation"


@dataclass
class PhaseDetection:
    """Result of phase detection."""
    phase: CampaignPhase
    confidence: float
    signals: Dict[str, float]


class CampaignPhaseDetector:
    """
    Detect campaign phase from observable signals.

    Uses hit rate, diversity, and improvement velocity to determine
    whether campaign is in exploration, transition, or exploitation phase.

    Parameters:
        exploration_threshold: Hit rate below this = exploration
        exploitation_threshold: Hit rate above this = exploitation
        window_size: Rolling window for signal computation
    """

    def __init__(
        self,
        exploration_threshold: float = 0.1,
        exploitation_threshold: float = 0.3,
        window_size: int = 3,
    ):
        self.exploration_threshold = exploration_threshold
        self.exploitation_threshold = exploitation_threshold
        self.window_size = window_size

    def detect(
        self,
        results: List[Dict[str, Any]],
        hit_threshold: float = 10.0,
    ) -> PhaseDetection:
        """
        Detect current campaign phase.

        Parameters:
            results: List of evaluation results
            hit_threshold: Solubility threshold for hits

        Returns:
            PhaseDetection with phase, confidence, and signals
        """
        if len(results) < self.window_size:
            return PhaseDetection(
                phase=CampaignPhase.EXPLORATION,
                confidence=0.5,
                signals={"n_results": len(results)},
            )

        # Compute signals from recent results
        recent = results[-self.window_size:]
        hit_rate = sum(
            1 for r in recent 
            if r.get("solubility", 0) >= hit_threshold
        ) / len(recent)

        # Determine phase
        if hit_rate < self.exploration_threshold:
            phase = CampaignPhase.EXPLORATION
            confidence = 1.0 - hit_rate / self.exploration_threshold
        elif hit_rate > self.exploitation_threshold:
            phase = CampaignPhase.EXPLOITATION
            confidence = (hit_rate - self.exploitation_threshold) / (1 - self.exploitation_threshold)
        else:
            phase = CampaignPhase.TRANSITION
            confidence = 0.5

        return PhaseDetection(
            phase=phase,
            confidence=confidence,
            signals={
                "hit_rate": hit_rate,
                "n_results": len(results),
            },
        )
