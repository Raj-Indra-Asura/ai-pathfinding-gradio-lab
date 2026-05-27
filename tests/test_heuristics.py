"""Tests for heuristic functions."""

import pytest
import math

from src.pathfinding_lab.heuristics.manhattan import manhattan_distance
from src.pathfinding_lab.heuristics.euclidean import euclidean_distance
from src.pathfinding_lab.heuristics.chebyshev import chebyshev_distance
from src.pathfinding_lab.heuristics.octile import octile_distance
from src.pathfinding_lab.heuristics.weighted import weighted_manhattan_distance


def test_manhattan_distance():
    """Test Manhattan distance calculation."""
    assert manhattan_distance((0, 0), (3, 4)) == 7
    assert manhattan_distance((1, 1), (1, 1)) == 0
    assert manhattan_distance((5, 5), (2, 3)) == 5


def test_euclidean_distance():
    """Test Euclidean distance calculation."""
    assert euclidean_distance((0, 0), (3, 4)) == pytest.approx(5.0, rel=0.01)
    assert euclidean_distance((1, 1), (1, 1)) == 0.0
    assert euclidean_distance((0, 0), (1, 1)) == pytest.approx(math.sqrt(2), rel=0.01)


def test_chebyshev_distance():
    """Test Chebyshev distance calculation."""
    assert chebyshev_distance((0, 0), (3, 4)) == 4
    assert chebyshev_distance((1, 1), (1, 1)) == 0
    assert chebyshev_distance((0, 0), (5, 5)) == 5


def test_octile_distance():
    """Test Octile distance calculation."""
    # Straight line should equal Manhattan
    assert octile_distance((0, 0), (0, 4)) == pytest.approx(4.0, rel=0.01)

    # Diagonal should use sqrt(2)
    assert octile_distance((0, 0), (2, 2)) == pytest.approx(2 * math.sqrt(2), rel=0.01)


def test_weighted_manhattan():
    """Test weighted Manhattan distance."""
    base = manhattan_distance((0, 0), (3, 4))
    weighted = weighted_manhattan_distance((0, 0), (3, 4), weight=2.0)

    assert weighted == base * 2.0


def test_heuristic_admissibility():
    """Test that heuristics never overestimate for simple cases."""
    # For 4-directional movement, Manhattan is admissible
    pos1 = (0, 0)
    pos2 = (3, 4)

    actual_cost = 7  # Minimum steps in 4-directional

    h_manhattan = manhattan_distance(pos1, pos2)
    h_euclidean = euclidean_distance(pos1, pos2)
    h_chebyshev = chebyshev_distance(pos1, pos2)

    # Manhattan should exactly match for 4-directional
    assert h_manhattan == actual_cost

    # Euclidean and Chebyshev should underestimate for 4-directional
    assert h_euclidean <= actual_cost
    assert h_chebyshev <= actual_cost
