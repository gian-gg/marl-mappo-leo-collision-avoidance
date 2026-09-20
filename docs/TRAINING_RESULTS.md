# Training results

Second full run of the curriculum, with the settings adopted in trials 7 to 9, and its
evaluation against the baselines. Settings and their evidence are in
[TRAINING_TRIALS.md](TRAINING_TRIALS.md); scenarios are described in
[TRAINING_SCENARIOS.md](TRAINING_SCENARIOS.md).

## Headline result

One shared 22-input, 7-action actor of about 11,700 weights, trained once through the
16 → 64 → 150 agent curriculum, resolves **92% of the close approaches a coasting
constellation would suffer at 150 agents**, against 90% for a physics-based rule, and
keeps more than twice the rule's worst-case margin. It spends 39% more delta-v doing
so. No policy caused a collision at any size.

| Agents | No-op | Rule | Trained actor |
| ---: | ---: | ---: | ---: |
| 16 | 8.55 | 0.45 (94.7%) | 0.40 (95.3%) |
| 64 | 43.60 | 4.30 (90.1%) | **2.95 (93.2%)** |
| 150 | 101.20 | 10.40 (89.7%) | **7.95 (92.1%)** |

The margin over the rule widens with population, which is the behaviour the locality
argument predicts: a fixed `k = 1` neighbourhood loses nothing as the constellation
grows.

## Training run

Curriculum: `configs/mappo_stage{1,2,3}.json`, each stage starting from the previous
stage's actor, with a new critic each time since its input grows with the population.

| Stage | Agents / objects | Updates | Median update | Wall clock |
| ---: | --- | ---: | ---: | --- |
| 1 | 16 / 32 | 125 | 27.0 s | 18:10 → 19:06 |
| 2 | 64 / 128 | 110 | 36.3 s | 19:06 → 20:13 |
| 3 | 150 / 300 | 135 | 58.6 s | 20:13 → 22:25 |

Total 4 h 15 min on an Apple M1 MacBook Air (8 GB), no collisions in training. The
stage-2 checkpoint is bit-identical to the trial 9 validation run, which confirms that
a run is fully determined by its configuration and seed.

## Evaluation

`oz evaluate` on `configs/eval_stage{1,2,3}.json`, the frozen benchmark, 20 held-out
episodes per size (seeds 1,000,042–1,000,061). All policies play the same episodes;
the actor runs deterministically with no critic.

| Size | Policy | Close approaches | Closest (m) | Mean shortfall | Delta-v (m/s) | Slot drift (m) |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 16 | No-op | 8.55 | 41.0 | 0.395 | 0.000 | 1 |
| 16 | Rule | 0.45 | 653.2 | 0.033 | 0.533 | 3,103 |
| 16 | Actor | 0.40 | 653.2 | 0.035 | 0.945 | 5,398 |
| 64 | No-op | 43.60 | 40.2 | 0.385 | 0.000 | 1 |
| 64 | Rule | 4.30 | 289.1 | 0.169 | 0.676 | 3,681 |
| 64 | Actor | **2.95** | **420.0** | **0.132** | 0.941 | 5,115 |
| 150 | No-op | 101.20 | 40.6 | 0.378 | 0.000 | 1 |
| 150 | Rule | 10.40 | 206.9 | 0.217 | 0.670 | 3,632 |
| 150 | Actor | **7.95** | **422.9** | **0.170** | 0.928 | 5,113 |

Shortfall is how far inside the 1 km safe separation a close approach fell (0 at the
threshold, 1 at contact).

### Significance

Both policies played the same 20 episodes, so the comparison is paired.

| Size | Difference in close approaches | Wilcoxon p | Better / worse / tied |
| ---: | ---: | ---: | --- |
| 16 | −0.05 | 0.317 | 1 / 0 / 19 |
| 64 | −1.35 | **0.0035** | 14 / 3 / 3 |
| 150 | −2.45 | **0.0015** | 13 / 1 / 6 |

At 16 agents the rule is already near-perfect and the difference is not significant.
At 64 and 150 it is. These tests measure variation between episodes, not between
training seeds.

### Delta-v including the return to the slot

Station-keeping is out of scope for the policy, but the drift it causes is measured
and the minimum two-burn return is calculated.

| Size | Rule (avoid + return) | Actor (avoid + return) |
| ---: | ---: | ---: |
| 64 | 0.676 + 0.725 = **1.40** | 0.941 + 1.029 = 1.97 |
| 150 | 0.670 + 0.726 = **1.40** | 0.928 + 1.022 = 1.95 |

The actor is 39% more expensive in total. The first curriculum run was slightly
cheaper than the rule because its lower drift offset a higher avoidance burn; that
advantage is gone. Reducing delta-v is the main open task.

### Implicit coordination in satellite-to-satellite conjunctions

No satellite communicates or follows a priority rule. Each agent-agent conjunction is
classified by how many of its two satellites maneuvered.

| Size | Policy | Neither (resolved) | One (resolved) | Both (resolved) |
| ---: | --- | --- | --- | --- |
| 64 | Rule | 49 (48) | 0 (0) | 40 (40) |
| 64 | Actor | 54 (46) | **9 (9)** | **32 (32)** |
| 150 | Rule | 127 (126) | 0 (0) | 75 (72) |
| 150 | Actor | 155 (129) | **14 (14)** | **60 (60)** |

The rule always makes both satellites maneuver. The actor resolves every conjunction
in which one or both of its satellites maneuver — 32/32 and 60/60 when both act,
against the rule's 40/40 and 72/75 — which closes the paired-maneuver weakness of the
first curriculum run, where the same figures were 34/41 and 61/79.

The remaining weakness has moved: of the 155 conjunctions at 150 agents where neither
satellite maneuvered, 26 were not resolved. Those are conjunctions the actor chose to
coast through and should not have.

## Comparison with the first curriculum run

The first run, before trials 7 to 9, resolved 93% at 16 agents, 91% at 64 and 90% at
150, with 4.00 and 9.95 close approaches at the two larger sizes and a worst case of
183 m. It was cheaper: 1.34 and 1.35 m/s in total against the rule's 1.40. The three
settings changes bought safety and spent fuel.

## Reproducibility

```sh
runs/run_v2_curriculum.sh     # stage 1 -> 2 -> 3
.venv/bin/oz evaluate --config configs/eval_stage3.json \
  --policy noop --policy rule --policy v2=runs/v2_stage3/checkpoints/latest.pt \
  --episodes 20 --output runs/v2_eval_stage3
```

| Item | SHA-256 |
| --- | --- |
| `runs/v2_stage1/checkpoints/latest.pt` | `79fc35f5c23ffd1d8ec4d4c616f6aa4f5d15fdddbc51b312449763ecce1835d6` |
| `runs/v2_stage2/checkpoints/latest.pt` | `09f67424d3c57859de7b4eae96ccfffa49564e0c40cdbc3ebde38a73b9d45693` |
| `runs/v2_stage3/checkpoints/latest.pt` | `5540903e4a8d012d94ba35e23523ef2d1a91fa21fa86944bf7174291a59be5ef` |

Code revision `d010dd6`; seed 42; Python 3.11.4, NumPy 1.24.4, PyTorch 2.4.1;
macOS 26.0 on Apple M1.

## Limitations and open work

- **One seed.** Every number here comes from a single training run. The paired tests
  measure episode variance, not training variance. Seed repeats are needed before
  these results are reported as robust.
- **Delta-v.** The actor costs 39% more than the rule in total, at every size. This is
  the clearest open weakness and the next thing to address.
- **Coasted conjunctions.** At 150 agents, 26 of 155 conjunctions where neither
  satellite maneuvered went unresolved.
- **Twenty episodes per size.** More episodes would tighten the comparison.
- **Scale not yet measured.** The real-catalogue sweeps (`oz scale`, up to the full
  24,922-object catalogue and 10,000 agents) have not been run. They are the evidence
  for the scalability claim and require a machine other than the training laptop.
- **Avoidance only.** Returning to the nominal orbit is out of scope; drift and the
  calculated return cost are reported instead.
