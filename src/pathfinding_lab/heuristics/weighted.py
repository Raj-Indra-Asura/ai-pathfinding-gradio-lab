"""Weighted Manhattan distance heuristic."""

from src.pathfinding_lab.core.types import Position


def weighted_manhattan_distance(pos1: Position, pos2: Position, weight: float = 1.0) -> float:
    """
    Calculate weighted Manhattan distance between two positions.

    Weighted heuristics can be used to make A* behave more greedily.
    A weight > 1.0 makes A* faster but may find sub-optimal paths.
    A weight < 1.0 ensures admissibility but may be slower.

    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)
        weight: Multiplier for the heuristic value

    Returns:
        Weighted Manhattan distance
    """
    row1, col1 = pos1
    row2, col2 = pos2
    manhattan = abs(row1 - row2) + abs(col1 - col2)
    return weight * manhattan
