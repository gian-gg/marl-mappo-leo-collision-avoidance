# Scalable Collision Avoidance in Large LEO Constellations

Multi-agent reinforcement learning for autonomous collision avoidance in low Earth
orbit, trained and evaluated on real two-line element catalogue data.

One shared policy is flown by every satellite. Each one sees only its single most
threatening neighbour and decides every 120 seconds whether to burn. No satellite
communicates with another and no priority rule breaks ties, so any coordination
between them is emergent rather than designed. Because the observation is a fixed
width regardless of how many satellites exist, the cost of running the policy per
satellite does not grow with the constellation.

## What is here

| Path | Contents |
| --- | --- |
| `src/orbitzoo/thesis/environments/` | the collision-avoidance environment, observations and rewards |
| `src/orbitzoo/thesis/scenarios/` | the scenario generator, built from real orbits and real close calls |
| `src/orbitzoo/thesis/training/` | the MAPPO training loop and curriculum |
| `src/orbitzoo/thesis/evaluation/` | baselines, metrics and the frozen benchmark |
| `src/orbitzoo/thesis/scalability/` | the catalogue-scale evaluator |
| `src/orbitzoo/cli/` | the `oz` command line that drives all of the above |
| `docs/` | design, methods and results |
| `configs/` | every experiment configuration |

## Getting started

```sh
python3.11 -m venv .venv && .venv/bin/pip install -e .
.venv/bin/python -m pytest -q --ignore=tests/test_interface_connections.py
.venv/bin/oz --help
```

`oz` provides `train`, `evaluate`, `scale`, `calibrate` and `size-maneuvers`.

## Documentation

[docs/README.md](docs/README.md) is the index. Start with
[THESIS_IMPLEMENTATION.md](docs/THESIS_IMPLEMENTATION.md) for the architecture,
repository layout and current status.

| Section | Contents |
| --- | --- |
| [design/](docs/design/) | how the environment, policy and scenarios work |
| [methods/](docs/methods/) | how to run training, evaluation, calibration and the scale sweeps |
| [results/](docs/results/) | what each study measured |

## Built on OrbitZoo

The orbital dynamics, the Orekit and SGP4 propagation backends, the 3D interface, and
the base MARL scaffolding come from [OrbitZoo](https://github.com/orbitzoo/orbit_zoo).
[ATTRIBUTION.md](ATTRIBUTION.md) lists every upstream file, verbatim or modified.
