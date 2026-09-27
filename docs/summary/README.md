# Summary

- **v4**, one small shared policy that sees only its most threatening neighbour, avoids 92.6% of close approaches at 150 satellites, against 84.4% for the traditional collinear maneuver, while using 26% less total fuel.
- Trained at 150 satellites, it runs unchanged at 10,000 on the real catalog with no collisions, and its cost per satellite stays flat.
- Picking neighbours by distance, or showing the policy everything, makes it fail. Locality is what makes it work.

## Reading order

| File | Covers |
|---|---|
| [00-calibration](00-calibration.md) | choosing k, Δt and Δv |
| [01-environment](01-environment.md) | what the policy sees, does and is rewarded for |
| [02-scenarios](02-scenarios.md) | how episodes are built, train/test split |
| [03-training](03-training.md) | the curriculum, network, seed repeat |
| [04-baselines](04-baselines.md) | no-op, collinear, fixed radius, global |
| [05-ablations](05-ablations.md) | how the ablations were trained and why they fail |
| [06-evaluation](06-evaluation.md) | safety, fuel, coordination, multi-threat, fuel trade-off |
| [07-scalability](07-scalability.md) | real catalog up to 10,000 satellites, denser orbits |
| [08-limitations](08-limitations.md) | what the results do not show |
