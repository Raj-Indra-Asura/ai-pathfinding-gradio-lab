"""Preset maze configurations."""

from typing import List, Tuple

from pathfinding_lab.core.types import Position


def get_preset_maze(name: str, width: int, height: int) -> Tuple[Position, Position, List[Position]]:
    """
    Get a preset maze configuration.

    Args:
        name: Name of the preset
        width: Grid width
        height: Grid height

    Returns:
        Tuple of (start, goal, obstacles)
    """
    # Simple presets for demonstration
    start = (0, 0)
    goal = (height - 1, width - 1)

    if name == "empty":
        return start, goal, []

    elif name == "simple_wall":
        # Single vertical wall with a gap
        obstacles = []
        mid_col = width // 2
        for row in range(height):
            if row != height // 2:
                obstacles.append((row, mid_col))
        return start, goal, obstacles

    elif name == "spiral":
        # TODO: Implement spiral maze pattern
        return start, goal, []

    else:
        return start, goal, []
