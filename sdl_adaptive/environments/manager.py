"""
Environment manager orchestrating multi-environment campaigns.

Wraps FormulationSimulator from sdl-core via composition.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sdl_adaptive.environments.registry import EnvironmentRegistry
from sdl_adaptive.environments.correlation import EnvironmentCorrelationTracker
from sdl_adaptive.environments.context import EnvironmentContext

if TYPE_CHECKING:
    from sdl_core import FormulationSimulator
    from sdl_core.sim.design_space import Formulation


class EnvironmentManager:
    """
    Orchestrate multi-environment campaigns.

    Wraps FormulationSimulator (composition pattern) to add:
    - Environment tracking via EnvironmentRegistry
    - Cross-environment correlation tracking
    - Environment-aware evaluation

    Parameters:
        simulator: FormulationSimulator from sdl-core (unchanged)
    """

    def __init__(self, simulator: "FormulationSimulator"):
        self._simulator = simulator  # Composition, not inheritance
        self.registry = EnvironmentRegistry()
        self.correlation_tracker = EnvironmentCorrelationTracker()

    def evaluate(
        self, 
        formulation: "Formulation",
        env_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate formulation in specified environment.

        Wraps simulator.evaluate() with environment context.
        """
        # Get environment context
        if env_id:
            ctx = self.registry.get(env_id)
            if ctx is None:
                raise ValueError(f"Environment {env_id} not registered")
        else:
            ctx = self.registry.active

        # Apply environment perturbation to input
        if ctx:
            formulation = ctx.apply_to_formulation(formulation)

        # Call underlying simulator (unchanged sdl-core class)
        result = self._simulator.evaluate(formulation)

        # Apply environment perturbation to output
        if ctx:
            result = ctx.apply_to_result(result)
            result["env_id"] = ctx.env_id

        return result

    def evaluate_batch(
        self,
        formulations: List["Formulation"],
        env_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Evaluate batch of formulations in specified environment."""
        return [self.evaluate(f, env_id) for f in formulations]

    @property
    def simulator(self) -> "FormulationSimulator":
        """Access underlying simulator."""
        return self._simulator
