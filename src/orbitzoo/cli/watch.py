"""Watch a trained policy fly one held-out episode in the OrbitZoo viewer."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def run_watch(args: argparse.Namespace) -> None:
    from orbitzoo.thesis.config import ExperimentConfig
    from orbitzoo.thesis.visualization.watch import WatchOptions, watch

    options = WatchOptions(
        episode=args.episode,
        substep_seconds=args.substep,
        fps=args.fps,
        record_directory=Path(args.record).expanduser() if args.record else None,
        hold=not args.no_hold,
    )
    try:
        watch(
            ExperimentConfig.load(Path(args.config).expanduser()),
            Path(args.checkpoint).expanduser(),
            options,
            progress=lambda message: print(message, file=sys.stderr, flush=True),
        )
    except Exception as error:
        raise SystemExit(f"oz: watch failed: {error}") from error


def add_watch_parser(subparsers: argparse._SubParsersAction) -> None:
    command = subparsers.add_parser(
        "watch",
        help="fly a trained policy through one held-out episode in the 3D viewer",
    )
    command.add_argument(
        "--config",
        default="configs/eval_stage3.json",
        help="experiment configuration path (default: %(default)s)",
    )
    command.add_argument(
        "--checkpoint",
        default="runs/v4_stage3/checkpoints/latest.pt",
        help="MAPPO checkpoint to fly (default: %(default)s)",
    )
    command.add_argument(
        "--episode",
        type=int,
        default=14,
        help="held-out episode index, as in oz evaluate (default: %(default)s)",
    )
    command.add_argument(
        "--substep",
        type=float,
        default=10.0,
        help="seconds of simulated time per rendered frame (default: %(default)s)",
    )
    command.add_argument("--fps", type=int, default=30, help="frame-rate cap and video rate (default: %(default)s)")
    command.add_argument("--record", help="new directory for PNG frames and episode.mp4")
    command.add_argument("--no-hold", action="store_true", help="close the window when the episode ends")
    command.set_defaults(handler=run_watch)
