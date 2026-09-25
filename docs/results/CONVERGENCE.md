# Policy convergence

Convergence is one of the five evaluation measures the methodology names. It asks
whether the shared policy stabilises into a consistent strategy, and is read from the
episode return, the action-distribution entropy, and the variance of both once training
settles.

Convergence is measured here for the adopted policy and for every variant, because the
comparison turns out to separate two failures that look alike from the outside: a
variant that never converged, and a variant that converged on doing nothing.

## Summary

Every run below finishes at 150 agents. Returns are comparable across runs because the
reward function, agent count and scenario distribution are identical; only the
observation differs. "Gain" is the improvement from the first five updates to the last
ten, and "settled at" is the update where a trailing ten-update mean first reaches 95%
of that gain.

| Final stage | Return start | Return end | Gain | SD, last quarter | Entropy end | Settled at |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **v4 stage 3** | 12.72 | **12.91** | 0.19 | 0.68 | 0.069 | 12 |
| **Control phase 2** | 11.64 | **12.51** | 0.87 | 0.76 | 0.064 | 35 |
| Radius stage 3 | −14.63 | −14.93 | −0.29 | 0.94 | 0.533 | 10 |
| Global, attempt 1 | −13.76 | −12.46 | 1.30 | 0.93 | **1.817** | 26 |
| Global, attempt 2, phase 2 | −7.83 | −7.42 | 0.40 | 0.89 | 0.175 | 27 |

The adopted policy and its control converge to a **positive** return near +12.5 with
entropy below 0.07. Every variant converges — or fails to — below −7.

## The adopted policy

The curriculum's first stage carries the learning. Stage 1 gains 15.99 return points
over 125 updates and settles at update 81; stages 2 and 3 gain 0.92 and 0.19, which is
what warm-starting is supposed to look like — each later stage inherits a working
policy and adapts it to a larger population rather than relearning.

| Stage | Agents | Updates | Gain | Entropy end |
| --- | ---: | ---: | ---: | ---: |
| 1 | 16 | 125 | 15.99 | 0.119 |
| 2 | 64 | 110 | 0.92 | 0.094 |
| 3 | 150 | 135 | 0.19 | 0.069 |

Entropy falls monotonically across the curriculum and the final-quarter standard
deviation is 0.68 return points against a mean of 12.91, about 5%. The policy is
stable, not still moving.

Control reaches the same place by a different route — one 150-agent stage of 125
updates plus one of 245 — ending at 12.51 with entropy 0.064. Two training protocols,
the same convergence behaviour, which is the evidence that the curriculum is a
convenience rather than the cause. See [ABLATIONS.md](ABLATIONS.md).

## Convergence is not competence

The two ablations both converge by the usual test — entropy falls, return flattens,
variance is no larger than the adopted policy's — and both converge to something
useless.

**Fixed radius** settles fastest of any run, at update 10 of its final stage, and
settles at −14.93. Its final stage gains nothing at all: −0.29, i.e. it ends slightly
below where it started. Its entropy also stops falling, at 0.533 against the adopted
policy's 0.069 — an order of magnitude more uncertain. A policy whose observation
rarely contains the object that matters cannot become confident about what to do, and
the entropy floor is that fact showing up in the training trace.

**Global observability, attempt 2** converges cleanly: entropy 1.918 → 0.175, return
−14.21 → −7.42, settled by update 27 of phase 2. On every conventional convergence
criterion this is a successful training run. Its policy manoeuvres in 0% of evaluation
states.

The measure therefore discriminates in one direction only. Failure to converge predicts
a useless policy — attempt 1 ended at entropy 1.817, barely below the uniform ceiling of
ln 7 = 1.946, and was useless. But convergence predicts nothing: attempt 2 converged and
was equally useless. Reported alone, convergence would have called the global variant a
success.

## What the returns do not tell you

Return is not a safety metric here, and two runs make that concrete.

Radius ends at −14.93 and global at −7.42, so by return the global variant looks
markedly better. By safety it is strictly worse: radius resolves 7.4% of the no-op
close approaches and global resolves 0%. The gap is fuel. Radius spends 1.91 m/s per
agent during training against global's 0.41, and the delta-v penalty charges it for
every burn whether or not the burn helped.

A variant can improve its return by manoeuvring less, which is exactly what the global
variant learned to do. Convergence and return therefore need to be read alongside the
close-approach counts in [ABLATIONS.md](ABLATIONS.md), never instead of them.

## Sources

Per-update training traces, `metrics.csv` in each run directory:
`v4_stage{1,2,3}`, `control_phase{1,2}`, `radius_stage{1,2,3}`,
`global_phase1` (attempt 1), `global2_phase{1,2}` (attempt 2).
