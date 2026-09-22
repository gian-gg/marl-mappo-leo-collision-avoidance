# Attribution

This repository contains code derived from [OrbitZoo](https://github.com/orbitzoo/orbit_zoo).
This file records exactly which files, so the boundary between upstream work and
this thesis's own work is auditable.

## Upstream source

| | |
| --- | --- |
| Repository | `https://github.com/orbitzoo/orbit_zoo` |
| Baseline commit | `09ac77c5` — "add perturbations to spacecrafts", 2026-07-16 |
| Upstream authors | orbitzoo (`cf2cbb65`, 2025-12-05), Alex (`f624d473`, `09ac77c5`, 2026-07-16) |

The baseline tree holds 66 files. This repository tracks 194.

## Carried verbatim from upstream

These 56 files are byte-identical to the baseline commit. None of this is the author's
work.

- `MANIFEST.in`
- `src/orbitzoo/dynamics/__init__.py`
- `src/orbitzoo/dynamics/classes.py`
- `src/orbitzoo/dynamics/constants.py`
- `src/orbitzoo/dynamics/orekit/__init__.py`
- `src/orbitzoo/dynamics/orekit/constants.py`
- `src/orbitzoo/dynamics/orekit/forces.py`
- `src/orbitzoo/dynamics/orekit/orekit_body.py`
- `src/orbitzoo/dynamics/orekit/orekit-data.zip`
- `src/orbitzoo/dynamics/tensorgator/__init__.py`
- `src/orbitzoo/dynamics/tensorgator/constants.py`
- `src/orbitzoo/dynamics/tensorgator/coord_conv.py`
- `src/orbitzoo/dynamics/tensorgator/prop_cpu.py`
- `src/orbitzoo/dynamics/tensorgator/prop_cuda.py`
- `src/orbitzoo/dynamics/tensorgator/propagation.py`
- `src/orbitzoo/interface/__init__.py`
- `src/orbitzoo/interface/interface_models.py`
- `src/orbitzoo/interface/logo_orbitzoo.png`
- `src/orbitzoo/interface/pygame_utils.py`
- `src/orbitzoo/rl_algorithms/__init__.py`
- `src/orbitzoo/rl_algorithms/ddpg.py`
- `src/orbitzoo/rl_algorithms/dqn.py`
- `src/orbitzoo/rl_algorithms/ippo.py`
- `src/orbitzoo/rl_algorithms/main.py`
- `src/orbitzoo/rl_algorithms/ppo.py`
- `src/orbitzoo/rl_algorithms/td3.py`
- `src/orbitzoo/rl_algorithms/utils.py`
- `src/orbitzoo/scripts/__init__.py`
- `src/orbitzoo/scripts/env_col_avoidance.py`
- `src/orbitzoo/scripts/env_constellation_fedavg.py`
- `src/orbitzoo/scripts/env_constellation_ippo.py`
- `src/orbitzoo/scripts/env_constellation_mappo.py`
- `src/orbitzoo/scripts/env_herrera.py`
- `src/orbitzoo/scripts/env_hohmann.py`
- `src/orbitzoo/scripts/env_kolosa.py`
- `src/orbitzoo/scripts/env_occupy_slots.py`
- `src/orbitzoo/scripts/env_rise_up_ddpg.py`
- `src/orbitzoo/scripts/env_rise_up_dqn.py`
- `src/orbitzoo/scripts/env_rise_up_ppo_cont.py`
- `src/orbitzoo/scripts/env_rise_up_ppo_disc.py`
- `src/orbitzoo/scripts/env_rise_up_td3.py`
- `src/orbitzoo/scripts/env_ruiz.py`
- `src/orbitzoo/scripts/mission_test_fedavg.py`
- `src/orbitzoo/scripts/mission_test_kolosa.py`
- `tests/test_interface_connections.py`
- `utils/col_avoidance.gif`
- `utils/dynamic_bodies.gif`
- `utils/hohmann.gif`
- `utils/hohmann1.png`
- `utils/hohmann2.png`
- `utils/marl.gif`
- `utils/orbitzoo_architecture.png`
- `utils/orbitzoo1.jpg`
- `utils/static_orbit.gif`
- `utils/tensorgator_ex1.png`
- `utils/tensorgator_ex2.png`

## Upstream files modified here

Ten upstream files carry local changes. Line counts ignore whitespace-only edits.

| File | Change | What was changed |
| --- | ---: | --- |
| `src/orbitzoo/rl_algorithms/mappo.py` | +475 −266 | Rewritten: typed `RolloutBatch`, restructured GAE and update loop, new checkpoint API (`checkpoint`, `from_checkpoint`, `load_actor`) |
| `src/orbitzoo/dynamics/orekit/main.py` | +25 −8 | Per-body finite-burn durations; covariance propagation made optional; orbit epoch corrected to the configured start time; state and covariance in float64 |
| `src/orbitzoo/__init__.py` | +13 −0 | Lazy `__getattr__` import of `OrbitZoo` |
| `src/orbitzoo/env.py` | +9 −3 | `maneuver_durations` threaded through `step()` |
| `src/orbitzoo/interface/main.py` | +6 −3 | Deep-merge of nested config defaults |
| `src/orbitzoo/dynamics/tensorgator/main.py` | +1 −1 | `maneuver_durations` added to the `step()` signature |
| `pyproject.toml` | — | Packaging, CLI entry point, tooling |
| `requirements.txt` | — | Added dependencies |
| `README.md` | — | Rewritten for this thesis |
| `.gitignore` | — | Added local artefact paths |

## Original to this thesis

Everything below is this project's own work.

| Area | Files | Contents |
| --- | ---: | --- |
| `src/orbitzoo/thesis/` | 51 | Collision-avoidance environment, scenario generator, maneuver contract, reward shaping, training curriculum, evaluation suite, scalability evaluator |
| `src/orbitzoo/cli/` | 12 | The `oz` command-line interface |
| `tests/` | 32 | Test suite, excluding `tests/test_interface_connections.py`, which is upstream |
| `docs/` | 15 | Thesis architecture, training trials, evaluation benchmark |
| `configs/` | 15 | Training, evaluation, and scenario configuration |
| `examples/`, `AGENTS.md`, `CLAUDE.md` | 3 | Usage example and agent guides |

No upstream file was deleted.
