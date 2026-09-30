"""Play one held-out episode with a trained policy in the headed OrbitZoo viewer."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import shutil
import subprocess
from typing import Any, Callable

import numpy as np
import pygame

from orbitzoo.thesis.config import ExperimentConfig
from orbitzoo.thesis.environments.collision_avoidance import CollisionAvoidanceEnv
from orbitzoo.thesis.environments.episodes import EpisodeSummary, play_episode
from orbitzoo.thesis.environments.scenarios import GeneratedEpisodeSource
from orbitzoo.thesis.evaluation.evaluator import evaluation_seeds, held_out
from orbitzoo.thesis.evaluation.policies import build_policy
from orbitzoo.thesis.visualization.board import BURNING, ThreatBoard
from orbitzoo.thesis.visualization.overlay import (
    OTHER_OBJECT_COLOR,
    STATE_COLORS,
    Overlay,
    Status,
    body_color,
)
from orbitzoo.thesis.visualization.playback import substep_dynamics

INTRO_SECONDS = 2.0
OUTRO_SECONDS = 3.0


@dataclass(frozen=True)
class WatchOptions:
    """How to play and optionally record the episode."""

    episode: int = 14
    substep_seconds: float = 10.0
    fps: int = 30
    record_directory: Path | None = None
    hold: bool = True


def interface_config() -> dict[str, Any]:
    """Viewer settings: dim Earth, no per-body labels, thrust arrows in the burn colour."""
    return {
        "zoom": 5.0,
        "background": {"color": (6, 8, 14)},
        "earth": {"show": True, "color": (40, 70, 140)},
        "timestamp": {"show": True, "size": 13},
        "bodies": {
            "show_label": False,
            "show_thrust": True,
            "color_body": OTHER_OBJECT_COLOR,
            "color_thrust": STATE_COLORS[BURNING],
        },
    }


class Player:
    """Renders the environment after every substep and optionally saves each frame."""

    def __init__(self, env: CollisionAvoidanceEnv, board: ThreatBoard, overlay: Overlay, options: WatchOptions) -> None:
        self.env = env
        self.board = board
        self.overlay = overlay
        self.options = options
        self.clock = pygame.time.Clock()
        self.frames = 0
        self.start_epoch = env.dynamics.current_epoch
        self.frame_directory = options.record_directory / "frames" if options.record_directory else None
        if self.frame_directory:
            self.frame_directory.mkdir(parents=True)

    def render(self, record: bool = True) -> None:
        interface = self.env.interface
        for sphere, body in zip(interface.spheres, interface.bodies, strict=True):
            sphere.color = body_color(self.board, body.name)
        delta_v = self.env.diagnostics.cumulative_delta_v_mps
        self.overlay.status = Status(
            decision=min(self.board.decision + 1, self.env.episode_horizon),
            horizon=self.env.episode_horizon,
            elapsed_seconds=self.env.dynamics.current_epoch.durationFrom(self.start_epoch),
            mean_delta_v_mps=float(np.mean(list(delta_v.values()))),
        )
        interface.frame(self.env.dynamics.current_epoch, overlay=self.overlay)
        if record and self.frame_directory:
            interface.save_screenshot(str(self.frame_directory / f"frame_{self.frames:05d}.png"))
            self.frames += 1
        self.clock.tick(self.options.fps)

    def pause(self, seconds: float) -> None:
        for _ in range(max(1, int(seconds * self.options.fps))):
            self.render()

    def hold(self) -> None:
        """Keep the final state on screen, with camera keys live, until the window is closed."""
        while True:
            self.render(record=False)

    def encode(self) -> Path | None:
        """Stitch the saved frames into an mp4 when ffmpeg is available."""
        if not self.frame_directory or not shutil.which("ffmpeg"):
            return None
        video = self.options.record_directory / "episode.mp4"
        subprocess.run(
            [
                "ffmpeg", "-loglevel", "error", "-framerate", str(self.options.fps),
                "-i", str(self.frame_directory / "frame_%05d.png"),
                "-pix_fmt", "yuv420p", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", str(video),
            ],
            check=True,
        )
        return video


def watch(
    config: ExperimentConfig,
    checkpoint: Path,
    options: WatchOptions,
    progress: Callable[[str], None] | None = None,
) -> EpisodeSummary:
    """Fly the checkpoint's policy through one held-out episode in the viewer."""
    if config.environment.scenario != "generated":
        raise ValueError("watch needs a config with the generated scenario")
    if options.episode < 0:
        raise ValueError("episode must be non-negative")
    if options.record_directory and options.record_directory.exists():
        raise FileExistsError(f"{options.record_directory} already exists")

    seed = evaluation_seeds(config, options.episode + 1)[options.episode]
    env = GeneratedEpisodeSource(held_out(config), interface_config()).environment(seed)
    policy = build_policy(f"v4={checkpoint}", config, env.local_observation_dim)
    board = ThreatBoard(env.agent_names, env.decision_interval_seconds)
    title = f"{policy.name} policy - held-out episode {options.episode}"
    others = len(env.interface.bodies) - env.num_agents
    subtitle = f"{env.num_agents} controlled satellites, {others} other objects"
    player = Player(env, board, Overlay(env.interface, board, title, subtitle), options)
    substep_dynamics(env.dynamics, options.substep_seconds, player.render)

    def choose(local: np.ndarray, _global: np.ndarray) -> np.ndarray:
        if env.step_index == 0:
            player.start_epoch = env.dynamics.current_epoch
            board.observe_assessments(asdict(item) for item in env.unsafe_assessments())
            player.pause(INTRO_SECONDS)
        actions = policy.choose(local)
        board.begin_decision(env.agent_names, actions)
        return actions

    def observe(_local: Any, _global: Any, _actions: Any, outputs: tuple) -> None:
        board.observe_step(outputs[-1])
        if progress:
            progress(
                f"decision {board.decision}/{env.episode_horizon}: {len(board.active)} active threats, "
                f"{board.close_approaches} close approaches"
            )

    summary = play_episode(env, seed, choose, observe_step=observe)
    board.burning = frozenset()
    player.pause(OUTRO_SECONDS)
    video = player.encode()
    if progress:
        closest = f"{summary.closest_approach_m:.1f} m" if summary.closest_approach_m is not None else "-"
        progress(
            f"episode done: {summary.close_approaches} close approaches, closest {closest}, {board.cleared} threats cleared, "
            f"delta-v {summary.mean_delta_v_per_agent_mps:.4f} m/s per satellite"
        )
        if video:
            progress(f"video: {video}")
    if options.hold:
        player.hold()
    return summary
