"""Tests for A* algorithm."""

import pytest

from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.heuristics.euclidean import euclidean_distance


def test_astar_simple_path():
    """Test A* finds a path in open grid."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = astar(grid, start, goal, manhattan_distance)

    assert result.success is True
    assert result.path_length > 0
    assert result.path[0] == start
    assert result.path[-1] == goal


def test_astar_optimal_path():
    """Test A* finds optimal path."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = astar(grid, start, goal, manhattan_distance)

    # A* with admissible heuristic should find optimal path
    expected_cost = abs(goal[0] - start[0]) + abs(goal[1] - start[1])
    assert result.path_cost == pytest.approx(expected_cost, rel=0.01)


def test_astar_better_than_dijkstra():
    """Test A* explores fewer nodes than Dijkstra."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (9, 9)

    from pathfinding_lab.algorithms.dijkstra import dijkstra

    astar_result = astar(grid, start, goal, manhattan_distance)
    dijkstra_result = dijkstra(grid, start, goal)

    # A* should visit fewer or equal nodes than Dijkstra
    assert astar_result.nodes_visited <= dijkstra_result.nodes_visited


def test_astar_different_heuristics():
    """Test A* with different heuristics."""
    grid = Grid(5, 5, 0.0, MovementMode.EIGHT_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result_manhattan = astar(grid, start, goal, manhattan_distance)
    result_euclidean = astar(grid, start, goal, euclidean_distance)

    # Both should find a path
    assert result_manhattan.success is True
    assert result_euclidean.success is True

    # Both should find same optimal cost (admissible heuristics)
    assert result_manhattan.path_cost == pytest.approx(result_euclidean.path_cost, rel=0.01)
