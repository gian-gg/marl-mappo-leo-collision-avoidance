# Scalable Collision Avoidance in Large LEO Constellations

Multi-agent reinforcement learning for autonomous collision avoidance in low Earth
orbit, trained and evaluated on real two-line element catalogue data.

One shared policy is flown by every satellite. Each one sees only its single most
threatening neighbour and decides every 120 seconds whether to burn. No satellite
communicates with another and no priority rule breaks ties, so any coordination
between them is emergent rather than designed.

The repository holds the collision-avoidance environment, the scenario generator,
the training curriculum, and the evaluation and scalability suites, all under
`src/orbitzoo/thesis/`, plus the `oz` command-line interface that drives them.

## Result

At 150 agents on held-out scenarios, against a physics-based rule baseline:

| Metric | Coasting | Collinear heuristic | Rule | Policy |
| --- | ---: | ---: | ---: | ---: |
| Close approaches per episode | 101.20 | 15.80 | 10.40 | **7.45** |
| Conjunctions resolved | — | 84.4% | 89.7% | **92.6%** |
| Closest approach (m) | 40.6 | 189.1 | 206.9 | **249.6** |
| Collisions | 0 | 0 | 0 | 0 |
| Delta-v incl. return (m/s) | 0.00 | 2.39 | **1.40** | 1.76 |

Two classical baselines: the collinear heuristic thrusts along the orbital track, the
rule searches all six directions and is close to optimal for an isolated conjunction.
The policy resolves 53% more conjunctions than the heuristic for 26% less total
delta-v, and 2.9 points more than the rule at 26% more delta-v
([COLLINEAR_BASELINE.md](docs/results/COLLINEAR_BASELINE.md)).

Retraining from scratch with a different seed gives 7.05, so the result reproduces.

The margin over the rule comes from encounters where a satellite faces two threats at
once. Raising their share from 15% to 100% of the mix grows the margin from 2.9 to 7.5
points, with the policy ahead in 59 of 60 episodes
([MULTITHREAT_BENCHMARK.md](docs/results/MULTITHREAT_BENCHMARK.md)). Those encounters are rare
in today's catalog, where the policy instead ties the rule while its cost per
satellite stays flat to 10,000 agents
([SCALABILITY_RESULTS.md](docs/results/SCALABILITY_RESULTS.md)). It spends 23–28% more
delta-v throughout.

## Documentation

Start with [THESIS_IMPLEMENTATION.md](docs/THESIS_IMPLEMENTATION.md) for the
architecture, repository layout, and current status.

| Document | Contents |
| --- | --- |
| [COLLISION_AVOIDANCE_ENVIRONMENT.md](docs/design/COLLISION_AVOIDANCE_ENVIRONMENT.md) | observations, rewards, safety screening |
| [MANEUVER_CONTRACT.md](docs/design/MANEUVER_CONTRACT.md) | the action set and how burns are realized |
| [MAPPO.md](docs/design/MAPPO.md) | the discrete MAPPO implementation |
| [TOY_ENVIRONMENT.md](docs/design/TOY_ENVIRONMENT.md) | the toy environment that validates the learning loop |
| [K_DT_CALIBRATION.md](docs/methods/K_DT_CALIBRATION.md) | how `k` and the decision interval were chosen |
| [HYPERPARAMETER_CALIBRATION_FINDINGS.md](docs/results/K_DT_RESULTS.md) | the calibration's adopted result and evidence |
| [MANEUVER_SIZING.md](docs/methods/MANEUVER_SIZING.md) | how the delta-v of one maneuver is chosen |
| [MANEUVER_SIZING_FINDINGS.md](docs/results/MANEUVER_SIZING_RESULTS.md) | the adopted delta-v and thrust |
| [TRAINING.md](docs/methods/TRAINING.md) | running and resuming training |
| [TRAINING_SCENARIOS.md](docs/design/TRAINING_SCENARIOS.md) | the scenario generator and train/test split |
| [TRAINING_TRIALS.md](docs/results/TRAINING_TRIALS.md) | every settings experiment and its evidence |
| [TRAINING_RESULTS.md](docs/results/TRAINING_RESULTS.md) | the full curriculum run and its evaluation |
| [EVALUATION.md](docs/methods/EVALUATION.md) | baselines, metrics, frozen benchmark |
| [SCALABILITY.md](docs/methods/SCALABILITY.md) | the large-population evaluator |
| [MULTITHREAT_BENCHMARK.md](docs/results/MULTITHREAT_BENCHMARK.md) | where the policy beats the rule, and by how much |
| [SCALABILITY_RESULTS.md](docs/results/SCALABILITY_RESULTS.md) | catalog-scale results and what they show about LEO |

## Getting started

```sh
python3.11 -m venv .venv && .venv/bin/pip install -e .
.venv/bin/python -m pytest -q --ignore=tests/test_interface_connections.py
.venv/bin/oz --help
```

[TRAINING.md](docs/methods/TRAINING.md) covers training, [EVALUATION.md](docs/methods/EVALUATION.md)
covers evaluation.

## Built on OrbitZoo

The orbital dynamics, the Orekit and SGP4 propagation backends, the 3D interface, and
the base MARL scaffolding come from [OrbitZoo](https://github.com/orbitzoo/orbit_zoo).
[ATTRIBUTION.md](ATTRIBUTION.md) lists every upstream file, verbatim or modified.
