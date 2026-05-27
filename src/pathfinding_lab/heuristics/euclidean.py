"""Euclidean distance heuristic."""

import math

from src.pathfinding_lab.core.types import Position


def euclidean_distance(pos1: Position, pos2: Position) -> float:
    """
    Calculate Euclidean (straight-line) distance between two positions.

    Euclidean distance is the straight-line distance in 2D space.
    It's admissible for 8-directional movement.

    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)

    Returns:
        Euclidean distance
    """
    row1, col1 = pos1
    row2, col2 = pos2
    return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)
