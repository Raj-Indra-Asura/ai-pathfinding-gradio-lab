"""Type definitions for the pathfinding laboratory."""

from enum import Enum
from typing import Tuple

# Position is represented as (row, col) tuple
Position = Tuple[int, int]


class CellType(Enum):
    """Types of cells in the grid."""
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    GOAL = 3
    VISITED = 4
    PATH = 5


class MovementMode(Enum):
    """Movement directions available."""
    FOUR_DIRECTIONAL = 4
    EIGHT_DIRECTIONAL = 8
