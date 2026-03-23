# SDL Adaptive Campaigns

Adaptive campaign management for self-driving labs: multi-environment lifecycle and phase-adaptive acquisition.

## Overview

This repository extends the [sdl-lab](https://github.com/sdl-lab) ecosystem with:

1. **Multi-environment lifecycle management** — Track, correlate, and reactivate multiple experimental environments
2. **Phase-adaptive acquisition** — Dynamically adjust exploration/exploitation based on campaign phase
3. **Research harness** — Systematic experiments to derive design rules for adaptive strategies

## Relationship to sdl-lab

This repo consumes sdl-lab packages as **pip dependencies** (read-only). It does not modify sdl-lab internals.

| sdl-lab Package | What We Use | How We Extend |
|-----------------|-------------|---------------|
| `sdl-core` | `FormulationSimulator`, `GPSurrogate` | Wrap with `EnvironmentManager` (composition) |
| `sdl-strategies` | `BatchBO` | Subclass as `AdaptiveBatchBO` for dynamic β |
| `sdl-orchestration` | `AdaptivePlanner`, `RuleCatalog` | Add new rules via `catalog.add()` |
| `sdl-experiments` | `ExperimentRunner`, `ComparisonRunner` | Use as research harness backbone |
| `sdl-analysis` | `compare_strategies`, metrics | Use for experiment analysis |
| `sdl-benchmarks` | `load_ros_dataset` | Use for validation data |

## Installation

```bash
# Clone and install in development mode
git clone https://github.com/sdl-lab/sdl-adaptive-campaigns.git
cd sdl-adaptive-campaigns
pip install -e ".[dev]"
```

## Repository Structure

```
sdl-adaptive-campaigns/
│
├── sdl_adaptive/              # Installable package (implementation)
│   ├── environments/          # Multi-environment lifecycle
│   │   ├── context.py         # EnvironmentContext
│   │   ├── registry.py        # EnvironmentRegistry
│   │   ├── correlation.py     # EnvironmentCorrelationTracker
│   │   ├── reactivation.py    # ReactivationBatchSelector
│   │   └── manager.py         # EnvironmentManager
│   │
│   └── acquisition/           # Phase-adaptive acquisition
│       ├── state.py           # AcquisitionState, per-env β
│       ├── phase_detector.py  # CampaignPhaseDetector
│       └── adaptive_bo.py     # AdaptiveBatchBO
│
├── research/                  # Research harness (not installable)
│   ├── stage1_phase_labelling/
│   ├── stage2_validation/
│   └── design_rules/
│
└── tests/
```

## Extension Patterns

### Pattern 1: Composition (EnvironmentManager)

```python
from sdl_core import FormulationSimulator
from sdl_adaptive.environments import EnvironmentManager

simulator = FormulationSimulator.fit(data)
env_manager = EnvironmentManager(simulator)  # Wraps, doesn't modify
```

### Pattern 2: Subclassing (AdaptiveBatchBO)

```python
from sdl_strategies import BatchBO
from sdl_adaptive.acquisition import AdaptiveBatchBO

strategy = AdaptiveBatchBO(
    design_space=space,
    acquisition_state=acq_state,  # Manages per-environment β
)
```

### Pattern 3: Rule Extension (RuleCatalog)

```python
from sdl_orchestration import RuleCatalog, Rule

catalog = RuleCatalog.default()
catalog.add(my_new_rule)  # Direct API, no modification
```

## Research Stages

1. **Stage 1 — Phase Labelling**: Does phase structure exist in campaigns?
2. **Stage 2 — Validation**: A/B/C/D/E comparison of adaptive strategies
3. **Design Rules**: Derive actionable rules from findings

## License

MIT License
