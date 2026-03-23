"""
Reactivation batch selector for dormant environments.

Selects which environments to reactivate and how many samples to allocate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import numpy as np

from sdl_adaptive.environments.registry import EnvironmentRegistry
from sdl_adaptive.environments.correlation import EnvironmentCorrelationTracker


@dataclass
class ReactivationCandidate:
    """Candidate environment for reactivation."""
    env_id: str
    dormant_iterations: int
    correlation_with_active: float
    priority_score: float


class ReactivationBatchSelector:
    """
    Select environments for reactivation and allocate samples.

    Decides when to reactivate dormant environments based on:
    - Time since last observation
    - Correlation with currently active environment
    - Expected information gain

    Parameters:
        min_dormant_iterations: Minimum iterations before considering reactivation
        correlation_threshold: Minimum correlation to consider transfer
        reactivation_fraction: Fraction of batch to allocate to reactivation
    """

    def __init__(
        self,
        min_dormant_iterations: int = 5,
        correlation_threshold: float = 0.3,
        reactivation_fraction: float = 0.25,
    ):
        self.min_dormant_iterations = min_dormant_iterations
        self.correlation_threshold = correlation_threshold
        self.reactivation_fraction = reactivation_fraction

    def select_for_reactivation(
        self,
        registry: EnvironmentRegistry,
        correlation_tracker: EnvironmentCorrelationTracker,
        current_iteration: int,
        batch_size: int,
    ) -> List[ReactivationCandidate]:
        """
        Select environments for reactivation.

        Parameters:
            registry: Environment registry
            correlation_tracker: Tracks cross-environment correlations
            current_iteration: Current campaign iteration
            batch_size: Total batch size available

        Returns:
            List of ReactivationCandidate objects, sorted by priority
        """
        active = registry.active
        if active is None:
            return []

        candidates = []

        for env_id in registry.all_ids:
            if env_id == active.env_id:
                continue

            env = registry.get(env_id)
            if env is None:
                continue

            # Calculate dormant iterations (simplified - would need tracking)
            dormant_iterations = self.min_dormant_iterations + 1  # Placeholder

            if dormant_iterations < self.min_dormant_iterations:
                continue

            # Get correlation with active environment
            correlation = correlation_tracker.get_correlation(active.env_id, env_id)
            if correlation is None:
                correlation = 0.5  # Default assumption

            if correlation < self.correlation_threshold:
                continue

            # Calculate priority score
            priority = self._calculate_priority(
                dormant_iterations=dormant_iterations,
                correlation=correlation,
            )

            candidates.append(ReactivationCandidate(
                env_id=env_id,
                dormant_iterations=dormant_iterations,
                correlation_with_active=correlation,
                priority_score=priority,
            ))

        # Sort by priority (highest first)
        candidates.sort(key=lambda c: c.priority_score, reverse=True)

        # Limit to reactivation budget
        max_reactivations = max(1, int(batch_size * self.reactivation_fraction))
        return candidates[:max_reactivations]

    def _calculate_priority(
        self,
        dormant_iterations: int,
        correlation: float,
    ) -> float:
        """Calculate reactivation priority score."""
        # Higher priority for longer dormancy and higher correlation
        dormancy_factor = min(1.0, dormant_iterations / 10.0)
        return dormancy_factor * correlation

    def allocate_samples(
        self,
        candidates: List[ReactivationCandidate],
        total_samples: int,
    ) -> Dict[str, int]:
        """
        Allocate samples across reactivation candidates.

        Parameters:
            candidates: Reactivation candidates
            total_samples: Total samples available for reactivation

        Returns:
            Dict mapping env_id to number of samples
        """
        if not candidates:
            return {}

        # Allocate proportionally to priority score
        total_priority = sum(c.priority_score for c in candidates)
        if total_priority == 0:
            # Equal allocation
            per_env = total_samples // len(candidates)
            return {c.env_id: per_env for c in candidates}

        allocation = {}
        remaining = total_samples

        for i, candidate in enumerate(candidates):
            if i == len(candidates) - 1:
                # Last candidate gets remainder
                allocation[candidate.env_id] = remaining
            else:
                share = int(total_samples * candidate.priority_score / total_priority)
                allocation[candidate.env_id] = share
                remaining -= share

        return allocation
