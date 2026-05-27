"""Maze generation module."""

from pathfinding_lab.mazes.generators import (
    generate_random_obstacles,
    generate_maze_pattern,
)
from pathfinding_lab.mazes.presets import get_preset_maze

__all__ = [
    "generate_random_obstacles",
    "generate_maze_pattern",
    "get_preset_maze",
]
