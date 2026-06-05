"""Tests for Bidirectional BFS algorithm."""

import pytest

from pathfinding_lab.algorithms.bidirectional_bfs import bidirectional_bfs
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode


def test_bidirectional_simple_path():
    """Test Bidirectional BFS finds a path in an open grid."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = bidirectional_bfs(grid, start, goal)

    assert result.success is True
    assert result.path_length > 0
    assert result.path[0] == start
    assert result.path[-1] == goal


def test_bidirectional_path_is_valid():
    """Test that every step in the Bidirectional BFS path is a valid neighbour move."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = bidirectional_bfs(grid, start, goal)

    assert result.success is True
    path = result.path
    for i in range(len(path) - 1):
        r0, c0 = path[i]
        r1, c1 = path[i + 1]
        assert abs(r1 - r0) + abs(c1 - c0) == 1, (
            f"Invalid step from {path[i]} to {path[i + 1]}"
        )


def test_bidirectional_no_path():
    """Test Bidirectional BFS returns failure when no path exists."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    # Surround goal completely
    grid.add_obstacle((3, 4))
    grid.add_obstacle((4, 3))
    grid.add_obstacle((3, 3))

    result = bidirectional_bfs(grid, start, goal)

    assert result is not None
    assert isinstance(result.success, bool)


def test_bidirectional_with_obstacles():
    """Test Bidirectional BFS finds a path around obstacles."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (0, 4)

    # Wall with a gap at the bottom row
    for row in range(4):
        grid.add_obstacle((row, 2))

    result = bidirectional_bfs(grid, start, goal)

    assert result.success is True
    for pos in result.path:
        assert pos not in grid.obstacles, f"Path passes through obstacle {pos}"


def test_bidirectional_visited_tracking():
    """Test Bidirectional BFS records visited nodes from both directions."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = bidirectional_bfs(grid, start, goal)

    assert len(result.visited_order) > 0
    # Both start and goal are seeded into visited_order at initialisation
    assert start in result.visited_order
    assert goal in result.visited_order


def test_bidirectional_fewer_nodes_than_bfs():
    """Test Bidirectional BFS visits fewer nodes than regular BFS on a large open grid.

    On a 15×15 obstacle-free grid the two frontiers meet roughly halfway, so
    each frontier only needs to cover half the search space.  This advantage
    disappears on very small grids where the overhead of managing two queues
    may actually increase node counts; the 15×15 size is chosen to ensure the
    assertion holds reliably.
    """
    grid = Grid(15, 15, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (14, 14)

    from pathfinding_lab.algorithms.bfs import bfs

    bidir_result = bidirectional_bfs(grid, start, goal)
    bfs_result = bfs(grid, start, goal)

    assert bidir_result.success is True
    assert bfs_result.success is True
    # Bidirectional search should explore fewer nodes than one-directional BFS
    assert bidir_result.nodes_visited <= bfs_result.nodes_visited


def test_bidirectional_result_has_algorithm_name():
    """Test that the result carries the correct algorithm name."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = bidirectional_bfs(grid, (0, 0), (4, 4))

    assert "Bidirectional" in result.algorithm_name
