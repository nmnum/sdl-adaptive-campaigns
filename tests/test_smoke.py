"""
Smoke test: Verify all sdl-lab imports work correctly.

This test validates that:
1. All sdl-lab packages are installed and importable
2. Key classes can be instantiated
3. The extension patterns (composition, subclassing) work
"""

import pytest


class TestSDLLabImports:
    """Test that all sdl-lab packages import correctly."""

    def test_sdl_core_imports(self):
        """Test sdl-core imports."""
        from sdl_core import FormulationSimulator, FormulationSpace, Formulation
        from sdl_core.sim.surrogates import GPSurrogate, RFSurrogate
        from sdl_core.sim.noise_models import GaussianNoise
        from sdl_core.sim.design_space import FormulationSpace

        assert FormulationSimulator is not None
        assert FormulationSpace is not None
        assert GPSurrogate is not None

    def test_sdl_strategies_imports(self):
        """Test sdl-strategies imports."""
        from sdl_strategies import Strategy, get_strategy
        from sdl_strategies.base import Strategy
        from sdl_strategies.bayesian.batch_bo import BatchBO

        assert Strategy is not None
        assert BatchBO is not None

    def test_sdl_orchestration_imports(self):
        """Test sdl-orchestration imports."""
        from sdl_orchestration import AdaptivePlanner, RuleCatalog, AuditLogger
        from sdl_orchestration.rules.rules import Rule, Condition, Action
        from sdl_orchestration.planner.planner import AdaptivePlanner

        assert AdaptivePlanner is not None
        assert RuleCatalog is not None
        assert Rule is not None

    def test_sdl_benchmarks_imports(self):
        """Test sdl-benchmarks imports."""
        from sdl_benchmarks import load_ros_dataset, RosDataset
        from sdl_benchmarks.loaders.ros_data_loader import load_ros_dataset

        assert load_ros_dataset is not None
        assert RosDataset is not None

    def test_sdl_analysis_imports(self):
        """Test sdl-analysis imports."""
        from sdl_analysis import hit_rate, compare_strategies, plot_convergence
        from sdl_analysis.metrics import hit_rate, sample_efficiency

        assert hit_rate is not None
        assert compare_strategies is not None

    def test_sdl_experiments_imports(self):
        """Test sdl-experiments imports."""
        from sdl_experiments import ExperimentRunner, ComparisonRunner
        from sdl_experiments.runners.experiment_runner import ExperimentRunner

        assert ExperimentRunner is not None
        assert ComparisonRunner is not None


class TestSDLLabAPIs:
    """Test that key sdl-lab APIs have expected signatures."""

    def test_formulation_simulator_evaluate_signature(self):
        """Verify FormulationSimulator.evaluate() signature."""
        from sdl_core import FormulationSimulator
        import inspect

        sig = inspect.signature(FormulationSimulator.evaluate)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "formulation" in params

    def test_formulation_simulator_evaluate_batch_signature(self):
        """Verify FormulationSimulator.evaluate_batch() signature."""
        from sdl_core import FormulationSimulator
        import inspect

        sig = inspect.signature(FormulationSimulator.evaluate_batch)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "formulations" in params

    def test_batch_bo_has_beta_attribute(self):
        """Verify BatchBO has beta as instance attribute."""
        from sdl_strategies.bayesian.batch_bo import BatchBO
        import inspect

        sig = inspect.signature(BatchBO.__init__)
        params = list(sig.parameters.keys())

        assert "beta" in params, "BatchBO.__init__ should accept beta parameter"

    def test_rule_catalog_has_add_method(self):
        """Verify RuleCatalog has add() method."""
        from sdl_orchestration import RuleCatalog

        assert hasattr(RuleCatalog, "add"), "RuleCatalog should have add() method"
        assert callable(getattr(RuleCatalog, "add"))

    def test_adaptive_planner_has_recommend_method(self):
        """Verify AdaptivePlanner has recommend() method."""
        from sdl_orchestration import AdaptivePlanner

        assert hasattr(AdaptivePlanner, "recommend"), "AdaptivePlanner should have recommend() method"


class TestExtensionPatterns:
    """Test that extension patterns work correctly."""

    def test_environment_manager_wraps_simulator(self):
        """Test composition pattern: EnvironmentManager wraps FormulationSimulator."""
        from sdl_adaptive.environments.manager import EnvironmentManager

        # Should accept simulator as argument (composition)
        import inspect
        sig = inspect.signature(EnvironmentManager.__init__)
        params = list(sig.parameters.keys())

        assert "simulator" in params

    def test_adaptive_batch_bo_extends_batch_bo(self):
        """Test subclassing pattern: AdaptiveBatchBO extends BatchBO."""
        from sdl_adaptive.acquisition.adaptive_bo import AdaptiveBatchBO
        from sdl_strategies.bayesian.batch_bo import BatchBO

        assert issubclass(AdaptiveBatchBO, BatchBO)

    def test_acquisition_state_provides_beta(self):
        """Test AcquisitionState provides per-environment beta."""
        from sdl_adaptive.acquisition.state import AcquisitionState

        state = AcquisitionState(default_beta=2.0)
        beta = state.beta_for("env_1", iteration=0)

        assert beta == 2.0

        state.set_beta("env_1", 3.0, reason="test")
        beta = state.beta_for("env_1", iteration=1)

        assert beta == 3.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
