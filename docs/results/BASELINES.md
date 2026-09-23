# Baseline comparison

The three policies named in the thesis methodology, measured on the same episodes and
the same catalog: the no-maneuver control, the heuristic collinear maneuver, and the
trained shared actor.

| Policy | What it does |
| --- | --- |
| No-maneuver | Never burns. Establishes the collision risk the environment carries. |
| Collinear | Thrusts along the orbital track when the predicted miss reaches the 1 km safe separation. Prograde or retrograde according to which widens the miss; no other direction is available to it. |
| Actor | The trained shared policy. 22 inputs, 7 actions, about 11,700 weights, run deterministically with no critic. |

A fourth policy, `rule`, searches all six burn directions with the same prediction and
is close to optimal for an isolated conjunction. It is reported separately in
[COLLINEAR_BASELINE.md](COLLINEAR_BASELINE.md) as the harder comparison.

## Held-out benchmark, 150 agents

20 episodes, `configs/eval_stage3.json`, generated from satellites never used in
training.

| Metric | No-maneuver | Collinear | **Actor** |
| --- | ---: | ---: | ---: |
| Close approaches per episode | 101.20 | 15.80 | **7.45** |
| Conjunctions resolved | — | 84.4% | **92.6%** |
| Closest approach (m) | 40.6 | 189.1 | **249.6** |
| Mean shortfall | 0.378 | 0.223 | **0.177** |
| Unsafe agent-steps | 423.25 | 109.80 | **90.50** |
| Collisions | 0 | 0 | 0 |
| Avoidance delta-v (m/s) | 0.000 | **0.786** | 0.860 |
| Slot drift (m) | 1 | 6,795 | **4,667** |
| Return delta-v (m/s) | 0.000 | 1.599 | **0.896** |
| **Total delta-v (m/s)** | 0.000 | 2.385 | **1.756** |

The actor resolves **53% fewer** close approaches than the collinear heuristic for
**26% less** total delta-v, winning 19 of 20 episodes (Wilcoxon p = 0.00010). It is
also the steadier of the two: standard deviation 2.33 against 4.47 per episode.

## Stress test: every encounter a double threat

Same benchmark with the scenario mix shifted so simultaneous double threats are 100%
of the weight ([MULTITHREAT_BENCHMARK.md](MULTITHREAT_BENCHMARK.md)).

| Metric | No-maneuver | Collinear | **Actor** |
| --- | ---: | ---: | ---: |
| Close approaches per episode | 148.35 | 46.00 | **21.90** |
| Conjunctions resolved | — | 69.0% | **85.2%** |
| Closest approach (m) | 39.8 | 118.6 | **165.2** |
| Unsafe agent-steps | 369.50 | 189.15 | **136.05** |
| Avoidance delta-v (m/s) | 0.000 | **0.930** | 1.035 |
| Slot drift (m) | 1 | 6,210 | **4,912** |
| **Total delta-v (m/s)** | 0.000 | 2.615 | **2.011** |

The actor resolves **52% fewer** close approaches for **23% less** total delta-v, and
wins **all 20 episodes** (p = 0.00009). The collinear heuristic degrades further than
the actor as threats overlap: 84.4% to 69.0%, against 92.6% to 85.2%.

## Catalog scale

The real catalog, 19,984 objects, six hours, agents drawn from the LEO payloads
([SCALABILITY_RESULTS.md](SCALABILITY_RESULTS.md)).

| Agents | No-maneuver | Collinear | **Actor** |
| ---: | ---: | ---: | ---: |
| 1,000 | 26 | 4 (84.6%) | **1 (96.2%)** |
| 2,000 | 41 | 4 (90.2%) | **1 (97.6%)** |
| 5,000 | 79 | 7 (91.1%) | **3 (96.2%)** |
| 10,000 | 118 | 10 (91.5%) | **8 (93.2%)** |

Conjunctions remaining and the share of the no-maneuver total resolved. No collisions
under any policy at any size. The closest approach anything reached while coasting was
100 m, so the collision count does not separate these policies; conjunctions inside
1 km is the metric that does.

### Cost at 10,000 agents

| Policy | Maneuvers | Avoidance | Slot drift (m) | Return | **Total** |
| --- | ---: | ---: | ---: | ---: | ---: |
| No-maneuver | 0 | 0.0000 | 0 | 0.0000 | **0.0000** |
| Collinear | 217 | 0.0109 | 355 | 0.0370 | **0.0479** |
| **Actor** | 336 | 0.0168 | **161** | **0.0207** | **0.0375** |

The actor makes **55% more burns and drifts less than half as far**. Along-track
thrust changes the orbital period, so every collinear maneuver walks the satellite out
of its slot and the station-keeping burn to return costs more than the avoidance did.
Radial and cross-track separations widen the miss without that penalty.

Against the collinear heuristic the actor is **20% safer and 22% cheaper** at 10,000
agents — the same direction as the benchmark, with smaller margins because real
catalog conjunctions are rarer and develop more slowly than generated ones.

### Compute

| Agents | No-maneuver | Collinear | Actor | Actor per agent |
| ---: | ---: | ---: | ---: | ---: |
| 1,000 | 1.086 | 1.024 | 0.998 | 0.998 ms |
| 2,000 | 1.868 | 1.860 | 1.866 | 0.933 ms |
| 5,000 | 4.447 | 5.195 | 6.181 | 1.236 ms |
| 10,000 | 13.930 | 11.141 | 8.987 | **0.899 ms** |

Seconds per decision step. Cost per agent is flat from 1,000 to 10,000 and the actor
is no more expensive than doing nothing — its network inference is about 2% of the
total, the rest being propagation and the neighbour search that every policy needs.
The variation across policies at a given size is machine noise; these runs shared the
node with another user.

## Summary

| Claim | Evidence |
| --- | --- |
| Safer than no-maneuver | 101.20 to 7.45 close approaches at 150 agents; 118 to 8 at 10,000 |
| Safer than the collinear heuristic | 53% fewer on the benchmark, 52% under stress, 20% at 10,000 agents |
| Cheaper than the collinear heuristic | 26%, 23% and 22% less total delta-v |
| Advantage grows as encounters overlap | 84.4% to 69.0% for collinear against 92.6% to 85.2% for the actor |
| Constant cost per satellite | 0.998 ms at 1,000 agents, 0.899 ms at 10,000 |

## Limitations

- **Two training seeds.** Seeds 42 and 7 give 7.45 and 7.05 close approaches at 150
  agents. Differences under 0.40 per episode are inside that spread.
- **One scenario seed per benchmark**, 20 episodes each, and one draw per sweep point.
- **The catalog sweep has no held-out split**, so it includes satellites the policy
  trained against; the 150-agent benchmark is the clean generalisation test.
- **The 1 km threshold is a convention.** Miss distance and shortfall are reported
  alongside the counts because a pass at 999 m scores as a failure and one at 1,001 m
  does not.
- **Collisions do not discriminate.** Zero under every policy including no-maneuver,
  because this catalog over six hours contains no contact trajectories.
