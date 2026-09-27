# How v4 was trained

v4 was trained with MAPPO in three stages. The satellite count rises from stage to stage, and each stage starts from the previous stage's actor.

| Stage | Satellites | Updates | Entropy bonus | Scenarios |
|---|---:|---:|---:|---|
| 1 | 16 | 125 | 0.05 | mostly single debris threats |
| 2 | 64 | 110 | 0.01 | adds double threats and satellite pairs |
| 3 | 150 | 135 | 0.01 | same as stage 2 |

The final policy is the stage 3 checkpoint.

**Network:** the actor has 22 inputs, hidden layers of 128 and 64 units, and 7 outputs, about 11,700 weights in total. The critic (training only) has hidden layers of 256 and 128.

## Why stages

- **Learn to maneuver first.** Stage 1 is small and simple, and its higher entropy bonus pushes the policy to try burns rather than settle on never maneuvering.
- **Harder scenarios later.** Stages 2 and 3 add double threats and satellite pairs. Their lower entropy bonus cuts burns fired when no threat is present.
- **Fixed size per stage.** The critic's input grows with the number of satellites, so each stage keeps a fixed count and starts a new critic.
- **Cheaper to debug.** A stage 1 update takes about 25 s, against about 57 s at 150 satellites.

## Seed repeat

The whole curriculum was retrained from scratch with a second seed and evaluated on the same benchmark.

| Seed | Close approaches | Resolved |
|---|---:|---:|
| 42 (v4) | 7.45 | 92.6% |
| 7 | 7.05 | 93.0% |

The result does not depend on one lucky run. Differences smaller than the 0.40 gap between seeds are within training noise.

## Convergence

A run has converged when return stops rising and entropy stops falling.

| Stage | Satellites | Return gained | Entropy at end |
|---|---:|---:|---:|
| 1 | 16 | 15.99 | 0.119 |
| 2 | 64 | 0.92 | 0.094 |
| 3 | 150 | 0.19 | 0.069 |

- Stage 1 does almost all the learning. It settles at update 81 of 125.
- Stages 2 and 3 adapt the policy to more satellites rather than relearning.
- Stage 3 ends with a return of 12.91 and settles by update 12. Over its last quarter the return varies by about 5%, so the policy is stable.

## Runtime

Training ran on an Apple M1 MacBook Air (8 GB).

| Stage | Satellites | Median update | Wall clock |
|---|---:|---:|---:|
| 1 | 16 | 25.4 s | 53 min |
| 2 | 64 | 34.5 s | 64 min |
| 3 | 150 | 56.6 s | 2 h 7 min |

Total: 4 h 4 min. Runtime at deployment scale is in the scalability section.
