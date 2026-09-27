# Dataset

All orbital data are public Two-Line Element sets (TLEs) plus a metadata file per catalog. The catalogs are frozen snapshots and are not included in the repository; they are available from the team.

## Files

Each catalog is a pair:

- **TLE file:** two- or three-line TLE records.
- **Metadata CSV:** one row per object, with `norad_id`, `name`, `object_type` (payload, rocket body, debris, unknown), `is_agent_candidate`, `radius_meters` and `constellation`.

## The two catalogs

| | Frozen catalog | Full catalog |
|---|---:|---:|
| Objects | 20,000 | 24,922 |
| Payloads | 12,732 | 15,742 |
| Debris | 7,268 | 9,180 |
| Agent candidates | 349 | 15,742 (every payload) |
| TLE epochs (UTC) | 2026-09-01 to 2026-09-15 | 2026-08-16 to 2026-09-15 |
| Used by | Calibration, scalability | Training, evaluation benchmark |

5,000- and 10,000-object subsets of the frozen catalog were used to check that calibration gives the same answer at smaller sizes.

## Agent candidates (frozen catalog)

| Constellation | Candidates |
|---|---:|
| Starlink | 247 |
| Blank | 69 |
| OneWeb | 14 |
| Kuiper | 9 |
| Qianfan | 5 |
| Planet | 3 |
| Spire | 2 |

Space stations, docked vehicles and debris are never agents, but they stay in the catalog as threats.

## Object radii (frozen catalog)

| Radius | Objects |
|---:|---:|
| 0.1–0.4 m | 7,548 |
| 1.0 m | 29 |
| 1.5 m | 3,108 |
| 2.0 m | 9,315 |

Radii only decide whether a pass is a physical collision. They do not change the 1 km close-approach threshold.

## Filters

- **Low Earth orbit:** 200 to 2,000 km altitude at the start epoch.
- **TLE age:** at most 14 days older than the newest TLE in the catalog.
- **Co-location (scalability only):** keeps one object per group already within 1 km at epoch. It removes 16 objects (the ISS modules and docked vehicles), leaving 19,984.

## Propagation and units

- **Calibration and scalability:** SGP4 with WGS-72 in the TEME frame.
- **Training and evaluation:** satellites start from SGP4, are converted to the EME2000 frame, and are then flown by Orekit with J2.
- **Units:** SI throughout (metres, metres per second).

## Derived data

- **496 reference conjunctions.** Found by propagating the frozen catalog for 72 hours with no maneuvers. They set k, Δt and Δv, and their geometry shapes every generated threat.
- **Train/test split.** Satellites, background objects and close-call shapes are split 80/20 by a fixed hash of their ID. Training never sees the test 20%.

| Split | Satellites | Background objects | Close-call shapes |
|---|---:|---:|---:|
| Train | 12,569 | 7,197 | 397 |
| Test | 3,169 | 1,787 | 99 |

## How each experiment uses the data

| Experiment | Catalog | Satellites controlled | Threats |
|---|---|---|---|
| Calibration | Frozen, 72 h | 16, 64, 256 real candidates | Real, unmodified |
| Training | Full, train split | 16 → 64 → 150 | Generated on real close-call geometry |
| Evaluation benchmark | Full, test split | 150 | Generated on real close-call geometry |
| Scalability | Frozen, 6 h | 1,000–10,000 | Real, unmodified |
| 8× shell | Full | 10,000 | Real plus shifted copies of real satellites |

In the scalability sweep, 1,000 to 10,000 LEO payloads are drawn at random and treated as able to maneuver, whatever their real propulsion. It asks what would happen if every satellite ran the policy.
