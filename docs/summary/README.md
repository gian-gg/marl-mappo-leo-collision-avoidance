# Summary

- **v4**, one small shared policy that sees only its most threatening neighbour, avoids 92.6% of close approaches at 150 satellites, against 84.4% for the traditional collinear maneuver, while using 26% less total fuel.
- Trained at 150 satellites, it runs unchanged at 10,000 on the real catalog with no collisions, and its cost per satellite stays flat.
- Picking neighbours by distance, or showing the policy everything, makes it fail. Locality is what makes it work.

## Reading order

| File | Covers |
|---|---|
| [00-dataset](00-dataset.md) | the catalogs, filters, split, and how each experiment uses them |
| [01-calibration](01-calibration.md) | choosing k, Δt and Δv |
| [02-environment](02-environment.md) | agent architecture, what the policy sees, does and is rewarded for |
| [03-scenarios](03-scenarios.md) | how episodes are built, train/test split |
| [04-training](04-training.md) | the curriculum, network, seed repeat, convergence, runtime |
| [05-hyperparameters](05-hyperparameters.md) | MAPPO, per-stage and reward settings |
| [06-baselines](06-baselines.md) | no-op, collinear, fixed radius, global |
| [07-ablations](07-ablations.md) | how the ablations were trained and why they fail |
| [08-evaluation](08-evaluation.md) | safety and significance, fuel, coordination, multi-threat, fuel trade-off |
| [09-scalability](09-scalability.md) | real catalog up to 10,000 satellites, denser orbits |
| [10-limitations](10-limitations.md) | what the results do not show |
