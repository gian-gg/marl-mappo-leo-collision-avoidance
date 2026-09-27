# Scenarios

Every episode is generated from its seed: real satellites on real orbits, facing close calls copied from the 496 real conjunctions found in calibration. The same seed always rebuilds the same episode.

## How an episode is built

1. Pick a random date within 72 hours of the catalog.
2. Fill the satellites with situations (table below).
3. For each threat, place it at a meeting point 6 to 16.5 minutes ahead (8 to 16.5 in evaluation) using a real close call's geometry, then fly it backwards to the start. If nobody maneuvers, the close call happens as planned.
4. Fill the remaining object slots with real debris from the catalog.

## Situations

| Situation | What happens | Right answer |
|---|---|---|
| Debris | One object on a collision course | Dodge |
| Satellite pair | Two controlled satellites on a collision course | One or both dodge |
| Double threat | Two objects, the second 1 to 4 min after the first | Dodge both |
| Harmless | An object passing 2 to 10 km away | Do nothing |
| Quiet | Nothing nearby | Do nothing |

Harmless and quiet teach the policy when not to burn.

| Situation | Stage 1 | Stages 2 and 3 |
|---|---:|---:|
| Debris | 50% | 30% |
| Satellite pair | — | 25% |
| Double threat | — | 15% |
| Harmless | 25% | 15% |
| Quiet | 25% | 15% |

## Train and test split

Satellites, background objects and close-call shapes are split 80/20 by ID. Training uses only the 80%, and evaluation uses only the 20%, so every evaluation episode is new to the policy.

| Split | Satellites | Background objects | Close-call shapes |
|---|---:|---:|---:|
| Train | 12,569 | 7,197 | 397 |
| Test | 3,169 | 1,787 | 99 |
