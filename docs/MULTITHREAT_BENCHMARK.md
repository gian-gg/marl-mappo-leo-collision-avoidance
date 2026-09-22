# Multi-threat benchmark

The trained policy resolves 89% of simultaneous double threats against the rule's 80%
on the standard benchmark, where they are 15% of the mix
([TRAINING_RESULTS.md](TRAINING_RESULTS.md)). This benchmark raises that share to
measure how the advantage depends on it.

## Headline result

The margin over the rule grows with the density of simultaneous threats, and the
policy wins in 59 of 60 episodes.

| Double threats in the mix | Rule | Seed 42 | Seed 7 | Margin |
| ---: | ---: | ---: | ---: | ---: |
| 15% (standard benchmark) | 89.7% | 92.6% | 93.0% | +2.9 |
| 40% | 83.3% | 88.7% | 88.8% | **+5.4** |
| 70% | 83.0% | 89.2% | 89.2% | **+6.2** |
| 100% | 77.7% | 85.2% | 85.2% | **+7.5** |

Share of the no-op close approaches resolved, 150 agents, 20 held-out episodes.

## Method

`configs/eval_multithreat_{40,70,100}.json` are the frozen stage-3 benchmark with the
scenario weights shifted toward `double_threat`; quiet and harmless situations shrink
first, then debris and satellite pairs. Everything else is unchanged, so the
comparison is against the same satellites, the same held-out split, and the same 20
seeds.

The episode's object budget caps the achievable share. Each double threat consumes
two non-agent objects, and a 150-agent episode holds 300 bodies, so the `100%` weight
yields 75 agents facing simultaneous double threats and 75 quiet ones. Half of all
agents under simultaneous attack is the maximum this environment can present.

```sh
.venv/bin/oz evaluate --config configs/eval_multithreat_100.json \
  --policy noop --policy rule \
  --policy v4=runs/v4_stage3/checkpoints/latest.pt \
  --policy seed7=runs/seed7_stage3/checkpoints/latest.pt \
  --episodes 20 --output runs/mt_eval_100
```

## Significance

Both policies play the same episodes as the rule, so the comparison is paired.

| Mix | Rule | Seed 42 | Difference | Wilcoxon p | Episodes better |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 40% | 25.50 | 17.25 | −8.25 | 0.00009 | 20 / 20 |
| 70% | 30.10 | 19.15 | −10.95 | 0.00013 | 19 / 20 |
| 100% | 33.15 | 21.90 | −11.25 | 0.00009 | 20 / 20 |

The two training seeds agree to within 0.1 percentage points at every rung — 88.7 and
88.8, 89.2 and 89.2, 85.2 and 85.2. Elsewhere in this project the seed spread is the
limit on what can be resolved; here it is far smaller than the margin, so a five to
seven point gap is not a training artifact.

## Why the policy is ahead

The rule reconstructs its top-ranked threat, predicts the closest approach along
curved J2 orbits, and picks whichever of the six burns most widens that miss. For an
isolated conjunction the answer is close to optimal, which is why the two policies tie
when threats arrive alone.

It has no representation of a second threat. A burn that is optimal against the first
can close the miss on the second, and the rule cannot see that happen.

The actor reads the same single neighbour — the same 22 inputs, no extra information —
and its advantage is entirely in this case. It was never given the second threat and
never told one exists; the training reward penalises realized close approaches, so
burns that traded one conjunction for another were punished, and what it learned is a
choice of direction that tolerates a threat it cannot see.

## Cost

| Mix | Rule delta-v | Actor delta-v | Penalty |
| ---: | ---: | ---: | ---: |
| 40% | 0.924 | 1.183 | +28% |
| 70% | 1.058 | 1.306 | +23% |
| 100% | 0.810 | 1.035 | +28% |

The fuel penalty is steady across the ladder and matches the figure measured
elsewhere; it does not grow as the benefit grows.

## Against the collinear heuristic

At 100% double threats the traditional along-track baseline resolves 69.0% against the
actor's 85.2%, losing all 20 episodes (p = 0.00009), and spends more total delta-v
doing it. See [COLLINEAR_BASELINE.md](COLLINEAR_BASELINE.md).

## Fuel variants under stress

Raising `delta_v_penalty_per_mps` removes the margin
([FUEL_TRADEOFF.md](FUEL_TRADEOFF.md)):

| Penalty | Close approaches | Margin over the rule |
| ---: | ---: | ---: |
| 1.0 (adopted) | 21.90 | **+7.6 pt** |
| 2.0 | 24.85 | +5.6 pt |
| 4.0 | 30.45 | +1.8 pt |
| 8.0 | 80.90 | −32.2 pt |

The margin depends on burns the cheaper-fuel policies stop making.

## How often this regime occurs

Simultaneous multi-threat is rare in LEO today. In the real catalog at 10,000
maneuvering satellites, 86% of the satellites involved in a conjunction face exactly
one, and successive threats to the same satellite arrive a median of 94 minutes apart.
Projecting a shell to eight times its population raises the conjunction count
thirty-fold and leaves that spacing at 96 minutes, because conjunctions occur where
orbits cross and a satellite returns to its crossings once per revolution. See
[SCALABILITY_RESULTS.md](SCALABILITY_RESULTS.md).

This benchmark is therefore a designed stress test, not a projection. It measures the
size of the advantage; the scalability results measure how often the environment asks
for it.

## Limitations

- **Constructed, not observed.** The scenario generator places the second threat 60 to
  240 seconds after the first. Real successive threats are 96 minutes apart.
- **Budget-capped.** Half of all agents is the highest simultaneous-threat share a
  300-body episode can present.
- **One scenario seed per rung.** Twenty episodes each, drawn once. The paired tests
  measure variation between episodes, not between scenario draws.
- **Two training seeds.** Enough to show the margin is not a training artifact, not
  enough for a confidence interval on its size.
