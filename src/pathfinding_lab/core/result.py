"""Search result data structure."""

from dataclasses import dataclass, field
from typing import List, Optional

from pathfinding_lab.core.types import Position


@dataclass
class SearchResult:
    """
    Stores the result of a pathfinding algorithm execution.

    Attributes:
        algorithm_name: Name of the algorithm used
        success: Whether a path was found
        path: List of positions from start to goal (empty if no path)
        visited_order: Order in which nodes were visited
        path_length: Number of steps in the path
        path_cost: Total cost of the path
        nodes_visited: Number of nodes explored
        runtime_ms: Execution time in milliseconds
        message: Additional information or error message
    """
    algorithm_name: str
    success: bool
    path: List[Position] = field(default_factory=list)
    visited_order: List[Position] = field(default_factory=list)
    path_length: int = 0
    path_cost: float = 0.0
    nodes_visited: int = 0
    runtime_ms: float = 0.0
    message: str = ""

    def __post_init__(self):
        """Calculate derived fields."""
        if self.path:
            self.path_length = len(self.path)
