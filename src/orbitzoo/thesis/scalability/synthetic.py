"""Project a catalog forward to a denser constellation by adding shifted copies of real satellites.

See docs/methods/SCALABILITY.md.
"""

from __future__ import annotations

import dataclasses

import numpy as np

from orbitzoo.thesis.calibration.models import CatalogObject, ObjectType

SYNTHETIC_ID_BASE = 900_000


def tle_checksum(line: str) -> int:
    """Modulo-10 sum of the digits, counting each minus sign as one."""
    return sum(int(char) if char.isdigit() else 1 if char == "-" else 0 for char in line[:68]) % 10


def shift_elements(line2: str, raan_degrees: float, anomaly_degrees: float) -> str:
    """Return line 2 with its right ascension and mean anomaly rotated, checksum rebuilt."""
    raan = (float(line2[17:25]) + raan_degrees) % 360.0
    anomaly = (float(line2[43:51]) + anomaly_degrees) % 360.0
    body = f"{line2[:17]}{raan:8.4f}{line2[25:43]}{anomaly:8.4f}{line2[51:68]}"
    return f"{body}{tle_checksum(body)}"


def densify(
    objects: tuple[CatalogObject, ...],
    multiplier: int,
    seed: int,
) -> tuple[CatalogObject, ...]:
    """Add ``multiplier - 1`` copies of every payload, spread over planes and phases.

    Copies keep their template's inclination, eccentricity and mean motion, so they occupy the
    same shell, and differ only in orbital plane and position within it.
    """
    if multiplier <= 1:
        return objects
    templates = [item for item in objects if item.object_type is ObjectType.PAYLOAD]
    if not templates:
        raise ValueError("densify needs at least one payload to copy")
    rng = np.random.default_rng([seed, 2])
    copies: list[CatalogObject] = []
    for index, template in enumerate(templates):
        for step in range(1, multiplier):
            fraction = step / multiplier
            raan = 360.0 * fraction + float(rng.uniform(-5.0, 5.0))
            anomaly = 360.0 * ((index * 0.618 + fraction) % 1.0) + float(rng.uniform(-5.0, 5.0))
            copies.append(
                dataclasses.replace(
                    template,
                    norad_id=SYNTHETIC_ID_BASE + len(copies),
                    name=f"{template.name} COPY {step}",
                    line2=shift_elements(template.line2, raan, anomaly),
                    is_agent_candidate=True,
                    has_metadata=False,
                )
            )
    return tuple(sorted(objects + tuple(copies), key=lambda item: item.norad_id))
