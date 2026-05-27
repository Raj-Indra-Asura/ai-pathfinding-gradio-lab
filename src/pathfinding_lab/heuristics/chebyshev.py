"""Chebyshev distance heuristic."""

from src.pathfinding_lab.core.types import Position


def chebyshev_distance(pos1: Position, pos2: Position) -> float:
    """
    Calculate Chebyshev (chessboard) distance between two positions.

    Chebyshev distance is the maximum of absolute differences of coordinates.
    It's admissible for 8-directional movement with equal diagonal cost.

    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)

    Returns:
        Chebyshev distance
    """
    row1, col1 = pos1
    row2, col2 = pos2
    return max(abs(row1 - row2), abs(col1 - col2))
