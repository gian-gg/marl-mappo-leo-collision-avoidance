# Calibration

Before training, three values were fixed from orbital data rather than tuned on the policy:

- **k:** how many neighbours each satellite sees.
- **Δt:** how often each satellite makes a decision.
- **Δv:** how big each burn is.

## k and Δt

The real catalog (20,000 objects) was propagated for 72 hours with no maneuvers. Close passes under 1 km (496 of them) were the threats to catch. Each pair of k and Δt was scored on:

- **Recall:** is the real threat among the k neighbours shown? Must be at least 99.9%.
- **Timely:** is it shown at least 3 decisions before closest approach? Must be at least 99%.

The rule is to pick the smallest k that passes, then the largest Δt at that k.

| k | Δt | Recall | Timely | Pass |
|---:|---:|---:|---:|:---:|
| 1 | 60 s | 100% | 99.8% | yes |
| 1 | **120 s** | **100%** | **99.5%** | **yes** |
| 1 | 300 s | 99.6% | 78.3% | no |
| 1 | 600 s | 97.5% | 0.4% | no |

**Result:** k = 1, Δt = 120 s. One well-ranked neighbour catches every threat, and deciding every 2 minutes leaves enough time to react. Smaller catalogs (5,000 and 10,000 objects) picked the same pair.

## Δv

Using the same 496 threats, each candidate burn size was tested with the satellite burning at every decision from first detection until closest approach. The rule is to pick the smallest Δv that clears at least 95% of threats.

| Δv per burn | 0.1 | 0.2 | **0.5** | 1 | 2 |
|---|---:|---:|---:|---:|---:|
| Resolved | 50.0% | 79.0% | **96.6%** | 98.6% | 99.4% |

**Result:** 0.5 m/s per burn. Most threats appear about 15 minutes before closest approach, which leaves several decisions to burn in. Finishing a 0.5 m/s burn within 60 s needs about 7 N of thrust for an 800 kg satellite.
