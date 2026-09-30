"""Threat lines, highlights and the status panel drawn over the OrbitZoo scene."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pygame
import play3d.three_d as three_d

from orbitzoo.thesis.visualization.board import BURNING, CLOSE_APPROACH, NOMINAL, THREATENED, ThreatBoard

SATELLITE_COLOR = (150, 170, 210)
OTHER_OBJECT_COLOR = (95, 95, 105)
STATE_COLORS = {
    THREATENED: (255, 176, 0),
    BURNING: (70, 230, 120),
    CLOSE_APPROACH: (255, 70, 70),
}
TEXT_COLOR = (232, 232, 238)
MUTED_COLOR = (150, 150, 162)
PANEL_COLOR = (8, 10, 16, 210)
PANEL_WIDTH = 430
MARGIN = 12
LISTED_THREATS = 6
NAME_WIDTH = 14


@dataclass(frozen=True)
class Status:
    """Episode progress shown in the panel."""

    decision: int
    horizon: int
    elapsed_seconds: float
    mean_delta_v_mps: float


def body_color(board: ThreatBoard, name: str) -> tuple[int, int, int]:
    """Viewer colour for one body."""
    state = board.state_of(name)
    if state != NOMINAL:
        return STATE_COLORS[state]
    return SATELLITE_COLOR if name in board.agent_names else OTHER_OBJECT_COLOR


class Overlay:
    """Draws the current board onto the viewer's screen; called by ``Interface.frame``."""

    def __init__(self, interface: Any, board: ThreatBoard, title: str, subtitle: str) -> None:
        self.interface = interface
        self.board = board
        self.title = title
        self.subtitle = subtitle
        self.status: Status | None = None
        self.index = {body.name: i for i, body in enumerate(interface.bodies)}
        self.title_font = pygame.font.SysFont("Menlo", 17, bold=True)
        self.font = pygame.font.SysFont("Menlo", 14)
        self.small_font = pygame.font.SysFont("Menlo", 11)

    def _project(self, name: str, view_projection: Any) -> tuple[int, int]:
        i = self.index[name]
        position = self.interface.bodies[i].position * self.interface.distance_scale
        x, y = self.interface._project_to_screen(*position, self.interface.spheres[i], view_projection)
        return int(x), int(y)

    def __call__(self, screen: pygame.Surface) -> None:
        view_projection = three_d.Camera.View_Projection_matrix()
        self._draw_pairs(screen, view_projection)
        self._draw_highlights(screen, view_projection)
        self._draw_panel(screen)
        self._draw_legend(screen)

    def _draw_pairs(self, screen: pygame.Surface, view_projection: Any) -> None:
        for threat in self.board.active.values():
            start, end = (self._project(name, view_projection) for name in threat.pair)
            pygame.draw.line(screen, STATE_COLORS[THREATENED], start, end, 1)
        for pair, _ in self.board.recent_close_approaches:
            start, end = (self._project(name, view_projection) for name in pair)
            pygame.draw.line(screen, STATE_COLORS[CLOSE_APPROACH], start, end, 2)

    def _draw_highlights(self, screen: pygame.Surface, view_projection: Any) -> None:
        in_threat = {name for pair in self.board.active for name in pair}
        in_threat |= {name for pair, _ in self.board.recent_close_approaches for name in pair}
        for name in self.index:
            state = self.board.state_of(name)
            if state == NOMINAL:
                if name in self.board.agent_names:
                    pygame.draw.circle(screen, SATELLITE_COLOR, self._project(name, view_projection), 2)
                continue
            center = self._project(name, view_projection)
            pygame.draw.circle(screen, STATE_COLORS[state], center, 5, 2)
            if name in self.board.agent_names and name in in_threat:
                label = self.small_font.render(name, True, STATE_COLORS[state])
                screen.blit(label, label.get_rect(midbottom=(center[0], center[1] - 7)))

    def _panel_lines(self) -> list[tuple[str, tuple[int, int, int]]]:
        board, status = self.board, self.status
        closest = f"{board.closest_approach_m:,.0f} m" if board.closest_approach_m is not None else "-"
        lines = [(self.subtitle, MUTED_COLOR)]
        if status:
            minutes, seconds = divmod(int(status.elapsed_seconds), 60)
            lines += [
                (f"Decision {status.decision:>2} / {status.horizon}   T+{minutes:02d}:{seconds:02d}", TEXT_COLOR),
                (f"Delta-v per satellite  {status.mean_delta_v_mps:.3f} m/s", TEXT_COLOR),
            ]
        lines += [
            (f"Close approaches <1 km {board.close_approaches:>5}", STATE_COLORS[CLOSE_APPROACH]),
            (f"Closest pass           {closest:>9}", TEXT_COLOR),
            (f"Threats cleared        {board.cleared:>5}", STATE_COLORS[BURNING]),
            (f"Satellites burning     {len(board.burning):>5}", STATE_COLORS[BURNING]),
            ("", TEXT_COLOR),
            (f"Active threats ({len(board.active)})   predicted miss", STATE_COLORS[THREATENED]),
        ]
        ranked = sorted(board.active.values(), key=lambda threat: threat.predicted_miss_m)
        for threat in ranked[:LISTED_THREATS]:
            first, second = (name[:NAME_WIDTH] for name in threat.pair)
            lines.append(
                (
                    f"{first:<{NAME_WIDTH}} x {second:<{NAME_WIDTH}} {threat.predicted_miss_m:>5.0f} m"
                    f"  {threat.time_to_closest_approach_s / 60:>4.1f}'",
                    MUTED_COLOR,
                )
            )
        return lines

    def _draw_panel(self, screen: pygame.Surface) -> None:
        lines = self._panel_lines()
        line_height = self.font.get_linesize()
        height = MARGIN * 3 + self.title_font.get_linesize() + line_height * len(lines)
        panel = pygame.Surface((PANEL_WIDTH, height), pygame.SRCALPHA)
        panel.fill(PANEL_COLOR)
        left = screen.get_width() - PANEL_WIDTH - MARGIN
        screen.blit(panel, (left, MARGIN))
        y = MARGIN * 2
        screen.blit(self.title_font.render(self.title, True, TEXT_COLOR), (left + MARGIN, y))
        y += self.title_font.get_linesize() + MARGIN
        for text, color in lines:
            screen.blit(self.font.render(text, True, color), (left + MARGIN, y))
            y += line_height

    def _draw_legend(self, screen: pygame.Surface) -> None:
        entries = [
            ("controlled satellite", SATELLITE_COLOR),
            ("other object", OTHER_OBJECT_COLOR),
            ("predicted miss < 1 km", STATE_COLORS[THREATENED]),
            ("burning", STATE_COLORS[BURNING]),
            ("close approach < 1 km", STATE_COLORS[CLOSE_APPROACH]),
        ]
        line_height = self.small_font.get_linesize() + 2
        y = screen.get_height() - MARGIN - line_height * len(entries)
        for text, color in entries:
            pygame.draw.circle(screen, color, (MARGIN + 5, y + line_height // 2), 4)
            screen.blit(self.small_font.render(text, True, TEXT_COLOR), (MARGIN + 16, y))
            y += line_height
