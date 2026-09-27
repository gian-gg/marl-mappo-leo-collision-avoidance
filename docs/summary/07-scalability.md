# How v4 scales

The frozen v4 policy, trained at 150 satellites, runs on the real space catalog with no retraining: 19,984 objects, 1,000 to 10,000 of them controlled satellites, over 6 hours.

Global observability is left out. Its input size is fixed to the 150 satellites it was trained on, so it cannot run at any other size.

## Safety (conjunctions left, share of no-op's avoided)

| Satellites | No-op | Collinear | Fixed radius | v4 |
|---:|---:|---:|---:|---:|
| 1,000 | 26 | 4 (84.6%) | 21 (19.2%) | 1 (96.2%) |
| 2,000 | 41 | 4 (90.2%) | 35 (14.6%) | 1 (97.6%) |
| 5,000 | 79 | 7 (91.1%) | 70 (11.4%) | 3 (96.2%) |
| 10,000 | 118 | 10 (91.5%) | 103 (12.7%) | 8 (93.2%) |

The share is net: a conjunction a policy's own burn creates counts against it. No collisions under any policy at any size.

## Compute (seconds per decision, per-satellite cost in brackets)

| Satellites | v4 | Fixed radius |
|---:|---:|---:|
| 1,000 | 1.0 (1.00 ms) | 1.7 (1.69 ms) |
| 10,000 | 8.7 (0.87 ms) | 15.2 (1.52 ms) |

Both stay flat per satellite, because each looks at a fixed number of neighbours. Fixed radius costs about 1.7 times as much, because it encodes 4 neighbours instead of 1.

## Fuel at 10,000 satellites (delta-v in m/s per agent)

| Policy | Slot drift (m) | Total |
|---|---:|---:|
| Collinear | 355 | 0.0479 |
| Fixed radius | 101 | 0.0711 |
| v4 | 161 | 0.0375 |

## Denser orbits (8× shell)

To test a more crowded future, the 500–600 km shell was filled to 8 times its real population with shifted copies of real satellites.

| | Real catalog | 8× shell |
|---|---:|---:|
| Conjunctions at 10,000 satellites | 118 | 3,545 |
| Satellites facing two or more | 14% | 47% |
| Median gap between threats to one satellite | 94 min | 96 min |

Crowding adds far more conjunctions but does not bunch them together. Threats to the same satellite stay about one orbit apart, so overlapping threats, where v4 does best, remain rare in LEO.

**Result:** v4 works at 10,000 satellites without retraining, beats collinear at every size, and uses about 22% less fuel. Fixed radius scales but avoids little, and it costs more fuel than v4 while doing so.

**Caveat:** each size is a single run, so differences of 1 to 3 conjunctions are not meaningful.
