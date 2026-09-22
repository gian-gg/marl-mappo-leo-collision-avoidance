# Results

Every measured outcome in the project, and what each one establishes.

## Headline

A shared 22-input, 7-action actor of about 11,700 weights, flown by every satellite,
resolves **92.6% of the close approaches a coasting constellation would suffer** at 150
agents, against 89.7% for a near-optimal physics rule and 84.4% for the traditional
along-track heuristic. Its cost per satellite is constant to 10,000 agents. It spends
23–28% more delta-v than the rule, and about 26% less than the heuristic once the
return to the nominal slot is counted. No policy caused a collision in any run.

| Benchmark, 150 agents | Coasting | Collinear | Rule | **Actor** |
| --- | ---: | ---: | ---: | ---: |
| Close approaches per episode | 101.20 | 15.80 | 10.40 | **7.45** |
| Conjunctions resolved | — | 84.4% | 89.7% | **92.6%** |
| Closest approach (m) | 40.6 | 189.1 | 206.9 | **249.6** |
| Delta-v including return (m/s) | 0.00 | 2.39 | **1.40** | 1.76 |
| Collisions | 0 | 0 | 0 | 0 |

## What each study establishes

| Study | Finding |
| --- | --- |
| [K_DT_RESULTS.md](K_DT_RESULTS.md) | One ranked neighbour and a 120 s decision interval suffice, chosen on a 20,000-object, 72-hour run. |
| [MANEUVER_SIZING_RESULTS.md](MANEUVER_SIZING_RESULTS.md) | 0.5 m/s at 7 N clears 95% of reference conjunctions; the action size follows from measured warning times. |
| [TRAINING_TRIALS.md](TRAINING_TRIALS.md) | Ten settings experiments. The reward shaping must preview the penalties it stands in for, and the entropy bonus that rescues early training later causes burns fired at nothing. |
| [TRAINING_RESULTS.md](TRAINING_RESULTS.md) | The adopted curriculum, and a second training seed reaching 7.05 against 7.45 — the result reproduces. |
| [COLLINEAR_BASELINE.md](COLLINEAR_BASELINE.md) | Against the heuristic the methodology names, the actor is 53% safer and 26% cheaper. Along-track burns change the orbital period, so drift and the return burn dominate their cost. |
| [MULTITHREAT_BENCHMARK.md](MULTITHREAT_BENCHMARK.md) | The margin over the rule is entirely in simultaneous multi-threat, and grows with it: 2.9 points at 15% of the mix, 7.5 at 100%, winning 59 of 60 episodes. |
| [FUEL_TRADEOFF.md](FUEL_TRADEOFF.md) | Charging more for fuel removes the margin rather than the waste. The burns that look precautionary are the policy acting before a conjunction develops. |
| [SCALABILITY_RESULTS.md](SCALABILITY_RESULTS.md) | Cost per satellite is flat to 10,000 agents. On the real catalogue the actor ties the rule, because the encounters it is best at are rare there. |

## Two measurements about LEO itself

**Conjunction spacing follows orbital period, not density.** Projecting a shell to
eight times its population raises conjunctions thirty-fold and leaves the median gap
between a satellite's successive threats at 96 minutes — one revolution. Simultaneous
multi-threat cannot be reached by adding satellites to existing shells.
[SCALABILITY_RESULTS.md](SCALABILITY_RESULTS.md)

**The public catalogue lists docked structures as separate co-located objects.** The
ISS complex appears as seven objects sharing one position, producing 28 unavoidable
conjunctions at zero range. Any study using the catalogue for conjunction statistics
needs to collapse them; doing so moved the measured resolution rates from 74–77% to
93–98%. [SCALABILITY_RESULTS.md](SCALABILITY_RESULTS.md)

## What is not claimed

- The actor does **not** beat the rule on today's real catalogue. It ties, because
  isolated conjunctions dominate there and the rule is near-optimal for those.
- It is **not** more fuel-efficient than the rule. It spends 23–28% more, consistently.
- Collisions are zero under every policy including coasting, so the collision count
  does not discriminate between them. Close approaches under 1 km are the metric that
  does.
- Every number rests on **two training seeds** and one scenario seed per benchmark.
  Differences smaller than 0.40 close approaches per episode are inside the observed
  seed spread.
