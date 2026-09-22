# Heuristic collinear baseline

The traditional collision-avoidance strategy specified in the thesis methodology: a
fixed thrust along the satellite's orbital track once a conjunction crosses the risk
threshold. It is implemented as `collinear` in
[EVALUATION.md](../methods/EVALUATION.md) and measured here against the no-op reference, the
stronger six-direction rule, and the trained actor.

## Result

| Benchmark | Policy | Close approaches | Resolved | Closest (m) |
| --- | --- | ---: | ---: | ---: |
| Standard | No-op | 101.20 | — | 40.6 |
| | Collinear | 15.80 | 84.4% | 189.1 |
| | Rule | 10.40 | 89.7% | 206.9 |
| | **Actor** | **7.45** | **92.6%** | **249.6** |
| 100% multi-threat | No-op | 148.35 | — | 39.8 |
| | Collinear | 46.00 | 69.0% | 118.6 |
| | Rule | 33.15 | 77.7% | 156.2 |
| | **Actor** | **21.90** | **85.2%** | **165.2** |

150 agents, 20 held-out episodes. Paired against the collinear baseline, the actor
resolves 53% and 52% more conjunctions, winning 19 of 20 and 20 of 20 episodes
(p = 0.0001 and p = 0.00009). The six-direction rule also beats it, in 17 of 20 and
20 of 20 (p = 0.00023 and p = 0.00009).

## Restricting to the orbital track costs fuel rather than saving it

| Benchmark | Policy | Avoidance delta-v | Slot drift (m) | Return delta-v | **Total** |
| --- | --- | ---: | ---: | ---: | ---: |
| Standard | Collinear | 0.786 | 6,795 | 1.599 | **2.385** |
| | Rule | **0.670** | 3,632 | 0.726 | **1.396** |
| | Actor | 0.860 | 4,667 | 0.896 | **1.756** |
| 100% multi-threat | Collinear | 0.930 | 6,210 | 1.685 | **2.615** |
| | Rule | **0.810** | 3,601 | 0.774 | **1.584** |
| | Actor | 1.035 | 4,912 | 0.976 | **2.011** |

The collinear heuristic spends the most delta-v in total despite resolving the least.
An along-track burn changes the satellite's orbital period, so it walks away from its
assigned slot: 6,795 m of drift against the rule's 3,632 m. Returning costs more than
the avoidance did. Radial and cross-track separations change the miss distance without
that penalty, which is why the unrestricted rule is both safer and cheaper overall.

Against this baseline the actor is therefore **53% safer and 26% cheaper** in total
delta-v — it is not on the wrong side of a safety-fuel trade at all.

## At catalog scale

The same three policies on the real catalog, 19,984 objects over six hours
([SCALABILITY_RESULTS.md](SCALABILITY_RESULTS.md)):

| Agents | No-op | Collinear | Rule | Actor |
| ---: | ---: | ---: | ---: | ---: |
| 1,000 | 26 | 4 (84.6%) | **1 (96.2%)** | **1 (96.2%)** |
| 2,000 | 41 | 4 (90.2%) | **1 (97.6%)** | **1 (97.6%)** |
| 5,000 | 79 | 7 (91.1%) | **2 (97.5%)** | 3 (96.2%) |
| 10,000 | 118 | 10 (91.5%) | **5 (95.8%)** | 8 (93.2%) |

Collinear leaves the most conjunctions unresolved at every size. The rule is best on
real catalog conjunctions, which are almost all isolated and therefore the case it is
near-optimal for.

### The along-track penalty, isolated

At 10,000 agents:

| Policy | Maneuvers | Slot drift (m) | Avoidance delta-v | Return | **Total** |
| --- | ---: | ---: | ---: | ---: | ---: |
| Collinear | 217 | **355** | 0.0109 | 0.0370 | **0.0479** |
| Rule | 185 | **125** | **0.0093** | 0.0161 | **0.0254** |
| Actor | **336** | 161 | 0.0168 | 0.0207 | **0.0375** |

The actor makes 55% more burns than the collinear heuristic and drifts less than half
as far, because radial and cross-track separations do not change the orbital period
and along-track burns do. Collinear's drift is 2.8 times the rule's here, against 1.9
times at 150 agents, so the penalty grows with population.

Against the collinear heuristic the actor is therefore 20% safer and 22% cheaper in
total delta-v at 10,000 agents, the same direction as the 53% and 26% measured on the
benchmark. The margins are smaller because real catalog conjunctions are rarer and
develop more slowly than the generated ones.

## Why both classical baselines are reported

`collinear` is the strategy the methodology names, and it is the weaker comparison.
`rule` searches all six burn directions with the same curved J2 prediction and is
close to optimal for an isolated conjunction; it is the harder target and was built
deliberately as one.

Reporting both separates two claims that would otherwise be confused: that the learned
policy beats a traditional heuristic, which it does decisively, and that it edges a
near-optimal physics solver, which it does by a smaller margin that only appears where
threats overlap ([MULTITHREAT_BENCHMARK.md](MULTITHREAT_BENCHMARK.md)).

## Limitations

- **The direction along the track follows the geometry.** A strictly predetermined
  sign would fail roughly half of all encounters, so the implementation burns prograde
  or retrograde according to which widens the predicted miss. The constraint is to the
  along-track axis, which is what makes it collinear.
- **Same trigger as the rule.** Both act when the curved-orbit predicted miss is at or
  inside the 1 km safe separation, so the comparison isolates the choice of direction.
- **One scenario seed per benchmark**, 20 episodes each, and one draw per sweep point.
- **Absolute drift is small at catalog scale** because few of the 10,000 agents ever
  maneuver; the ratios between policies are the comparable quantity, not the metres.
