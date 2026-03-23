"""
Acquisition state management for phase-adaptive optimization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime


@dataclass
class AcquisitionState:
    """
    Manage per-environment acquisition parameters.

    Tracks β (exploration/exploitation balance) for each environment,
    allowing dynamic adjustment based on campaign phase.

    Attributes:
        default_beta: Default β for new environments
        beta_bounds: (min, max) bounds for β
    """

    default_beta: float = 2.0
    beta_bounds: tuple = (0.1, 10.0)

    _env_betas: Dict[str, float] = field(default_factory=dict)
    _history: list = field(default_factory=list)

    def beta_for(self, env_id: str, iteration: int) -> float:
        """Get β for environment at given iteration."""
        if env_id not in self._env_betas:
            self._env_betas[env_id] = self.default_beta
        return self._env_betas[env_id]

    def set_beta(self, env_id: str, beta: float, reason: str = "") -> None:
        """Set β for environment."""
        beta = max(self.beta_bounds[0], min(self.beta_bounds[1], beta))
        old_beta = self._env_betas.get(env_id, self.default_beta)
        self._env_betas[env_id] = beta
        self._history.append({
            "env_id": env_id,
            "old_beta": old_beta,
            "new_beta": beta,
            "reason": reason,
            "timestamp": datetime.now(),
        })

    def boost_for_reactivation(self, env_id: str, boost_factor: float = 1.5) -> None:
        """Boost β when reactivating an environment."""
        current = self.beta_for(env_id, 0)
        self.set_beta(env_id, current * boost_factor, reason="reactivation_boost")

    def decay_beta(self, env_id: str, decay_rate: float = 0.95) -> None:
        """Decay β over time (shift toward exploitation)."""
        current = self.beta_for(env_id, 0)
        self.set_beta(env_id, current * decay_rate, reason="decay")
