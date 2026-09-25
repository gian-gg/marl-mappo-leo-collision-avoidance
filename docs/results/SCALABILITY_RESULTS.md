# Scalability results

The frozen actor run at catalog scale against the no-op and rule baselines, and what
the sweeps measured about LEO itself. The evaluator is described in
[SCALABILITY.md](../methods/SCALABILITY.md); the policy is the one adopted in
[TRAINING_RESULTS.md](TRAINING_RESULTS.md).

## Headline result

At 10,000 maneuvering satellites in the real catalog, the learned policy matches a
physics-based rule on safety and costs the same per satellite as doing nothing.

| Agents | No-op | Collinear | Rule | v4 | seed 7 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 26 | 4 (84.6%) | 1 (96.2%) | 1 (96.2%) | 1 (96.2%) |
| 2,000 | 41 | 4 (90.2%) | 1 (97.6%) | 1 (97.6%) | 1 (97.6%) |
| 5,000 | 79 | 7 (91.1%) | 2 (97.5%) | 3 (96.2%) | 3 (96.2%) |
| 10,000 | 118 | 10 (91.5%) | 5 (95.8%) | 8 (93.2%) | 6 (94.9%) |

Conjunctions remaining, and the share of the no-op total resolved. 19,984 objects,
6 hours, 1 km safe separation. No collisions under any policy at any size.

The rule ends 1–3 conjunctions ahead at the two largest sizes. Two training seeds of
the same configuration differ by 2 at 10,000 agents, so that margin is the size of
the seed-to-seed spread and is not evidence of a real difference.

## Compute scales linearly in agents

| Agents | Seconds per decision | Per agent |
| ---: | ---: | ---: |
| 1,000 | 1.004 | 1.004 ms |
| 2,000 | 1.863 | 0.931 ms |
| 5,000 | 4.402 | 0.880 ms |
| 10,000 | 8.687 | **0.869 ms** |

Ten times the agents costs 8.7 times the wall clock, so the per-agent cost is flat
and slightly falling. This is the locality argument measured rather than asserted: a
`k = 1` neighborhood means each satellite does constant work however large the
constellation grows.

The actor's own inference is about 2% of that cost. At 10,000 agents the policy runs
in 8.839 s per decision against the no-op reference's 8.944 s — within noise of doing
nothing at all.

## The fixed-radius variant scales, costs more, and resolves almost nothing

The radius ablation was swept over the same catalog and agent ladders, with its own
no-op reference (`configs/scalability_radius.json`, `k = 4`, 1,000 km).

| Agents | Conjunctions | Radius resolves | v4 resolves |
| ---: | ---: | ---: | ---: |
| 1,000 | 26 | 5 (19.2%) | **25 (96.2%)** |
| 2,000 | 41 | 6 (14.6%) | **40 (97.6%)** |
| 5,000 | 79 | 11 (13.9%) | **76 (96.2%)** |
| 10,000 | 118 | 15 (12.7%) | **111 (94.1%)** |

19,984 objects, 6 hours. Across the catalog sweep at 349 maneuvering satellites the
radius variant resolves **zero** conjunctions at every size while still spending
delta-v, where v4 resolves all of them.

The benchmark result therefore holds at catalog scale: proximity selection resolves
roughly an eighth of what threat ranking resolves, and the share falls as the
constellation grows.

### It is 1.7 times more expensive per decision

| Agents | v4, `k = 1` | Radius, `k = 4` | Ratio |
| ---: | ---: | ---: | ---: |
| 1,000 | 1.004 s | 1.694 s | 1.69 |
| 2,000 | 1.863 s | 3.041 s | 1.63 |
| 5,000 | 4.402 s | 7.521 s | 1.71 |
| 10,000 | 8.687 s | 15.172 s | **1.75** |

The cost is the encoder, not the policy: the no-op rows carry the same ratio, 8.703 s
against 14.952 s at 10,000 agents, because both sweeps encode observations before any
policy is consulted. Per-agent observation cost is 849 µs at `k = 1` and 1,484 µs at
`k = 4`.

Four slots cost 1.7 times one slot rather than four times, because the pairwise
screening that precedes selection is shared across slots and does not depend on `k`.
The extra cost is the per-neighbour encoding alone.

### Scalability is not what this ablation refutes

Per-agent observation cost is flat across the ladder — 1,456, 1,397, 1,444, 1,484 µs
from 1,000 to 10,000 agents — so the radius variant scales as well as the adopted
policy does. Any fixed-size neighbourhood does, whichever rule fills it.

The fixed-radius ablation therefore does not fail on scalability. It fails on
effectiveness, at a 1.7x runtime premium. The scalability half of the locality argument
rests on the global variant below, not on this one.

## Global observability cannot be deployed at another size

The global-observability variant is absent from every table above, and not by omission.
Its actor consumes one block per moving body, so its input width is `7 + 9n` rather than
the `7 + 15k` of a locality-constrained actor. A policy trained at 150 agents has 2,707
inputs and cannot be loaded against a 1,000-object catalog at all: the first layer is the
wrong shape.

Scalability testing deploys a *frozen* policy at increasing sizes without retraining. A
variant whose parameters depend on the population fails that test by construction, before
any runtime is measured. Retraining it per size would also be self-defeating — the first
layer alone holds about 346,000 weights at 150 agents and would hold 23 million at 10,000.

This is the scalability half of the locality argument, and it is structural rather than
empirical. The safety half — that the variant does not learn to avoid anything even at a
fixed size — is in [ABLATIONS.md](ABLATIONS.md).

## Co-located catalog objects

The first sweep reported 159 collisions. All of them were the ISS: Zarya, Unity,
Zvezda, Destiny, Poisk and the docked Crew Dragon and Cygnus vehicles are catalogued
as separate objects that share one position. Seven objects give 21 mutual pairs, each
reporting a conjunction at zero range and zero time-to-closest-approach that no
maneuver could avoid.

`ScalabilityConfig.colocation_separation_meters` (default 1 km) now keeps one object
per co-located group at epoch. It removes 16 of 20,000 objects and takes the reported
collisions to zero. It also raised both policies from an apparent 74–77% of
conjunctions resolved to 93–98%, since the unavoidable pairs had been counted as
failures for every policy.

Any study using the public catalog for conjunction statistics needs this filter.

## Conjunction spacing is set by orbital period, not density

The policy's advantage over the rule is in simultaneous multi-threat encounters, and
grows with their density — see [MULTITHREAT_BENCHMARK.md](MULTITHREAT_BENCHMARK.md).
The sweeps measured how often that situation actually arises.

In the real catalog at 10,000 agents, 86% of the satellites involved in a conjunction
face exactly one, and successive threats to the same satellite are a median of 94
minutes apart.

To test whether density changes this, the 500–600 km shell was projected forward to
eight times its population by adding phase- and plane-shifted copies of real
satellites (`density_multiplier`, see [SCALABILITY.md](../methods/SCALABILITY.md)). That raised
conjunctions thirty-fold and left the timing untouched:

| | Real catalog | Shell at 8x density |
| --- | ---: | ---: |
| Conjunctions at 10,000 agents | 118 | 3,545 |
| Satellites facing two or more | 14% | 47% |
| Median gap between successive threats | 94 min | **96 min** |
| Two threats within one 30-minute screening horizon | 12% | **14%** |
| Two threats within one 120 s decision step | — | 1% |

The 96-minute median is one orbital period. Conjunctions occur where orbits cross,
and a satellite returns to those crossings once per revolution, so adding satellites
adds crossings without moving them closer together in time.

Simultaneous multi-threat is therefore rare in LEO at any density that can be reached
by populating existing shells. The encounter the policy handles best is one the
environment seldom presents.

## Satellite-to-satellite conjunctions

Conjunctions between two maneuvering satellites, at 10,000 agents in the real catalog:

| Policy | Both maneuvered | Resolved |
| --- | ---: | ---: |
| Rule | 32 | 28 (87.5%) |
| v4 | 33 | 30 (90.9%) |
| seed 7 | 36 | 32 (88.9%) |

Both policies edge the rule in the case it cannot reason about, since it has no
representation of the other satellite also maneuvering. The sample is 32–36 pairs and
the margin is one to two conjunctions, so nothing can be concluded from it.

Repeating the measurement in the projected shell, where 97% of objects are payloads
and 3,545 conjunctions occur, settles it:

| Policy | Both maneuvered | Resolved | 95% CI |
| --- | ---: | ---: | --- |
| Rule | 500 | 470 (94.0%) | [91.7%, 95.8%] |
| Seed 42 | 515 | 482 (93.6%) | [91.2%, 95.5%] |
| Seed 7 | 553 | 522 (94.4%) | [92.2%, 96.1%] |

Fisher's exact test gives p = 0.80 against the rule for both seeds, and p = 0.61
between the two seeds. At a sample fifteen times larger the intervals overlap almost
entirely: **the policy neither beats nor trails the rule on satellite-to-satellite
coordination.** The apparent edge at 32 pairs was noise.

## Fuel

The policy is consistently the more expensive of the two, and the collinear heuristic
is the most expensive of the three. At 10,000 agents on the real catalog:

| Policy | Maneuvers | Slot drift (m) | Avoidance | Return | **Total** |
| --- | ---: | ---: | ---: | ---: | ---: |
| Collinear | 217 | **355** | 0.0109 | 0.0370 | **0.0479** |
| Rule | 185 | **125** | **0.0093** | 0.0161 | **0.0254** |
| v4 | **336** | 161 | 0.0168 | 0.0207 | **0.0375** |

The actor makes 55% more burns than the collinear heuristic yet drifts less than half
as far: along-track thrust changes the orbital period, radial and cross-track
separations do not. Collinear's drift is 2.8 times the rule's at 10,000 agents against
1.9 times at 150, so the penalty grows with population. See
[COLLINEAR_BASELINE.md](COLLINEAR_BASELINE.md).

| Population | Policy | Maneuvers | Delta-v per agent | Burns per conjunction resolved |
| --- | --- | ---: | ---: | ---: |
| Real catalog, 10,000 agents | Rule | 185 | 0.0093 | **1.64** |
| | Seed 42 | 336 | 0.0168 | 3.05 |
| | Seed 7 | 427 | 0.0214 | 3.81 |
| Projected shell, 10,000 agents | Rule | 4,004 | 0.2002 | **1.17** |
| | Seed 42 | 6,172 | 0.3086 | 1.82 |
| | Seed 7 | 8,058 | 0.4029 | 2.35 |

The rule is about twice as efficient per conjunction resolved, and the gap is wider at
catalog scale than the 26% measured on the 150-agent benchmark. Seed 7 burns twice as
often as the rule and ends with 117 conjunctions against its 122, a difference that is
not statistically distinguishable. This is the clearest and most consistent difference
between the two policies, and it favours the rule.

## Reproducing

```sh
.venv/bin/oz scale --config configs/scalability.json \
  --policy rule --policy v4=runs/v4_stage3/checkpoints/latest.pt \
  --policy seed7=runs/seed7_stage3/checkpoints/latest.pt \
  --sweep both --output runs/scale_final
```

Artifacts: `runs/scale_v4_filtered` (real catalog), `runs/scale_collinear` (real
catalog with both classical baselines), `runs/shell_probe` (projected shell, no-op
reference) and `runs/shell_pairs` (projected shell, all policies). Run on an NVIDIA GB10 Grace Blackwell node, 20 Arm cores, Python 3.11.16.

## Limitations

- **One scenario seed.** Every sweep point is a single draw of the population and of
  the encounters it produces. There are no error bars on a conjunction count, so
  differences of one to three conjunctions cannot be resolved.
- **Six hours.** A longer horizon would raise the counts and tighten the comparison.
- **No held-out split.** The sweep draws agents from the whole catalog, so it includes
  satellites the policy trained against. The generated benchmark splits satellites
  80/20 by hashed identifier and is the clean generalisation test; this sweep measures
  behaviour and cost at population.
- **Synthetic density.** The projected shell keeps each template's inclination,
  eccentricity and mean motion and varies only plane and phase. It emulates a denser
  population, not any specific planned constellation.
- **The 1 km threshold is a convention.** A pass at 999 m counts as a failure and one
  at 1,001 m as a success; two of the policy's three extra failures at 10,000 agents
  missed by 3 m and 1 m. Miss distance and shortfall are reported alongside counts for
  this reason.
