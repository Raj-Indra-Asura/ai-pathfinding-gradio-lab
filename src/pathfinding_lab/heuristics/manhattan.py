"""Manhattan distance heuristic."""

from src.pathfinding_lab.core.types import Position


def manhattan_distance(pos1: Position, pos2: Position) -> float:
    """
    Calculate Manhattan (taxicab) distance between two positions.

    Manhattan distance is the sum of absolute differences of coordinates.
    It's admissible for 4-directional movement.

    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)

    Returns:
        Manhattan distance
    """
    row1, col1 = pos1
    row2, col2 = pos2
    return abs(row1 - row2) + abs(col1 - col2)
