"""Tests for Dijkstra's algorithm."""

import pytest

from pathfinding_lab.algorithms.dijkstra import dijkstra
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode


def test_dijkstra_simple_path():
    """Test Dijkstra finds a path in open grid."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = dijkstra(grid, start, goal)

    assert result.success is True
    assert result.path_length > 0
    assert result.path[0] == start
    assert result.path[-1] == goal


def test_dijkstra_optimal_path():
    """Test Dijkstra finds optimal path."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = dijkstra(grid, start, goal)

    # Path cost should equal Manhattan distance for 4-directional
    expected_cost = abs(goal[0] - start[0]) + abs(goal[1] - start[1])
    assert result.path_cost == pytest.approx(expected_cost, rel=0.01)


def test_dijkstra_8_directional():
    """Test Dijkstra with 8-directional movement."""
    grid = Grid(5, 5, 0.0, MovementMode.EIGHT_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = dijkstra(grid, start, goal)

    assert result.success is True
    # With diagonal movement, should be more efficient
    assert result.path_cost < 4.0  # Would be 4 with only cardinal moves


def test_dijkstra_with_obstacles():
    """Test Dijkstra finds path around obstacles."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (0, 4)

    # Add wall
    grid.add_obstacle((0, 2))

    result = dijkstra(grid, start, goal)

    if result.success:
        # Path should avoid obstacle
        assert (0, 2) not in result.path
