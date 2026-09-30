# Visualization

`oz watch` flies a trained checkpoint through one held-out evaluation episode in the
headed OrbitZoo viewer.

```sh
.venv/bin/oz watch                       # v4, held-out episode 14, live window
.venv/bin/oz watch --episode 3           # another held-out episode
.venv/bin/oz watch --record runs/watch_ep14 --no-hold   # PNG frames + episode.mp4
```

Defaults: `configs/eval_stage3.json`, `runs/v4_stage3/checkpoints/latest.pt`,
episode 14. `--episode N` is the same index as row N of an `oz evaluate` run with that
config, so the seed is `config.seed + 1_000_000 + N`. Episode 14 (seed 1000056) is the
default because it has the largest drop in close approaches: 99 for no-op against 2 for v4.

With `--record`, frames go to `<dir>/frames/` and `<dir>/episode.mp4` is stitched with
ffmpeg when it is on `PATH`. The directory must not exist. Headless recording works with
`SDL_VIDEODRIVER=dummy`.

## What is on screen

| Mark | Meaning |
| --- | --- |
| pale blue dot | controlled satellite, nothing to do |
| grey dot | other object (debris, uncontrolled satellite) |
| amber ring + line | unsafe pair: predicted miss under the 1 km safe separation within the screening horizon; the line joins the two bodies |
| green ring, green arrow | satellite burning during this decision interval |
| red ring + line | close approach under 1 km realized during the last decision interval |

The panel shows the decision, elapsed time, mean delta-v per satellite, close approaches
and closest pass (same definitions as `episodes.csv`), threats cleared, satellites
burning, and the six tightest active threats with predicted miss and minutes to closest
approach. Only satellites in a threat are labelled.

"Threats cleared" is a viewer tally: an unsafe pair involving a controlled satellite that
stops being unsafe while its closest approach was still more than one decision interval
away, and did not collide. It uses the same rule as the evaluation's pair resolution, but
counts satellite–debris pairs too, so it is not the coordination metric.

Camera keys are OrbitZoo's: `w`/`s` zoom, `a`/`d` and arrows pan, `q`/`e` and `r`/`t`
rotate. After the episode the window stays open until closed, unless `--no-hold`.

## Playback substeps

The environment propagates each 120 s decision in one Orekit call. For smooth motion,
`oz watch` wraps `dynamics.step` so each decision is propagated in pieces of
`--substep` seconds (default 10) and a frame is drawn after each piece. The policy,
observations, rewards and safety screen still run once per decision, unchanged.

Every burn is kept whole in the first piece, which is stretched to the longest burn
(about 21 s at 0.5 m/s and 7 N). Splitting a finite burn across propagation calls loses
all but the last piece of it: a 21.4 s burn cut at 10 s delivered 0.033 m/s instead of
0.5 m/s, and the episode no longer matched evaluation. With burns kept whole, episode 14
reproduces the evaluation row: 2 close approaches, closest 894.1 m, 0.877 m/s per
satellite.

## Scope

The viewer draws every body each frame, so it suits the 150-satellite evaluation setting.
The 1k–10k satellite [scalability](SCALABILITY.md) runs are reported as tables and plots,
not in the viewer.
