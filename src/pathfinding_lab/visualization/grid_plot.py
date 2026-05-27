"""Grid visualization using Matplotlib."""

from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.result import SearchResult
from pathfinding_lab.core.types import Position


def create_grid_plot(
    grid: Grid,
    start: Position,
    goal: Position,
    result: Optional[SearchResult] = None,
    figsize: tuple = (10, 10)
) -> plt.Figure:
    """
    Create a visualization of the grid with pathfinding results.

    Args:
        grid: The grid to visualize
        start: Start position
        goal: Goal position
        result: Optional SearchResult to overlay path and visited nodes
        figsize: Figure size (width, height)

    Returns:
        Matplotlib Figure object
    """
    # Create base grid visualization
    vis_grid = np.zeros((grid.height, grid.width))

    # Mark obstacles
    for obstacle in grid.obstacles:
        row, col = obstacle
        vis_grid[row, col] = 1

    # Mark visited nodes if result provided
    if result and result.visited_order:
        for pos in result.visited_order:
            row, col = pos
            if pos != start and pos != goal:
                vis_grid[row, col] = 2

    # Mark path if result provided and path found
    if result and result.path:
        for pos in result.path:
            row, col = pos
            if pos != start and pos != goal:
                vis_grid[row, col] = 3

    # Mark start and goal
    start_row, start_col = start
    goal_row, goal_col = goal
    vis_grid[start_row, start_col] = 4
    vis_grid[goal_row, goal_col] = 5

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Define colors: empty, obstacle, visited, path, start, goal
    colors = ['white', 'black', 'lightblue', 'yellow', 'green', 'red']
    cmap = ListedColormap(colors)

    # Display grid
    ax.imshow(vis_grid, cmap=cmap, vmin=0, vmax=5)

    # Add grid lines
    ax.set_xticks(np.arange(-0.5, grid.width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.height, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    ax.tick_params(which='minor', size=0)

    # Labels
    ax.set_xlabel('Column')
    ax.set_ylabel('Row')

    # Title
    if result:
        title = f"{result.algorithm_name}\n"
        if result.success:
            title += f"Path Length: {result.path_length}, "
            title += f"Cost: {result.path_cost:.2f}, "
            title += f"Visited: {result.nodes_visited}, "
            title += f"Time: {result.runtime_ms:.2f}ms"
        else:
            title += result.message
        ax.set_title(title)
    else:
        ax.set_title(f"Grid ({grid.width}x{grid.height})")

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='Start'),
        Patch(facecolor='red', label='Goal'),
        Patch(facecolor='black', label='Obstacle'),
        Patch(facecolor='lightblue', label='Visited'),
        Patch(facecolor='yellow', label='Path'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    return fig
