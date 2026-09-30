"""Split each decision's propagation into short substeps so the viewer moves smoothly.

See docs/methods/VISUALIZATION.md.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Mapping

COAST = [0.0, 0.0, 0.0]


def burn_schedule(
    step_size: float, substep_seconds: float, durations: Mapping[str, float]
) -> list[tuple[float, dict[str, float]]]:
    """Substeps covering ``step_size``; the first holds every burn whole, the rest coast in equal pieces."""
    if step_size <= 0 or substep_seconds <= 0:
        raise ValueError("step_size and substep_seconds must be positive")
    first = min(max(substep_seconds, *durations.values(), 0.0), step_size)
    remaining = step_size - first
    count = math.ceil(remaining / substep_seconds - 1e-9) if remaining > 1e-9 else 0
    schedule = [(first, dict(durations))]
    schedule += [(remaining / count, dict.fromkeys(durations, 0.0)) for _ in range(count)]
    return schedule


def substep_dynamics(dynamics: Any, substep_seconds: float, on_substep: Callable[[], None]) -> None:
    """Replace ``dynamics.step`` so every call propagates in substeps and calls ``on_substep`` after each."""
    propagate = dynamics.step

    def step(
        step_size: float | None = None,
        actions: dict[str, list[float]] | None = None,
        maneuver_durations: dict[str, float] | None = None,
    ) -> None:
        step_size = float(step_size) if step_size else float(dynamics.step_size)
        actions = actions or {}
        durations = {name: (maneuver_durations or {}).get(name, step_size) for name in actions}
        for dt, burns in burn_schedule(step_size, substep_seconds, durations):
            propagate(
                dt,
                {name: thrust if burns[name] > 0 else COAST for name, thrust in actions.items()},
                burns,
            )
            on_substep()

    dynamics.step = step
