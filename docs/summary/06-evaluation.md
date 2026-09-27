# How v4 was evaluated

All policies play the same 20 held-out episodes with 150 satellites. Nothing is learned during evaluation.

There are two benchmarks:

- **Standard** uses the same scenario mix as training: single debris, satellite pairs, quiet stretches, and 15% double threats. It tests normal operation.
- **Multi-threat** makes double threats (two objects closing on one satellite at once) as common as possible, about half of all satellites. It tests the hardest case, where dodging one threat can push the satellite into the other.

Metrics:

- **Close approaches:** passes where a satellite came within 1 km of another object, averaged per episode. Lower is better.
- **Resolved:** the share of no-op's close approaches that the policy avoided, `1 − policy / no-op`. Higher is better.
- **Closest pass:** the smallest miss distance seen in any of the 20 episodes, i.e. the worst case. Higher is better.

## Safety

| Benchmark | Policy | Close approaches | Resolved | Closest pass (m) |
|---|---|---:|---:|---:|
| Standard | No-op | 101.20 | — | 40.6 |
| | Collinear | 15.80 | 84.4% | 189.1 |
| | Fixed radius | 93.70 | 7.4% | 40.7 |
| | Global | 101.20 | 0.0% | 40.6 |
| | v4 | 7.45 | 92.6% | 249.6 |
| Multi-threat | No-op | 148.35 | — | 39.8 |
| | Collinear | 46.00 | 69.0% | 118.6 |
| | Fixed radius | 136.95 | 7.7% | 28.3 |
| | Global | 148.35 | 0.0% | 39.8 |
| | v4 | 21.90 | 85.2% | 165.2 |

v4 beat collinear in 19 of 20 standard episodes and all 20 multi-threat episodes. Both ablations lose to v4 on both benchmarks.

## Fuel (standard, delta-v in m/s per agent)

| Policy | Avoidance | Return to slot | Total |
|---|---:|---:|---:|
| Collinear | 0.786 | 1.599 | 2.385 |
| Fixed radius | 0.322 | 0.174 | 0.496 |
| Global | 0.000 | 0.000 | 0.000 |
| v4 | 0.860 | 0.896 | 1.756 |

Burning along the track changes the orbital period, so collinear drifts further from its slot, and getting back costs more than the dodge did. The ablations are cheap only because they barely act.

## Coordination

Satellites never communicate and follow no priority rule. Each satellite-to-satellite conjunction is sorted by how many of its two satellites maneuvered (150 satellites, standard benchmark).

| Who maneuvered | Conjunctions | Resolved |
|---|---:|---:|
| Neither | 142 | 127 |
| One | 2 | 2 |
| Both | 72 | 71 |

When satellites act, they almost always clear each other without dodging into each other. The misses are mostly cases where neither moved.

## Multi-threat sweep

The share of double threats was raised step by step from the standard 15% to the maximum.

| Double threats | 15% | 40% | 70% | 100% |
|---|---:|---:|---:|---:|
| v4 resolved | 92.6% | 88.7% | 89.2% | 85.2% |

v4 loses only about 7 points going from the normal mix to the hardest one. A second training seed gives the same numbers within 0.4 points.

## Fuel trade-off

To see whether v4 could burn less, the whole curriculum was retrained with a higher fuel penalty.

| Variant | Fuel penalty | Close approaches | Resolved | Delta-v (m/s) |
|---|---:|---:|---:|---:|
| v4 | 1 | 7.45 | 92.6% | 0.860 |
| fuel2 | 2 | 8.40 | 91.7% | 0.804 |
| fuel4 | 4 | 13.45 | 86.7% | 0.783 |
| fuel8 | 8 | 52.05 | 48.6% | 0.513 |

Charging more for fuel saves little and costs a lot of safety. About a quarter of v4's burns happen before a threat is flagged, acting early, and a higher penalty removes exactly those. v4's penalty was kept.

**Result:** v4 is about 53% safer than collinear and 26% cheaper in total fuel. Fixed radius and global are close to doing nothing.
