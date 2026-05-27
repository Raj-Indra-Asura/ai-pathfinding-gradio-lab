"""Node representation for pathfinding algorithms."""

from dataclasses import dataclass, field
from typing import Optional

from src.pathfinding_lab.core.types import Position


@dataclass
class Node:
    """
    Represents a single node/cell in the pathfinding grid.

    Attributes:
        position: (row, col) coordinates of the node
        g_cost: Cost from start node to this node (for Dijkstra, A*)
        h_cost: Heuristic estimate from this node to goal (for A*, Greedy)
        f_cost: Total cost (g_cost + h_cost) for A*
        parent: Parent node in the path (for path reconstruction)
        is_obstacle: Whether this node is blocked
    """
    position: Position
    g_cost: float = float('inf')
    h_cost: float = 0.0
    f_cost: float = float('inf')
    parent: Optional['Node'] = None
    is_obstacle: bool = False

    def __lt__(self, other: 'Node') -> bool:
        """Compare nodes by f_cost for priority queue ordering."""
        return self.f_cost < other.f_cost

    def __hash__(self) -> int:
        """Hash by position for use in sets."""
        return hash(self.position)

    def __eq__(self, other: object) -> bool:
        """Equality based on position."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.position == other.position

    def reset_costs(self) -> None:
        """Reset all costs to default values."""
        self.g_cost = float('inf')
        self.h_cost = 0.0
        self.f_cost = float('inf')
        self.parent = None
