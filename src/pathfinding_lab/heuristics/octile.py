"""Octile distance heuristic."""

import math

from src.pathfinding_lab.core.types import Position


def octile_distance(pos1: Position, pos2: Position) -> float:
    """
    Calculate Octile distance between two positions.

    Octile distance considers that diagonal moves cost sqrt(2) and
    cardinal moves cost 1. It's admissible and consistent for 8-directional
    movement on a grid.

    Formula: D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    where D = 1 (cardinal cost), D2 = sqrt(2) (diagonal cost)

    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)

    Returns:
        Octile distance
    """
    row1, col1 = pos1
    row2, col2 = pos2

    dx = abs(row1 - row2)
    dy = abs(col1 - col2)

    # Cost constants
    D = 1.0  # Cardinal movement cost
    D2 = math.sqrt(2)  # Diagonal movement cost

    # Octile distance formula
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
