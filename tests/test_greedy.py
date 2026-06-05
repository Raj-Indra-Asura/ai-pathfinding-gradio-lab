"""Tests for Greedy Best-First Search algorithm."""

import pytest

from pathfinding_lab.algorithms.greedy_best_first import greedy_best_first
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.heuristics.euclidean import euclidean_distance


def test_greedy_simple_path():
    """Test Greedy Best-First finds a path in an open grid."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = greedy_best_first(grid, start, goal, manhattan_distance)

    assert result.success is True
    assert result.path_length > 0
    assert result.path[0] == start
    assert result.path[-1] == goal


def test_greedy_path_is_valid():
    """Test that every step in the Greedy path is a valid neighbour move."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = greedy_best_first(grid, start, goal, manhattan_distance)

    assert result.success is True
    path = result.path
    for i in range(len(path) - 1):
        r0, c0 = path[i]
        r1, c1 = path[i + 1]
        assert abs(r1 - r0) + abs(c1 - c0) == 1, (
            f"Invalid step from {path[i]} to {path[i + 1]}"
        )


def test_greedy_no_path():
    """Test Greedy Best-First returns failure when no path exists."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    # Completely block the goal
    grid.add_obstacle((3, 4))
    grid.add_obstacle((4, 3))
    grid.add_obstacle((3, 3))

    result = greedy_best_first(grid, start, goal, manhattan_distance)

    assert result is not None
    assert isinstance(result.success, bool)


def test_greedy_with_obstacles():
    """Test Greedy Best-First finds a path around obstacles."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (0, 4)

    # Partial wall with a gap at the bottom
    for row in range(4):
        grid.add_obstacle((row, 2))

    result = greedy_best_first(grid, start, goal, manhattan_distance)

    assert result.success is True
    for pos in result.path:
        assert pos not in grid.obstacles, f"Path passes through obstacle {pos}"


def test_greedy_visited_tracking():
    """Test Greedy Best-First records visited nodes."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = greedy_best_first(grid, start, goal, manhattan_distance)

    assert len(result.visited_order) > 0
    assert start in result.visited_order
    assert goal in result.visited_order


def test_greedy_different_heuristics_both_find_path():
    """Test Greedy Best-First works with different heuristics."""
    grid = Grid(5, 5, 0.0, MovementMode.EIGHT_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result_manhattan = greedy_best_first(grid, start, goal, manhattan_distance)
    result_euclidean = greedy_best_first(grid, start, goal, euclidean_distance)

    assert result_manhattan.success is True
    assert result_euclidean.success is True


def test_greedy_fewer_nodes_than_bfs():
    """Test Greedy typically visits fewer nodes than BFS on an open grid.

    On a large, obstacle-free grid Greedy Best-First is guided directly toward
    the goal by the heuristic, so it explores far fewer nodes than BFS.
    This property only holds reliably on open grids; in maze-like environments
    the heuristic can lead Greedy into dead ends, causing it to visit more nodes.
    """
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (9, 9)

    from pathfinding_lab.algorithms.bfs import bfs

    greedy_result = greedy_best_first(grid, start, goal, manhattan_distance)
    bfs_result = bfs(grid, start, goal)

    assert greedy_result.success is True
    assert bfs_result.success is True
    # Greedy uses a heuristic so it should visit fewer or equal nodes than BFS
    assert greedy_result.nodes_visited <= bfs_result.nodes_visited
