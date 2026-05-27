"""Grid representation for pathfinding."""

import random
from typing import List, Optional, Set

import numpy as np

from pathfinding_lab.core.node import Node
from pathfinding_lab.core.types import MovementMode, Position


class Grid:
    """
    Represents a 2D grid for pathfinding algorithms.

    The grid contains obstacles and provides methods to:
    - Generate random obstacles
    - Get neighbors of a cell
    - Check if a position is valid
    - Convert between grid and node representations
    """

    def __init__(
        self,
        width: int,
        height: int,
        obstacle_density: float = 0.2,
        movement_mode: MovementMode = MovementMode.FOUR_DIRECTIONAL,
        random_seed: Optional[int] = None,
    ):
        """
        Initialize a grid.

        Args:
            width: Number of columns
            height: Number of rows
            obstacle_density: Fraction of cells to be obstacles (0.0 to 1.0)
            movement_mode: 4-directional or 8-directional movement
            random_seed: Seed for reproducible random obstacle generation
        """
        self.width = width
        self.height = height
        self.obstacle_density = obstacle_density
        self.movement_mode = movement_mode

        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)

        # Initialize empty grid (0 = empty, 1 = obstacle)
        self.grid = np.zeros((height, width), dtype=int)
        self.obstacles: Set[Position] = set()

    def generate_obstacles(self, start: Position, goal: Position) -> None:
        """
        Generate random obstacles, ensuring start and goal remain accessible.

        Args:
            start: Start position to keep clear
            goal: Goal position to keep clear
        """
        total_cells = self.width * self.height
        num_obstacles = int(total_cells * self.obstacle_density)

        # Keep start and goal clear
        protected_positions = {start, goal}

        # Also protect immediate neighbors to ensure some initial movement
        for neighbor in self.get_neighbors(start):
            protected_positions.add(neighbor)
        for neighbor in self.get_neighbors(goal):
            protected_positions.add(neighbor)

        attempts = 0
        max_attempts = num_obstacles * 10

        while len(self.obstacles) < num_obstacles and attempts < max_attempts:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            pos = (row, col)

            if pos not in protected_positions and pos not in self.obstacles:
                self.add_obstacle(pos)

            attempts += 1

    def add_obstacle(self, position: Position) -> None:
        """Add an obstacle at the given position."""
        row, col = position
        if self.is_valid(position):
            self.grid[row, col] = 1
            self.obstacles.add(position)

    def remove_obstacle(self, position: Position) -> None:
        """Remove an obstacle at the given position."""
        row, col = position
        if self.is_valid(position):
            self.grid[row, col] = 0
            self.obstacles.discard(position)

    def is_valid(self, position: Position) -> bool:
        """Check if a position is within grid bounds."""
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width

    def is_obstacle(self, position: Position) -> bool:
        """Check if a position contains an obstacle."""
        if not self.is_valid(position):
            return True
        return position in self.obstacles

    def get_neighbors(self, position: Position) -> List[Position]:
        """
        Get valid neighboring positions.

        Args:
            position: Current position

        Returns:
            List of valid neighbor positions (not obstacles, within bounds)
        """
        row, col = position
        neighbors = []

        if self.movement_mode == MovementMode.FOUR_DIRECTIONAL:
            # Cardinal directions: up, right, down, left
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        else:  # EIGHT_DIRECTIONAL
            # Cardinal + diagonal directions
            directions = [
                (-1, 0), (-1, 1), (0, 1), (1, 1),
                (1, 0), (1, -1), (0, -1), (-1, -1)
            ]

        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if self.is_valid(new_pos) and not self.is_obstacle(new_pos):
                neighbors.append(new_pos)

        return neighbors

    def get_movement_cost(self, from_pos: Position, to_pos: Position) -> float:
        """
        Get the cost of moving from one position to another.

        Args:
            from_pos: Starting position
            to_pos: Destination position

        Returns:
            Movement cost (1.0 for cardinal, ~1.414 for diagonal)
        """
        row1, col1 = from_pos
        row2, col2 = to_pos

        # Check if diagonal movement
        if abs(row1 - row2) == 1 and abs(col1 - col2) == 1:
            return np.sqrt(2)  # Diagonal cost

        return 1.0  # Cardinal cost

    def create_node(self, position: Position) -> Node:
        """Create a Node object for the given position."""
        return Node(position=position, is_obstacle=self.is_obstacle(position))

    def reset(self) -> None:
        """Clear all obstacles from the grid."""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.obstacles.clear()

    def copy(self) -> 'Grid':
        """Create a deep copy of this grid."""
        new_grid = Grid(self.width, self.height, 0.0, self.movement_mode)
        new_grid.grid = self.grid.copy()
        new_grid.obstacles = self.obstacles.copy()
        return new_grid
