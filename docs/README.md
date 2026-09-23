# Documentation

Start with [THESIS_IMPLEMENTATION.md](THESIS_IMPLEMENTATION.md) for the architecture,
repository layout, reproducibility conventions, and current status.

Everything else is either how the system works, how to run a study, or what a study
measured. Most methods have a matching results document.

## Design — how the system works

| Document | Contents |
| --- | --- |
| [MAPPO.md](design/MAPPO.md) | the discrete MAPPO implementation |
| [COLLISION_AVOIDANCE_ENVIRONMENT.md](design/COLLISION_AVOIDANCE_ENVIRONMENT.md) | observations, rewards, safety screening |
| [MANEUVER_CONTRACT.md](design/MANEUVER_CONTRACT.md) | the action set and how burns are realized |
| [TRAINING_SCENARIOS.md](design/TRAINING_SCENARIOS.md) | the scenario generator and train/test split |
| [TOY_ENVIRONMENT.md](design/TOY_ENVIRONMENT.md) | the toy environment that validates the learning loop |

## Methods — how to run a study

| Document | Pairs with |
| --- | --- |
| [K_DT_CALIBRATION.md](methods/K_DT_CALIBRATION.md) | [K_DT_RESULTS.md](results/K_DT_RESULTS.md) |
| [MANEUVER_SIZING.md](methods/MANEUVER_SIZING.md) | [MANEUVER_SIZING_RESULTS.md](results/MANEUVER_SIZING_RESULTS.md) |
| [TRAINING.md](methods/TRAINING.md) | [TRAINING_TRIALS.md](results/TRAINING_TRIALS.md), [TRAINING_RESULTS.md](results/TRAINING_RESULTS.md) |
| [EVALUATION.md](methods/EVALUATION.md) | [COLLINEAR_BASELINE.md](results/COLLINEAR_BASELINE.md), [MULTITHREAT_BENCHMARK.md](results/MULTITHREAT_BENCHMARK.md), [FUEL_TRADEOFF.md](results/FUEL_TRADEOFF.md) |
| [SCALABILITY.md](methods/SCALABILITY.md) | [SCALABILITY_RESULTS.md](results/SCALABILITY_RESULTS.md) |

## Results — what was measured

[results/README.md](results/README.md) summarises every outcome and states what is not
claimed.

| Document | Question it answers |
| --- | --- |
| [BASELINES.md](results/BASELINES.md) | the three policies the methodology names, on every benchmark |
| [K_DT_RESULTS.md](results/K_DT_RESULTS.md) | how many neighbours, and how often to decide |
| [MANEUVER_SIZING_RESULTS.md](results/MANEUVER_SIZING_RESULTS.md) | how large one maneuver should be |
| [TRAINING_TRIALS.md](results/TRAINING_TRIALS.md) | every settings experiment and its evidence |
| [TRAINING_RESULTS.md](results/TRAINING_RESULTS.md) | the adopted curriculum, its seed repeat, its evaluation |
| [COLLINEAR_BASELINE.md](results/COLLINEAR_BASELINE.md) | the traditional along-track heuristic, measured |
| [MULTITHREAT_BENCHMARK.md](results/MULTITHREAT_BENCHMARK.md) | where the policy beats the rule, and by how much |
| [FUEL_TRADEOFF.md](results/FUEL_TRADEOFF.md) | what a cheaper policy costs, across four delta-v penalties |
| [SCALABILITY_RESULTS.md](results/SCALABILITY_RESULTS.md) | catalog-scale results and what they show about LEO |

## Reading order

For the result: [TRAINING_RESULTS.md](results/TRAINING_RESULTS.md), then
[MULTITHREAT_BENCHMARK.md](results/MULTITHREAT_BENCHMARK.md) for where the advantage
comes from, then [SCALABILITY_RESULTS.md](results/SCALABILITY_RESULTS.md) for how often
that situation arises and what the method costs at 10,000 agents.

For the design: [COLLISION_AVOIDANCE_ENVIRONMENT.md](design/COLLISION_AVOIDANCE_ENVIRONMENT.md),
then [K_DT_RESULTS.md](results/K_DT_RESULTS.md) for why the neighbourhood is one
satellite wide.
