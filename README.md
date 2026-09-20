# Scalable Collision Avoidance in Large LEO Constellations

Multi-agent reinforcement learning for autonomous collision avoidance, trained and
evaluated on real two-line element catalogue data.

One shared policy — about 11,700 weights — is flown by every satellite. Each one sees
only its single most threatening neighbour and decides every 120 seconds whether to
burn. No satellite communicates with another, and no priority rule breaks ties, so any
coordination between them is emergent rather than designed.

## Result so far

At 64 agents on held-out scenarios, against a physics-based rule baseline:

| Metric | Coasting | Rule | Policy |
| --- | ---: | ---: | ---: |
| Close approaches per episode | 43.60 | 4.30 | **2.40** |
| Closest approach (m) | 40.2 | 289.1 | **420.0** |
| Collisions | 0 | 0 | 0 |
| Delta-v per agent (m/s) | 0.00 | **0.676** | 1.119 |

The policy resolves 95% of the conjunctions a coasting constellation would suffer,
against the rule's 90%, and spends 65% more delta-v doing it. Numbers above come from
a single training run evaluated on 20 episodes; see the limitations in
[docs/TRAINING_TRIALS.md](docs/TRAINING_TRIALS.md).

## Method

| Element | Choice |
| --- | --- |
| Algorithm | MAPPO with centralized training, decentralized execution |
| Observation | own state plus the top-ranked neighbour, 22 inputs |
| Locality | `k = 1` neighbour, 120 s decision interval, both calibrated |
| Actions | 7 discrete burns in the RSW frame, 0.5 m/s at 7 N |
| Dynamics | Orekit with J2 and drag for training, SGP4 for scale evaluation |
| Scenarios | real TLEs, with conjunctions built backwards from real close-call geometry |

The critic sees the whole constellation during training and is discarded afterwards,
so the deployed policy is the actor alone and its input width does not grow with the
population.

## Documentation

Start with [docs/THESIS_IMPLEMENTATION.md](docs/THESIS_IMPLEMENTATION.md) for the
architecture and current status.

| Document | Contents |
| --- | --- |
| [COLLISION_AVOIDANCE_ENVIRONMENT.md](docs/COLLISION_AVOIDANCE_ENVIRONMENT.md) | observations, rewards, safety screening |
| [K_DT_CALIBRATION.md](docs/K_DT_CALIBRATION.md) | how `k` and the decision interval were chosen |
| [MANEUVER_CONTRACT.md](docs/MANEUVER_CONTRACT.md) | the action set and how burns are realized |
| [TRAINING.md](docs/TRAINING.md) | running and resuming training |
| [TRAINING_SCENARIOS.md](docs/TRAINING_SCENARIOS.md) | the scenario generator and train/test split |
| [TRAINING_TRIALS.md](docs/TRAINING_TRIALS.md) | every settings experiment and its evidence |
| [TRAINING_RESULTS.md](docs/TRAINING_RESULTS.md) | the full curriculum run and its evaluation |
| [EVALUATION.md](docs/EVALUATION.md) | baselines, metrics, frozen benchmark |
| [SCALABILITY.md](docs/SCALABILITY.md) | the large-population evaluator |

## Running it

```sh
python3.11 -m venv .venv && .venv/bin/pip install -e .
.venv/bin/python -m pytest -q --ignore=tests/test_interface_connections.py

.venv/bin/oz train --config configs/mappo_stage1.json --output runs/stage1
.venv/bin/oz evaluate --config configs/eval_stage2.json \
  --policy noop --policy rule --policy final=runs/stage2/checkpoints/latest.pt \
  --episodes 20 --output runs/eval
```

Training runs a 16 → 64 → 150 agent curriculum, each stage starting from the previous
stage's actor. `configs/eval_stage*.json` hold the benchmark fixed so results stay
comparable as the training mix changes.

## Data

`data/full/` holds 24,922 catalogued LEO objects: 15,742 payloads treated as
maneuverable and 9,180 debris. Scenarios draw real satellites and rebuild real
close-call geometry inside the simulator's own dynamics, with an 80/20 split by
hashed identifier so evaluation never reuses a training satellite.

## Built on OrbitZoo

This repository began as a fork of [OrbitZoo](https://github.com/orbitzoo/orbit_zoo),
which provides the orbital dynamics, the Orekit and SGP4 propagation backends, the
3D interface, and the base MARL scaffolding. The collision-avoidance environment,
scenario generator, maneuver contract, training curriculum, evaluation suite, and
scalability evaluator in `src/orbitzoo/thesis/` are this project's additions.

Three fixes to the upstream dynamics are carried here: correcting the orbit epoch to
the configured start time, allowing covariance computation to be disabled, and
per-body burn durations.

> **Licence status is unresolved.** Upstream OrbitZoo ships no licence file, so its
> terms are not yet established. Resolve this with the OrbitZoo authors before
> publishing or redistributing this repository.
