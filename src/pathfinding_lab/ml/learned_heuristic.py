"""Learned heuristic function using ML model."""

import pickle
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.ensemble import RandomForestRegressor

from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import Position
from pathfinding_lab.ml.features import extract_features


class LearnedHeuristic:
    """
    Learned heuristic using a trained ML model.

    WARNING: Learned heuristics are NOT guaranteed to be admissible,
    which means A* with this heuristic may not find optimal paths.
    This is an educational experiment to understand ML in pathfinding.
    """

    def __init__(self, model_path: str = "learned_heuristic_model.pkl"):
        """
        Initialize learned heuristic.

        Args:
            model_path: Path to trained model pickle file
        """
        self.model: Optional[RandomForestRegressor] = None
        self.model_path = model_path
        self._load_model()

    def _load_model(self) -> None:
        """Load the trained model from disk."""
        if Path(self.model_path).exists():
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
        else:
            print(f"Warning: Model file {self.model_path} not found.")
            print("Please train the model first using ml/train_heuristic.py")

    def __call__(self, grid: Grid, current: Position, goal: Position) -> float:
        """
        Predict distance from current to goal.

        Args:
            grid: Current grid
            current: Current position
            goal: Goal position

        Returns:
            Predicted distance
        """
        if self.model is None:
            # Fallback to Manhattan distance
            r1, c1 = current
            r2, c2 = goal
            return abs(r1 - r2) + abs(c1 - c2)

        features = extract_features(grid, current, goal)
        prediction = self.model.predict(features)[0]

        # Ensure non-negative
        return max(0.0, prediction)


def create_learned_heuristic_function(grid: Grid, model_path: str = "learned_heuristic_model.pkl"):
    """
    Create a learned heuristic function for use with pathfinding algorithms.

    Args:
        grid: Grid (needed for feature extraction)
        model_path: Path to trained model

    Returns:
        Heuristic function that takes (current, goal) and returns distance estimate
    """
    learned_h = LearnedHeuristic(model_path)

    def heuristic(current: Position, goal: Position) -> float:
        return learned_h(grid, current, goal)

    return heuristic
