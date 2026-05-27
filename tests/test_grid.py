"""Tests for Grid class."""

import pytest

from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode


def test_grid_creation():
    """Test basic grid creation."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    assert grid.width == 10
    assert grid.height == 10
    assert len(grid.obstacles) == 0


def test_obstacle_generation():
    """Test obstacle generation."""
    grid = Grid(10, 10, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
    start = (0, 0)
    goal = (9, 9)
    grid.generate_obstacles(start, goal)

    # Should have some obstacles
    assert len(grid.obstacles) > 0

    # Start and goal should be clear
    assert start not in grid.obstacles
    assert goal not in grid.obstacles


def test_neighbors_4_directional():
    """Test 4-directional neighbor generation."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    neighbors = grid.get_neighbors((5, 5))

    # Should have 4 neighbors in open grid
    assert len(neighbors) == 4

    # Check specific neighbors
    assert (4, 5) in neighbors  # Up
    assert (6, 5) in neighbors  # Down
    assert (5, 4) in neighbors  # Left
    assert (5, 6) in neighbors  # Right


def test_neighbors_8_directional():
    """Test 8-directional neighbor generation."""
    grid = Grid(10, 10, 0.0, MovementMode.EIGHT_DIRECTIONAL)
    neighbors = grid.get_neighbors((5, 5))

    # Should have 8 neighbors in open grid
    assert len(neighbors) == 8


def test_neighbors_with_obstacles():
    """Test neighbors with obstacles."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    grid.add_obstacle((4, 5))
    grid.add_obstacle((6, 5))

    neighbors = grid.get_neighbors((5, 5))

    # Should have only 2 neighbors (left and right)
    assert len(neighbors) == 2
    assert (5, 4) in neighbors
    assert (5, 6) in neighbors


def test_movement_cost():
    """Test movement cost calculation."""
    grid = Grid(10, 10, 0.0, MovementMode.EIGHT_DIRECTIONAL)

    # Cardinal movement should cost 1.0
    cost = grid.get_movement_cost((5, 5), (5, 6))
    assert cost == 1.0

    # Diagonal movement should cost sqrt(2)
    cost = grid.get_movement_cost((5, 5), (6, 6))
    assert cost == pytest.approx(1.414, rel=0.01)


def test_boundary_handling():
    """Test grid boundary handling."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)

    # Corner position should have 2 neighbors
    neighbors = grid.get_neighbors((0, 0))
    assert len(neighbors) == 2

    # Edge position should have 3 neighbors
    neighbors = grid.get_neighbors((0, 2))
    assert len(neighbors) == 3
