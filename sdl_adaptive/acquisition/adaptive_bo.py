"""
Adaptive Bayesian Optimization with dynamic β.

Extends BatchBO from sdl-strategies via subclassing.
"""

from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from sdl_strategies.bayesian.batch_bo import BatchBO
from sdl_adaptive.acquisition.state import AcquisitionState
from sdl_adaptive.acquisition.phase_detector import CampaignPhaseDetector, CampaignPhase

if TYPE_CHECKING:
    from sdl_core.sim.design_space import FormulationSpace, Formulation


class AdaptiveBatchBO(BatchBO):
    """
    Batch Bayesian Optimization with adaptive β.

    Extends BatchBO to dynamically adjust β based on:
    - Current environment
    - Campaign phase
    - Reactivation status

    Parameters:
        design_space: Formulation design space
        acquisition_state: Manages per-environment β
        phase_detector: Detects campaign phase (optional)
        **kwargs: Passed to BatchBO
    """

    def __init__(
        self,
        design_space: "FormulationSpace",
        acquisition_state: Optional[AcquisitionState] = None,
        phase_detector: Optional[CampaignPhaseDetector] = None,
        **kwargs,
    ):
        # Remove beta from kwargs if present (we manage it dynamically)
        kwargs.pop("beta", None)
        super().__init__(design_space=design_space, **kwargs)

        self.acq_state = acquisition_state or AcquisitionState()
        self.phase_detector = phase_detector or CampaignPhaseDetector()
        self._current_env_id: str = "default"
        self._results_history: List[dict] = []

    def set_environment(self, env_id: str) -> None:
        """Set current environment for β lookup."""
        self._current_env_id = env_id

    def suggest(self, batch_size: int = 1) -> List["Formulation"]:
        """
        Suggest next batch with adaptive β.

        Updates self.beta based on current environment and phase
        before delegating to parent class.
        """
        # Get β for current environment
        self.beta = self.acq_state.beta_for(
            self._current_env_id, 
            self.n_observations
        )

        # Optionally adjust based on phase
        if self._results_history:
            detection = self.phase_detector.detect(self._results_history)
            if detection.phase == CampaignPhase.EXPLOITATION:
                # Reduce exploration in exploitation phase
                self.beta = max(0.5, self.beta * 0.8)

        # Delegate to parent
        return super().suggest(batch_size)

    def observe(self, formulations: List["Formulation"], results: List[dict]) -> None:
        """Record observations and update history."""
        super().observe(formulations, results)
        self._results_history.extend(results)
