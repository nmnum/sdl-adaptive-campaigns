"""
Environment context for multi-environment campaigns.

Wraps FormulationSimulator evaluation with environment-specific perturbations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass
class EnvironmentContext:
    """
    Context for a single experimental environment.

    Attributes:
        env_id: Unique environment identifier
        created_at: When environment was first observed
        perturbation: Environment-specific perturbation parameters
        metadata: Additional environment metadata
    """

    env_id: str
    created_at: datetime = field(default_factory=datetime.now)
    perturbation: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def apply_to_formulation(self, formulation: Any) -> Any:
        """Apply environment perturbation to formulation before evaluation."""
        # Default: no perturbation (pass-through)
        return formulation

    def apply_to_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment perturbation to result after evaluation."""
        # Default: no perturbation (pass-through)
        return result
