import numpy as np
import pytest

from orbitzoo.thesis.visualization.board import (
    BURNING,
    CLOSE_APPROACH,
    NOMINAL,
    THREATENED,
    ThreatBoard,
)
from orbitzoo.thesis.visualization.playback import COAST, burn_schedule, substep_dynamics


def _assessment(first, second, miss, tca, unsafe=True):
    return {
        "first_name": first,
        "second_name": second,
        "predicted_miss_distance_meters": miss,
        "time_to_closest_approach_seconds": tca,
        "is_unsafe": unsafe,
    }


def _info(step, assessments=(), close=(), collisions=()):
    return {
        "step_index": step,
        "flagged_assessments": list(assessments),
        "close_approaches": [{"pair": pair, "miss_distance_meters": miss} for pair, miss in close],
        "collision_pairs": list(collisions),
    }


def test_burn_schedule_keeps_every_burn_whole_in_first_substep():
    schedule = burn_schedule(120.0, 10.0, {"a": 21.4, "b": 0.0})

    assert schedule[0] == (pytest.approx(21.4), {"a": 21.4, "b": 0.0})
    assert sum(dt for dt, _ in schedule) == pytest.approx(120.0)
    assert all(dt <= 10.0 + 1e-9 for dt, _ in schedule[1:])
    assert all(burns == {"a": 0.0, "b": 0.0} for _, burns in schedule[1:])


def test_burn_schedule_uses_substep_length_when_no_one_burns():
    schedule = burn_schedule(100.0, 30.0, {"a": 0.0})

    assert schedule[0][0] == 30.0
    assert [dt for dt, _ in schedule[1:]] == pytest.approx([70.0 / 3] * 3)


def test_burn_schedule_is_one_step_when_substep_covers_it():
    assert burn_schedule(120.0, 120.0, {"a": 21.4}) == [(120.0, {"a": 21.4})]


def test_burn_schedule_rejects_non_positive_sizes():
    with pytest.raises(ValueError):
        burn_schedule(120.0, 0.0, {})


def test_substep_dynamics_coasts_after_burn_and_calls_back_each_substep():
    calls = []

    class Dynamics:
        step_size = 60.0

        def step(self, step_size, actions, maneuver_durations):
            calls.append((step_size, dict(actions), dict(maneuver_durations)))

    dynamics = Dynamics()
    rendered = []
    substep_dynamics(dynamics, 20.0, lambda: rendered.append(True))

    dynamics.step(60.0, {"a": [0.0, 7.0, 0.0]}, {"a": 30.0})

    assert len(calls) == len(rendered) == 3
    assert [call[0] for call in calls] == pytest.approx([30.0, 15.0, 15.0])
    assert [call[2]["a"] for call in calls] == [30.0, 0.0, 0.0]
    assert calls[0][1]["a"] == [0.0, 7.0, 0.0]
    assert calls[1][1]["a"] == COAST


def test_board_counts_threat_cleared_before_its_encounter():
    board = ThreatBoard(["sat1", "sat2"], 120.0)
    board.observe_assessments([_assessment("deb1", "sat1", 300.0, 600.0)])

    board.observe_step(_info(1))

    assert board.cleared == 1
    assert board.active == {}


def test_board_does_not_count_threat_flown_past():
    board = ThreatBoard(["sat1"], 120.0)
    board.observe_assessments([_assessment("sat1", "deb1", 300.0, 60.0)])

    board.observe_step(_info(1, close=[(("sat1", "deb1"), 300.0)]))

    assert board.cleared == 0
    assert board.close_approaches == 1
    assert board.closest_approach_m == 300.0


def test_board_ignores_pairs_without_controlled_satellite_and_orders_agent_first():
    board = ThreatBoard(["sat1"], 120.0)
    board.observe_assessments(
        [
            _assessment("deb1", "deb2", 100.0, 600.0),
            _assessment("deb1", "sat1", 400.0, 600.0),
            _assessment("deb3", "sat1", 5000.0, 600.0, unsafe=False),
        ]
    )

    assert [threat.pair for threat in board.active.values()] == [("sat1", "deb1")]


def test_board_keeps_first_predicted_miss():
    board = ThreatBoard(["sat1"], 120.0)
    board.observe_assessments([_assessment("sat1", "deb1", 300.0, 600.0)])
    board.observe_assessments([_assessment("sat1", "deb1", 800.0, 480.0)])

    (threat,) = board.active.values()
    assert threat.predicted_miss_m == 800.0
    assert threat.first_predicted_miss_m == 300.0


def test_board_state_priority():
    board = ThreatBoard(["sat1", "sat2", "sat3"], 120.0)
    board.observe_assessments([_assessment("sat1", "deb1", 300.0, 600.0), _assessment("sat2", "deb2", 300.0, 600.0)])
    board.begin_decision(["sat1", "sat2", "sat3"], np.array([1, 0, 0]))
    board.recent_close_approaches = [(("sat3", "deb3"), 500.0)]

    assert board.state_of("sat1") == BURNING
    assert board.state_of("sat2") == THREATENED
    assert board.state_of("sat3") == CLOSE_APPROACH
    assert board.state_of("deb9") == NOMINAL
