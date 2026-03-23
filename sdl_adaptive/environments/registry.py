"""
Registry for tracking multiple experimental environments.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from datetime import datetime

from sdl_adaptive.environments.context import EnvironmentContext


class EnvironmentRegistry:
    """
    Registry for tracking multiple experimental environments.

    Manages environment lifecycle: creation, activation, deactivation, reactivation.
    """

    def __init__(self):
        self._environments: Dict[str, EnvironmentContext] = {}
        self._active_env_id: Optional[str] = None
        self._history: List[Dict] = []

    def register(self, env_id: str, **kwargs) -> EnvironmentContext:
        """Register a new environment."""
        if env_id in self._environments:
            raise ValueError(f"Environment {env_id} already registered")

        ctx = EnvironmentContext(env_id=env_id, **kwargs)
        self._environments[env_id] = ctx
        self._history.append({
            "action": "register",
            "env_id": env_id,
            "timestamp": datetime.now(),
        })
        return ctx

    def get(self, env_id: str) -> Optional[EnvironmentContext]:
        """Get environment by ID."""
        return self._environments.get(env_id)

    def activate(self, env_id: str) -> None:
        """Set active environment."""
        if env_id not in self._environments:
            raise ValueError(f"Environment {env_id} not registered")
        self._active_env_id = env_id
        self._history.append({
            "action": "activate",
            "env_id": env_id,
            "timestamp": datetime.now(),
        })

    @property
    def active(self) -> Optional[EnvironmentContext]:
        """Get currently active environment."""
        if self._active_env_id:
            return self._environments.get(self._active_env_id)
        return None

    @property
    def all_ids(self) -> List[str]:
        """Get all registered environment IDs."""
        return list(self._environments.keys())

    def __len__(self) -> int:
        return len(self._environments)
