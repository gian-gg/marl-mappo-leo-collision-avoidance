# Ablations

The thesis claims that a *locality-constrained* observation — one threat-ranked
neighbour — is what makes shared-policy collision avoidance learnable at constellation
scale. Two ablations test that claim by removing locality in the two directions it can
be removed: selecting the neighbour by proximity instead of predicted threat, and
removing selection entirely.

| Ablation | Change | Actor input |
| --- | --- | ---: |
| Fixed radius | Nearest objects within 1,000 km, `k = 4` | 67 |
| Global observability | Every moving body, no selection | 2,707 |
| **Control** | None; matches the ablations' training protocol | 22 |

## Why a control model

The adopted policy (v4) is trained on the 16 → 64 → 150 curriculum. The global
ablation cannot be, because its actor width scales with the population, so a 16-agent
stage produces a network of the wrong shape. It is instead trained at a fixed 150
agents in two phases.

Comparing an ablation trained one way against a policy trained another confounds the
ablation with the training protocol. **Control** removes that: it is the unmodified
threat-ranked encoder trained under the ablations' exact protocol — 150 agents,
two phases, same seed, same budget.

Control and v4 are statistically indistinguishable:

| Benchmark | v4 | Control | p |
| --- | ---: | ---: | ---: |
| Standard, 150 agents | 7.45 | 6.65 | 0.056 |
| Multi-threat, 100 agents | 21.90 | 20.45 | 0.096 |

The curriculum is therefore not what produces v4's result, and control is a fair
comparator for the ablations.

## Results

150 agents, 20 held-out episodes, `configs/eval_stage3.json` and the matching
`eval_radius.json` / `eval_global.json`. All policies see the same scenario seeds; the
identical no-op row across the three files confirms it.

| Policy | Close approaches | Resolved | Closest (m) | Delta-v | Unsafe steps |
| --- | ---: | ---: | ---: | ---: | ---: |
| Coasting | 101.20 | — | 40.6 | 0.000 | 423.3 |
| Collinear | 15.80 | 84.4% | 189.1 | 0.786 | 109.8 |
| Rule | 10.40 | 89.7% | 206.9 | 0.670 | 105.1 |
| v4 | 7.45 | 92.6% | 249.6 | 0.860 | 90.5 |
| **Control** | **6.65** | **93.4%** | 203.7 | 0.926 | 90.5 |
| Fixed radius | 93.70 | 7.4% | 40.7 | 0.322 | 403.7 |
| Global | 101.20 | 0.0% | 40.6 | 0.000 | 423.3 |

Multi-threat benchmark, double threats at 100% of the mix, 100 agents:

| Policy | Close approaches | Resolved | Delta-v | Unsafe steps |
| --- | ---: | ---: | ---: | ---: |
| Coasting | 148.35 | — | 0.000 | 369.5 |
| Collinear | 46.00 | 69.0% | 0.930 | 189.2 |
| Rule | 33.15 | 77.7% | 0.810 | 176.1 |
| v4 | 21.90 | 85.2% | 1.035 | 136.1 |
| **Control** | **20.45** | **86.2%** | 1.071 | 137.4 |
| Fixed radius | 136.95 | 7.7% | 0.322 | 354.6 |
| Global | 148.35 | 0.0% | 0.000 | 369.5 |

Both ablations lose to control and to v4 at p = 0.0001 on both benchmarks, paired
across the same 20 episodes.

## Fixed radius: proximity is the wrong selector

The radius ablation resolves 7.4% of what a coasting constellation suffers, against
control's 93.4%. It is closer to doing nothing than to avoiding anything, and it spends
a third of control's fuel doing it.

This is not an information deficit. The ablation carries **four** neighbour slots to
control's one, so its actor sees 67 inputs against 22. It has more of the wrong thing.

The cause is geometric. Across 750 agent-samples from five held-out episodes, the
object that the threat ranking selects is a median of **4,457 km away**, and is the
*nearest* object only 5.9% of the time. Its median rank by proximity is 29th.

| Property of the threat-ranked neighbour | Value |
| --- | ---: |
| Median separation | 4,457 km |
| Median rank by proximity | 29th |
| Is the nearest object | 5.9% |
| Falls inside the 1,000 km radius | **7.6%** |

That last figure is the ablation's result. The radius encoder can only act on a
conjunction whose counterpart happens to be inside its sphere, which is 7.6% of them —
and it resolves 7.4% on the standard benchmark and 7.7% under multi-threat. It is doing
about as well as a proximity selector can do, and that ceiling is low because in orbit
the object about to hit you is usually far away and closing fast, while the objects
beside you are co-moving and harmless.

## Global observability: trained, confident, and useless

The global ablation was trained twice. The first attempt did not learn at all; the
second was retuned and learned cleanly. Both evaluate identical to coasting.

### First attempt

Phase 1 never left its initialisation. Against a ceiling of ln 7 = 1.946, entropy
stayed between 1.93 and 1.80 for all 125 updates:

| Phase 1 update | Entropy | Delta-v | Return | Unsafe steps |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1.928 | 10.37 | −15.54 | 352 |
| 20 | 1.823 | 8.57 | −13.69 | 365 |
| 40 | 1.808 | 8.38 | −14.74 | 407 |
| 80 | 1.797 | 8.26 | −13.74 | 341 |
| 125 | 1.818 | 8.45 | −13.06 | 355 |

The policy was still choosing almost uniformly at random after 125 updates, still
burning 8.45 m/s per agent, and the return had moved 2.5 points in total. Phase 1
hyperparameters had been tuned for a 22-input actor; applied to a 2,707-input one,
where the first layer holds about 346,000 weights instead of 2,800, the entropy bonus
dominated the task gradient and the policy never committed.

That is a failure to train, not a finding, and it is not reported as one.

### Second attempt

Entropy coefficient 0.05 → 0.01 in phase 1 and 0.01 → 0.003 in phase 2, with the
phase-1 actor learning rate raised 1e-4 → 3e-4. Architecture, rewards, seed and update
budget unchanged. `configs/mappo_global2_phase{1,2}.json`.

| Phase 1 update | Entropy | Delta-v | Return | Unsafe steps |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1.918 | 10.37 | −15.54 | 352 |
| 20 | 1.118 | 3.62 | −10.05 | 392 |
| 40 | 0.471 | 1.22 | −9.94 | 436 |
| 80 | 0.233 | 0.50 | −8.53 | 409 |
| 125 | 0.353 | 0.80 | −8.14 | 400 |
| Phase 2, 245 | 0.126 | 0.23 | −7.72 | 458 |

Both attempts share a seed, so they begin from the same place — update 1 is delta-v
10.37, return −15.54, 352 unsafe steps in each. From there they diverge completely.
Entropy collapses, delta-v falls from 10.37 to 0.80, and the return improves
monotonically from −15.54 to −8.14. The optimiser worked.

### What it learned

The last column is the finding. Unsafe agent-steps go from 352 to 400 while the return
improves — slightly *worse* than where it started, and worse still by the end of phase
2. The entire return improvement came from cutting the fuel bill, not from avoiding
anything. The policy learned that burning costs delta-v and does not help, and stopped
burning.

At update 1, before it had learned anything, it was burning 10.37 m/s per agent —
twelve times what v4 spends — essentially at random. That bought 352 unsafe steps
against coasting's 423: a 17% reduction. Control, with a tenth of the fuel and 22
inputs, reaches 90.5: a 79% reduction.

Undirected manoeuvring buys 17%. One chosen neighbour buys 79%. The skill is not
acting; it is knowing which object to act on.

### Both checkpoints evaluate as coasting

| Checkpoint | Entropy at save | Training delta-v | Evaluated delta-v | Close approaches |
| --- | ---: | ---: | ---: | ---: |
| Phase 1 | 0.353 | 0.80 | 0.000 | 101.20 |
| Phase 2 | 0.126 | 0.23 | 0.000 | 101.20 |

Evaluation takes the greedy action, so a delta-v of exactly 0.000 means the argmax is
`NO_OP` in every state on every episode. The checkpoints are not broken: under
sampling they do fire thrusters, which is where the training delta-v comes from. Their
*mode* is always to do nothing.

The phase-1 checkpoint was evaluated separately to rule out the objection that the
result is only a late-training collapse. It is not — the mode is `NO_OP` at entropy
0.353 as well.

## What is not claimed

- The global result rests on **one retuning attempt**, not a hyperparameter sweep. The
  claim is that global observability does not learn under settings that train the
  local encoder well, and does not learn after the one adjustment its failure mode
  indicated. It is not a proof that no configuration could.
- Each ablation was trained with **one seed**. Differences smaller than 0.40 close
  approaches per episode are inside the observed seed spread — which does not affect
  either conclusion here, since both gaps exceed 85 close approaches.
- The radius ablation used 1,000 km and `k = 4`. A different radius would give a
  different number; the claim is about the selector, not the threshold.

## Reproducing

```
scripts/run_ablations.sh radius
scripts/run_ablations.sh control
scripts/run_ablations.sh global
scripts/run_global2.sh
```
