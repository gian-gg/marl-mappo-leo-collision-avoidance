"""Live threats, burns and close approaches for the viewer to highlight."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import numpy as np

NOMINAL = "nominal"
THREATENED = "threatened"
BURNING = "burning"
CLOSE_APPROACH = "close_approach"


@dataclass(frozen=True)
class Threat:
    """One predicted unsafe pair, controlled satellite first."""

    pair: tuple[str, str]
    predicted_miss_m: float
    time_to_closest_approach_s: float
    first_predicted_miss_m: float


class ThreatBoard:
    """Tracks what one episode's viewer shows, updated once per decision."""

    def __init__(self, agent_names: Iterable[str], decision_interval_seconds: float) -> None:
        self.agent_names = frozenset(agent_names)
        self.decision_interval_seconds = decision_interval_seconds
        self.decision = 0
        self.active: dict[frozenset[str], Threat] = {}
        self.burning: frozenset[str] = frozenset()
        self.recent_close_approaches: list[tuple[tuple[str, str], float]] = []
        self.close_approaches = 0
        self.closest_approach_m: float | None = None
        self.cleared = 0
        self._first_miss: dict[frozenset[str], float] = {}

    def _ordered(self, first: str, second: str) -> tuple[str, str]:
        if first in self.agent_names and second not in self.agent_names:
            return first, second
        if second in self.agent_names and first not in self.agent_names:
            return second, first
        return tuple(sorted((first, second)))

    def observe_assessments(self, assessments: Iterable[Mapping[str, Any]], collided: Iterable[Iterable[str]] = ()) -> None:
        """Replace the active threats, counting pairs cleared before their encounter."""
        active: dict[frozenset[str], Threat] = {}
        for item in assessments:
            pair = frozenset((item["first_name"], item["second_name"]))
            if not item["is_unsafe"] or not pair & self.agent_names:
                continue
            miss = float(item["predicted_miss_distance_meters"])
            first_miss = self._first_miss.setdefault(pair, miss)
            active[pair] = Threat(
                self._ordered(item["first_name"], item["second_name"]),
                miss,
                float(item["time_to_closest_approach_seconds"]),
                first_miss,
            )
        collided_pairs = {frozenset(pair) for pair in collided}
        self.cleared += sum(
            1
            for pair, threat in self.active.items()
            if pair not in active
            and pair not in collided_pairs
            and threat.time_to_closest_approach_s > self.decision_interval_seconds
        )
        self.active = active

    def begin_decision(self, agent_names: Iterable[str], actions: np.ndarray) -> None:
        """Mark the satellites that burn during the coming decision interval."""
        self.burning = frozenset(name for name, action in zip(agent_names, actions, strict=True) if action != 0)

    def observe_step(self, info: Mapping[str, Any]) -> None:
        """Record one environment step's outcome."""
        self.decision = int(info["step_index"])
        self.recent_close_approaches = [
            (self._ordered(*item["pair"]), float(item["miss_distance_meters"]))
            for item in info["close_approaches"]
            if set(item["pair"]) & self.agent_names
        ]
        self.close_approaches += len(self.recent_close_approaches)
        misses = [miss for _, miss in self.recent_close_approaches]
        if self.closest_approach_m is not None:
            misses.append(self.closest_approach_m)
        self.closest_approach_m = min(misses, default=None)
        self.observe_assessments(info["flagged_assessments"], info["collision_pairs"])

    def state_of(self, name: str) -> str:
        """The highlight for one body; close approaches outrank burns, burns outrank threats."""
        if any(name in pair for pair, _ in self.recent_close_approaches):
            return CLOSE_APPROACH
        if name in self.burning:
            return BURNING
        if any(name in pair for pair in self.active):
            return THREATENED
        return NOMINAL
