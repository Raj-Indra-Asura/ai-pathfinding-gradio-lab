"""Maze and obstacle pattern generators."""

import random
from typing import Set

from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.types import Position


def generate_random_obstacles(
    grid: Grid,
    start: Position,
    goal: Position,
    density: float = 0.2
) -> Set[Position]:
    """
    Generate random obstacles.

    Args:
        grid: Grid to generate obstacles for
        start: Start position to keep clear
        goal: Goal position to keep clear
        density: Fraction of cells to make obstacles

    Returns:
        Set of obstacle positions
    """
    grid.generate_obstacles(start, goal)
    return grid.obstacles


def generate_maze_pattern(grid: Grid, start: Position, goal: Position, pattern: str = "vertical") -> None:
    """
    Generate patterned obstacles.

    Args:
        grid: Grid to add obstacles to
        start: Start position
        goal: Goal position
        pattern: Pattern type ('vertical', 'horizontal', 'checkerboard')
    """
    grid.reset()

    if pattern == "vertical":
        # Vertical walls with gaps
        for col in range(2, grid.width, 4):
            for row in range(grid.height):
                if row % 3 != 0:  # Leave gaps
                    pos = (row, col)
                    if pos != start and pos != goal:
                        grid.add_obstacle(pos)

    elif pattern == "horizontal":
        # Horizontal walls with gaps
        for row in range(2, grid.height, 4):
            for col in range(grid.width):
                if col % 3 != 0:  # Leave gaps
                    pos = (row, col)
                    if pos != start and pos != goal:
                        grid.add_obstacle(pos)

    elif pattern == "checkerboard":
        # Checkerboard pattern
        for row in range(grid.height):
            for col in range(grid.width):
                if (row + col) % 2 == 0 and random.random() < 0.3:
                    pos = (row, col)
                    if pos != start and pos != goal:
                        grid.add_obstacle(pos)


# TODO: Implement recursive division maze generation
# TODO: Implement Prim's algorithm maze generation
# TODO: Implement Kruskal's algorithm maze generation
