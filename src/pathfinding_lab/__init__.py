"""
AI Pathfinding Laboratory - Educational pathfinding algorithms with Gradio interface.
"""

__version__ = "0.1.0"

from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.node import Node
from src.pathfinding_lab.core.result import SearchResult
from src.pathfinding_lab.core.types import Position, CellType, MovementMode

__all__ = [
    "Grid",
    "Node",
    "SearchResult",
    "Position",
    "CellType",
    "MovementMode",
]
