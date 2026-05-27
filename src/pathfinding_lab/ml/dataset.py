"""Dataset generation for learned heuristics."""

import random
from typing import List, Tuple

import numpy as np

from pathfinding_lab.algorithms.dijkstra import dijkstra
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode, Position


def generate_training_data(
    num_samples: int = 1000,
    grid_size: int = 20,
    obstacle_density: float = 0.2,
    random_seed: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate training data for learned heuristic.

    For each sample, we:
    1. Create a random grid
    2. Pick random start and goal
    3. Run Dijkstra to get true optimal distance
    4. Extract features from the state

    Args:
        num_samples: Number of training samples
        grid_size: Size of grid
        obstacle_density: Density of obstacles
        random_seed: Random seed

    Returns:
        Tuple of (features, labels) as numpy arrays
    """
    random.seed(random_seed)
    np.random.seed(random_seed)

    features = []
    labels = []

    for i in range(num_samples):
        # Create grid
        grid = Grid(grid_size, grid_size, obstacle_density, MovementMode.FOUR_DIRECTIONAL)

        # Random start and goal
        start = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        goal = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))

        # Generate obstacles
        grid.generate_obstacles(start, goal)

        # Run Dijkstra to get true distance
        result = dijkstra(grid, start, goal)

        if result.success:
            # Extract features
            feature_vector = extract_features(grid, start, goal)
            features.append(feature_vector)
            labels.append(result.path_cost)

        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_samples} samples")

    return np.array(features), np.array(labels)


def extract_features(grid: Grid, start: Position, goal: Position) -> List[float]:
    """
    Extract features from a grid state.

    Features:
    - Manhattan distance
    - Euclidean distance
    - Straight-line obstacle count
    - Local obstacle density around start
    - Local obstacle density around goal

    Args:
        grid: Current grid
        start: Start position
        goal: Goal position

    Returns:
        Feature vector
    """
    start_row, start_col = start
    goal_row, goal_col = goal

    # Basic distance features
    manhattan = abs(start_row - goal_row) + abs(start_col - goal_col)
    euclidean = np.sqrt((start_row - goal_row) ** 2 + (start_col - goal_col) ** 2)

    # Count obstacles in straight line (bresenham-style)
    obstacles_in_line = count_obstacles_in_line(grid, start, goal)

    # Local obstacle density
    start_density = get_local_obstacle_density(grid, start, radius=2)
    goal_density = get_local_obstacle_density(grid, goal, radius=2)

    return [manhattan, euclidean, obstacles_in_line, start_density, goal_density]


def count_obstacles_in_line(grid: Grid, start: Position, goal: Position) -> int:
    """Count obstacles in approximate straight line between start and goal."""
    count = 0
    start_row, start_col = start
    goal_row, goal_col = goal

    steps = max(abs(goal_row - start_row), abs(goal_col - start_col))
    if steps == 0:
        return 0

    for i in range(steps + 1):
        t = i / steps
        row = int(start_row + t * (goal_row - start_row))
        col = int(start_col + t * (goal_col - start_col))
        if grid.is_obstacle((row, col)):
            count += 1

    return count


def get_local_obstacle_density(grid: Grid, position: Position, radius: int = 2) -> float:
    """Calculate obstacle density in local neighborhood."""
    row, col = position
    count = 0
    total = 0

    for dr in range(-radius, radius + 1):
        for dc in range(-radius, radius + 1):
            new_row, new_col = row + dr, col + dc
            if grid.is_valid((new_row, new_col)):
                total += 1
                if grid.is_obstacle((new_row, new_col)):
                    count += 1

    return count / total if total > 0 else 0
