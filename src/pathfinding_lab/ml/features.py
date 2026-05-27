"""Feature extraction for learned heuristics."""

from typing import List

import numpy as np

from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.types import Position
from src.pathfinding_lab.ml.dataset import extract_features as base_extract_features


def extract_features(grid: Grid, current: Position, goal: Position) -> np.ndarray:
    """
    Extract features for heuristic prediction.

    Args:
        grid: Current grid
        current: Current position
        goal: Goal position

    Returns:
        Feature vector as numpy array
    """
    features = base_extract_features(grid, current, goal)
    return np.array(features).reshape(1, -1)
