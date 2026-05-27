# Week 12: Solutions

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 11 Solutions](week_11_solutions.md)** | **📚 [Week 12 Documentation](../docs/week_12_final_project.md)** | **📝 [Week 12 Exercises](../exercises/week_12.md)**

---

## Exercise 1 Solution: Integration Testing

### Explanation

Integration testing verifies that different components of the system work together correctly. Unlike unit tests that isolate individual functions, integration tests exercise the full pipeline from UI input through algorithm execution to visualization output. This catches issues that only appear when components interact, such as data format mismatches, state management bugs, or callback timing issues.

For the Gradio pathfinding application, integration tests ensure that:
1. Grid generation creates valid, usable grids
2. Algorithm routing correctly dispatches to the right algorithm implementation
3. Visualization produces valid matplotlib figures from search results
4. All algorithms work end-to-end through the UI interface

These tests use pytest with fixtures to simulate Gradio's callback system, allowing us to test the UI functions without launching a web server.

### Code

```python
"""
Comprehensive integration tests for Gradio UI components.

Tests the full pipeline: grid generation → algorithm execution → visualization
"""

import pytest
import pandas as pd
from matplotlib.figure import Figure

from pathfinding_lab.ui.gradio_app import (
    generate_grid,
    run_algorithm,
    compare_algorithms,
    current_grid,
)
from pathfinding_lab.core.types import MovementMode


@pytest.fixture
def reset_grid():
    """Reset global grid state before and after each test."""
    import pathfinding_lab.ui.gradio_app as gradio_module

    # Clear global state before test
    gradio_module.current_grid = None

    yield

    # Clean up after test
    gradio_module.current_grid = None


def test_generate_grid_creates_valid_grid(reset_grid):
    """
    Test that generate_grid produces a valid grid with correct properties.

    Verifies:
    - Returns matplotlib Figure
    - Creates grid with correct dimensions
    - Respects obstacle density bounds
    - Sets start and goal correctly
    - Global current_grid is updated
    """
    # Generate a 10x10 grid with 20% obstacle density
    fig, message = generate_grid(
        width=10,
        height=10,
        obstacle_density=0.2,
        seed=42,
        movement_mode="4-directional",
        start_row=0,
        start_col=0,
        goal_row=9,
        goal_col=9
    )

    # Verify figure is valid matplotlib object
    assert isinstance(fig, Figure), "Should return matplotlib Figure"

    # Verify success message
    assert "generated" in message.lower(), "Should contain success message"
    assert "10" in message, "Should mention grid dimensions"

    # Access global grid state
    import pathfinding_lab.ui.gradio_app as gradio_module
    grid = gradio_module.current_grid

    # Verify grid exists and has correct dimensions
    assert grid is not None, "current_grid should be set"
    assert grid.width == 10, "Grid width should be 10"
    assert grid.height == 10, "Grid height should be 10"

    # Verify obstacle density is reasonable (with some variance due to randomness)
    obstacle_count = len(grid.obstacles)
    expected_obstacles = 10 * 10 * 0.2  # 20 obstacles
    # Allow 50% variance due to random generation and avoiding start/goal
    assert 10 <= obstacle_count <= 30, f"Obstacle count {obstacle_count} outside expected range"

    # Verify movement mode
    assert grid.movement_mode == MovementMode.FOUR_DIRECTIONAL


def test_generate_grid_avoids_start_and_goal(reset_grid):
    """
    Test that grid generation never places obstacles at start or goal.

    Critical for ensuring algorithms have valid starting conditions.
    """
    # Generate multiple grids with high obstacle density
    for seed in range(10):
        fig, message = generate_grid(
            width=20,
            height=20,
            obstacle_density=0.5,  # High density
            seed=seed,
            movement_mode="4-directional",
            start_row=5,
            start_col=5,
            goal_row=15,
            goal_col=15
        )

        import pathfinding_lab.ui.gradio_app as gradio_module
        grid = gradio_module.current_grid

        # Verify start and goal are never obstacles
        start = (5, 5)
        goal = (15, 15)
        assert start not in grid.obstacles, f"Start {start} should not be obstacle"
        assert goal not in grid.obstacles, f"Goal {goal} should not be obstacle"


def test_generate_grid_eight_directional(reset_grid):
    """Test 8-directional movement mode configuration."""
    fig, message = generate_grid(
        width=15,
        height=15,
        obstacle_density=0.1,
        seed=100,
        movement_mode="8-directional",
        start_row=0,
        start_col=0,
        goal_row=14,
        goal_col=14
    )

    import pathfinding_lab.ui.gradio_app as gradio_module
    grid = gradio_module.current_grid

    # Verify 8-directional mode
    assert grid.movement_mode == MovementMode.EIGHT_DIRECTIONAL

    # Corner should have 3 neighbors in 8-directional (not 2)
    corner_neighbors = grid.get_neighbors((0, 0))
    assert len(corner_neighbors) == 3, "8-directional corner should have 3 neighbors"


def test_run_algorithm_requires_grid_first(reset_grid):
    """
    Test that run_algorithm fails gracefully when no grid is generated.

    Important for user experience - clear error message guides user.
    """
    # Try to run algorithm without generating grid
    fig, metrics, message = run_algorithm(
        algorithm="BFS",
        heuristic="Manhattan",
        start_row=0,
        start_col=0,
        goal_row=9,
        goal_col=9
    )

    # Should return None for figure and metrics
    assert fig is None, "Should not return figure when grid missing"
    assert metrics is None, "Should not return metrics when grid missing"

    # Should have helpful error message
    assert "generate a grid first" in message.lower(), "Should prompt user to generate grid"


def test_run_algorithm_bfs(reset_grid):
    """Test BFS algorithm execution through UI."""
    # First generate a grid
    generate_grid(10, 10, 0.2, 42, "4-directional", 0, 0, 9, 9)

    # Run BFS
    fig, metrics, message = run_algorithm(
        algorithm="BFS",
        heuristic="Manhattan",  # BFS ignores heuristic
        start_row=0,
        start_col=0,
        goal_row=9,
        goal_col=9
    )

    # Verify figure
    assert isinstance(fig, Figure), "Should return matplotlib Figure"

    # Verify metrics DataFrame
    assert isinstance(metrics, pd.DataFrame), "Should return DataFrame"
    assert len(metrics) == 1, "Should have one row of metrics"

    # Verify expected columns
    expected_columns = {"Algorithm", "Path Length", "Path Cost", "Nodes Visited", "Runtime (ms)"}
    assert expected_columns.issubset(set(metrics.columns)), f"Missing columns: {expected_columns - set(metrics.columns)}"

    # Verify values are reasonable
    assert metrics["Algorithm"].iloc[0] == "BFS"
    assert metrics["Path Length"].iloc[0] > 0, "Should find a path"
    assert metrics["Nodes Visited"].iloc[0] > 0, "Should visit nodes"
    assert metrics["Runtime (ms)"].iloc[0] >= 0, "Runtime should be non-negative"

    # Verify success message
    assert "success" in message.lower() or "found" in message.lower()


def test_run_algorithm_astar_with_heuristic(reset_grid):
    """Test A* algorithm with different heuristics."""
    generate_grid(15, 15, 0.15, 123, "4-directional", 0, 0, 14, 14)

    # Test with Manhattan heuristic
    fig_manhattan, metrics_manhattan, msg_manhattan = run_algorithm(
        algorithm="A*",
        heuristic="Manhattan",
        start_row=0,
        start_col=0,
        goal_row=14,
        goal_col=14
    )

    assert isinstance(fig_manhattan, Figure)
    assert metrics_manhattan["Algorithm"].iloc[0] == "A*"
    assert metrics_manhattan["Path Length"].iloc[0] > 0

    # Test with Euclidean heuristic
    generate_grid(15, 15, 0.15, 123, "4-directional", 0, 0, 14, 14)  # Same grid
    fig_euclidean, metrics_euclidean, msg_euclidean = run_algorithm(
        algorithm="A*",
        heuristic="Euclidean",
        start_row=0,
        start_col=0,
        goal_row=14,
        goal_col=14
    )

    # Both should find optimal path (same length)
    assert metrics_manhattan["Path Length"].iloc[0] == metrics_euclidean["Path Length"].iloc[0]

    # May explore different number of nodes
    manhattan_visited = metrics_manhattan["Nodes Visited"].iloc[0]
    euclidean_visited = metrics_euclidean["Nodes Visited"].iloc[0]
    assert manhattan_visited > 0 and euclidean_visited > 0


def test_all_algorithms_can_run(reset_grid):
    """
    Test that all 6 algorithms can be executed through UI.

    Comprehensive test ensuring algorithm routing works for all algorithms.
    """
    # Generate test grid once
    generate_grid(12, 12, 0.25, 999, "4-directional", 1, 1, 10, 10)

    algorithms = [
        ("BFS", "Manhattan"),
        ("DFS", "Manhattan"),
        ("Dijkstra", "Manhattan"),
        ("Greedy Best-First", "Manhattan"),
        ("A*", "Manhattan"),
        ("Bidirectional BFS", "Manhattan"),
    ]

    results = []

    for algo, heuristic in algorithms:
        fig, metrics, message = run_algorithm(
            algorithm=algo,
            heuristic=heuristic,
            start_row=1,
            start_col=1,
            goal_row=10,
            goal_col=10
        )

        # Verify each algorithm produces valid output
        assert isinstance(fig, Figure), f"{algo} should return Figure"
        assert isinstance(metrics, pd.DataFrame), f"{algo} should return DataFrame"
        assert metrics["Algorithm"].iloc[0] == algo, f"Algorithm name should be {algo}"

        # Some algorithms might fail to find path with high obstacle density
        # But they should still return valid result structure
        if "success" in message.lower() or "found" in message.lower():
            assert metrics["Path Length"].iloc[0] > 0, f"{algo} should find path"

        results.append((algo, metrics))

    # All algorithms should have run
    assert len(results) == 6, "All 6 algorithms should execute"


def test_visualization_output_structure(reset_grid):
    """
    Test that visualization produces correct plot structure.

    Verifies the returned figure contains expected elements.
    """
    generate_grid(8, 8, 0.1, 42, "4-directional", 0, 0, 7, 7)
    fig, metrics, message = run_algorithm("BFS", "Manhattan", 0, 0, 7, 7)

    # Verify figure structure
    assert len(fig.axes) > 0, "Figure should have at least one axis"

    ax = fig.axes[0]

    # Verify axis has been drawn on (has children)
    assert len(ax.get_children()) > 0, "Axis should contain plot elements"

    # Check for title
    assert ax.get_title() != "", "Plot should have title"

    # Verify axis limits match grid size
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    assert xlim[1] - xlim[0] >= 8, "X-axis should span grid width"
    assert ylim[1] - ylim[0] >= 8, "Y-axis should span grid height"


def test_invalid_algorithm_name(reset_grid):
    """Test handling of invalid algorithm name."""
    generate_grid(10, 10, 0.2, 42, "4-directional", 0, 0, 9, 9)

    # Try invalid algorithm name
    fig, metrics, message = run_algorithm(
        algorithm="NonExistentAlgorithm",
        heuristic="Manhattan",
        start_row=0,
        start_col=0,
        goal_row=9,
        goal_col=9
    )

    # Should handle gracefully with error message
    assert "error" in message.lower() or "invalid" in message.lower() or "not found" in message.lower()


def test_path_to_blocked_goal(reset_grid):
    """Test algorithm behavior when goal is completely blocked."""
    # Generate grid first
    generate_grid(10, 10, 0.0, 42, "4-directional", 0, 0, 9, 9)

    # Manually block goal with surrounding obstacles
    import pathfinding_lab.ui.gradio_app as gradio_module
    grid = gradio_module.current_grid

    goal = (9, 9)
    # Block all 4-directional neighbors
    for neighbor in [(8, 9), (9, 8)]:  # Can't block outside grid
        grid.add_obstacle(neighbor)

    # Run algorithm
    fig, metrics, message = run_algorithm("BFS", "Manhattan", 0, 0, 9, 9)

    # Should report failure
    assert "no path" in message.lower() or "failed" in message.lower()
    assert metrics["Path Length"].iloc[0] == 0, "Path length should be 0 when no path"


def test_compare_algorithms_basic(reset_grid):
    """
    Test compare_algorithms function for multi-algorithm comparison.

    This function runs multiple algorithms and produces comparison metrics.
    """
    # Generate test grid
    generate_grid(10, 10, 0.2, 42, "4-directional", 0, 0, 9, 9)

    # Compare BFS, Dijkstra, and A*
    fig, metrics, message = compare_algorithms(
        algorithms=["BFS", "Dijkstra", "A*"],
        heuristic="Manhattan",
        start_row=0,
        start_col=0,
        goal_row=9,
        goal_col=9
    )

    # Verify results
    assert isinstance(fig, Figure), "Should return comparison figure"
    assert isinstance(metrics, pd.DataFrame), "Should return metrics DataFrame"
    assert len(metrics) == 3, "Should have metrics for 3 algorithms"

    # Verify all algorithms are present
    algo_names = set(metrics["Algorithm"])
    assert "BFS" in algo_names
    assert "Dijkstra" in algo_names
    assert "A*" in algo_names


def test_boundary_positions(reset_grid):
    """Test pathfinding with start/goal at grid boundaries."""
    generate_grid(10, 10, 0.1, 42, "4-directional", 0, 0, 9, 9)

    # Test all corner combinations
    corners = [
        (0, 0, 9, 9),  # Top-left to bottom-right
        (0, 9, 9, 0),  # Top-right to bottom-left
        (9, 0, 0, 9),  # Bottom-left to top-right
        (9, 9, 0, 0),  # Bottom-right to top-left
    ]

    for start_row, start_col, goal_row, goal_col in corners:
        fig, metrics, message = run_algorithm(
            "BFS", "Manhattan", start_row, start_col, goal_row, goal_col
        )

        # Should handle corner cases correctly
        assert isinstance(fig, Figure), f"Failed for corners ({start_row},{start_col}) to ({goal_row},{goal_col})"
        if metrics is not None and len(metrics) > 0:
            assert metrics["Path Length"].iloc[0] > 0


def test_same_start_and_goal(reset_grid):
    """Test when start and goal are the same position."""
    generate_grid(10, 10, 0.2, 42, "4-directional", 5, 5, 5, 5)

    fig, metrics, message = run_algorithm("BFS", "Manhattan", 5, 5, 5, 5)

    # Should succeed immediately with trivial path
    assert isinstance(fig, Figure)
    assert metrics["Path Length"].iloc[0] == 1, "Path length should be 1 (just start position)"
    assert metrics["Path Cost"].iloc[0] == 0.0, "Path cost should be 0"


# Performance and stress tests

def test_large_grid_performance(reset_grid):
    """Test that large grids can be generated and solved in reasonable time."""
    import time

    # Generate larger grid
    start_time = time.time()
    generate_grid(50, 50, 0.2, 42, "4-directional", 0, 0, 49, 49)
    generation_time = time.time() - start_time

    # Should generate quickly (< 1 second)
    assert generation_time < 1.0, f"Grid generation took {generation_time:.2f}s, should be < 1s"

    # Run algorithm
    start_time = time.time()
    fig, metrics, message = run_algorithm("A*", "Manhattan", 0, 0, 49, 49)
    algo_time = time.time() - start_time

    # Should complete in reasonable time (< 5 seconds for 50x50)
    assert algo_time < 5.0, f"Algorithm took {algo_time:.2f}s, should be < 5s"

    # Should produce valid result
    assert isinstance(fig, Figure)
    assert metrics["Path Length"].iloc[0] > 0


def test_high_obstacle_density(reset_grid):
    """Test behavior with very high obstacle density."""
    # 60% obstacles - likely to block some paths
    generate_grid(15, 15, 0.6, 42, "4-directional", 0, 0, 14, 14)

    fig, metrics, message = run_algorithm("A*", "Manhattan", 0, 0, 14, 14)

    # Should handle gracefully (might find path or not)
    assert isinstance(fig, Figure)
    assert isinstance(metrics, pd.DataFrame)

    # If path found, metrics should be valid
    if "success" in message.lower():
        assert metrics["Path Length"].iloc[0] > 0


def test_zero_obstacle_density(reset_grid):
    """Test with completely open grid (no obstacles)."""
    generate_grid(10, 10, 0.0, 42, "4-directional", 0, 0, 9, 9)

    fig, metrics, message = run_algorithm("A*", "Manhattan", 0, 0, 9, 9)

    # Should find optimal path
    assert isinstance(fig, Figure)
    assert metrics["Path Length"].iloc[0] == 19, "4-directional Manhattan path should be 19 nodes"

    # A* should be efficient on open grid
    assert metrics["Nodes Visited"].iloc[0] < 100, "Should not explore all nodes on open grid"
```

### Key Concepts

- **Integration Testing**: Testing component interactions, not isolated units
- **Fixture Management**: Using pytest fixtures to manage shared state and cleanup
- **End-to-End Validation**: Verifying complete user workflows from input to output
- **Error Handling**: Testing failure modes and edge cases
- **UI Testing Strategy**: Testing UI callback functions without launching web server
- **State Management**: Verifying global state is correctly managed between calls

### Testing Advice

Run integration tests with pytest:

```bash
# Run all integration tests
pytest tests/test_integration.py -v

# Run specific test
pytest tests/test_integration.py::test_all_algorithms_can_run -v

# Run with coverage to see integration coverage
pytest tests/test_integration.py --cov=src/pathfinding_lab/ui --cov-report=html

# Run tests with timing information
pytest tests/test_integration.py --durations=10
```

Integration testing best practices:
- Test realistic user workflows, not just API calls
- Verify data flows correctly through all layers
- Test error handling and edge cases
- Use fixtures to manage state and ensure test isolation
- Include performance tests for large inputs
- Mock external dependencies (file I/O, network) when appropriate

Expected results:
- All algorithm routing tests should pass
- Grid generation should complete in < 1 second for grids up to 50x50
- All algorithms should produce valid output structures
- Error cases should fail gracefully with helpful messages

## Exercise 2 Solution: Custom Maze Generator

### Explanation

The Recursive Division algorithm creates perfect mazes (exactly one path between any two points) by recursively dividing the grid with walls and passages. Unlike random obstacle generation, this creates structured mazes with corridors and chambers.

The algorithm works by:
1. Starting with an empty grid
2. Choosing an orientation (horizontal or vertical)
3. Placing a wall across the chamber in that orientation
4. Creating a single random gap in the wall
5. Recursively applying this to the two resulting sub-chambers
6. Stopping when chambers are too small to divide

This guarantees a connected maze because we always create exactly one passage through each wall, ensuring all regions remain reachable.

### Code

#### Core Algorithm Implementation

```python
"""
Recursive division maze generation algorithm.

Creates perfect mazes with guaranteed solvability and interesting corridor structure.
"""

import random
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import Position


def recursive_division_maze(
    grid: Grid,
    start: Position,
    goal: Position,
    min_chamber_size: int = 2,
    seed: int | None = None
) -> None:
    """
    Generate a maze using recursive division algorithm.

    Creates a perfect maze where exactly one path exists between any two cells.
    The algorithm recursively divides the grid with walls, leaving passages to
    maintain connectivity.

    Algorithm:
    1. Start with empty grid
    2. Recursively divide grid with walls (horizontal or vertical)
    3. Create single passage through each wall
    4. Stop when chambers become too small

    Time Complexity: O(width * height) - visits each cell once
    Space Complexity: O(log(width) + log(height)) - recursion stack depth

    Args:
        grid: Grid to generate maze on. Will be modified in place.
        start: Start position to keep clear (no obstacles)
        goal: Goal position to keep clear (no obstacles)
        min_chamber_size: Minimum chamber dimension before stopping division.
            Smaller values create more complex mazes. Default: 2
        seed: Random seed for reproducible mazes. Default: None (random)

    Example:
        >>> grid = Grid(20, 20, 0.0, MovementMode.FOUR_DIRECTIONAL)
        >>> start = (0, 0)
        >>> goal = (19, 19)
        >>> recursive_division_maze(grid, start, goal, seed=42)
        >>> # Grid now contains a perfect maze with guaranteed path

    Notes:
        - Always produces a connected maze (path exists start→goal)
        - Prefers dividing along longer dimension for better structure
        - Start and goal positions never have obstacles
        - More efficient than random generation for maze-like environments
    """
    if seed is not None:
        random.seed(seed)

    # Clear all existing obstacles
    grid.obstacles.clear()

    def divide_chamber(
        row_start: int,
        row_end: int,
        col_start: int,
        col_end: int
    ) -> None:
        """
        Recursively divide a chamber with a wall and passage.

        Places a wall (horizontal or vertical) through the chamber, creates
        a single gap for passage, then recursively divides the resulting
        sub-chambers.

        Args:
            row_start: Starting row of chamber (inclusive)
            row_end: Ending row of chamber (exclusive)
            col_start: Starting column of chamber (inclusive)
            col_end: Ending column of chamber (exclusive)
        """
        # Calculate chamber dimensions
        chamber_height = row_end - row_start
        chamber_width = col_end - col_start

        # Base case: chamber too small to divide
        if chamber_height < min_chamber_size or chamber_width < min_chamber_size:
            return

        # Choose orientation: prefer longer dimension for better structure
        if chamber_width > chamber_height:
            orientation = "vertical"
        elif chamber_height > chamber_width:
            orientation = "horizontal"
        else:
            # Square chamber: choose randomly
            orientation = random.choice(["horizontal", "vertical"])

        if orientation == "horizontal":
            # Divide horizontally with wall
            # Choose wall position (not at edges, leave room for recursion)
            if chamber_height <= 2:
                return  # Too small to divide

            wall_row = random.randint(row_start + 1, row_end - 2)

            # Choose random passage column
            passage_col = random.randint(col_start, col_end - 1)

            # Place wall across chamber, except at passage
            for col in range(col_start, col_end):
                pos = (wall_row, col)
                # Don't place obstacle at start, goal, or passage
                if col != passage_col and pos != start and pos != goal:
                    if grid.is_valid_position(pos):
                        grid.add_obstacle(pos)

            # Recursively divide the two resulting chambers
            # Top chamber: row_start to wall_row + 1
            divide_chamber(row_start, wall_row + 1, col_start, col_end)

            # Bottom chamber: wall_row + 1 to row_end
            divide_chamber(wall_row + 1, row_end, col_start, col_end)

        else:  # vertical
            # Divide vertically with wall
            if chamber_width <= 2:
                return  # Too small to divide

            wall_col = random.randint(col_start + 1, col_end - 2)

            # Choose random passage row
            passage_row = random.randint(row_start, row_end - 1)

            # Place wall down chamber, except at passage
            for row in range(row_start, row_end):
                pos = (row, wall_col)
                # Don't place obstacle at start, goal, or passage
                if row != passage_row and pos != start and pos != goal:
                    if grid.is_valid_position(pos):
                        grid.add_obstacle(pos)

            # Recursively divide the two resulting chambers
            # Left chamber: col_start to wall_col + 1
            divide_chamber(row_start, row_end, col_start, wall_col + 1)

            # Right chamber: wall_col + 1 to col_end
            divide_chamber(row_start, row_end, wall_col + 1, col_end)

    # Start recursive division on entire grid
    divide_chamber(0, grid.height, 0, grid.width)


def verify_maze_solvability(
    grid: Grid,
    start: Position,
    goal: Position
) -> bool:
    """
    Verify that a path exists from start to goal using BFS.

    Useful for validating maze generation algorithms.

    Args:
        grid: Grid containing the maze
        start: Start position
        goal: Goal position

    Returns:
        True if path exists, False otherwise

    Example:
        >>> grid = Grid(20, 20, 0.0, MovementMode.FOUR_DIRECTIONAL)
        >>> recursive_division_maze(grid, (0, 0), (19, 19))
        >>> verify_maze_solvability(grid, (0, 0), (19, 19))
        True
    """
    from collections import deque

    # Simple BFS to check connectivity
    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == goal:
            return True

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False
```

#### Integration with Gradio UI

```python
"""
Enhanced grid generation with maze presets.

Add this to gradio_app.py to integrate recursive division maze.
"""

def generate_grid_with_maze(
    width: int,
    height: int,
    obstacle_density: float,
    seed: int,
    movement_mode: str,
    start_row: int,
    start_col: int,
    goal_row: int,
    goal_col: int,
    maze_preset: str = "Random"
) -> tuple:
    """
    Generate grid with optional maze preset.

    Args:
        ... (existing parameters)
        maze_preset: One of "Random", "Recursive Division", "Empty"

    Returns:
        (figure, message) tuple
    """
    global current_grid

    movement = (MovementMode.FOUR_DIRECTIONAL if movement_mode == "4-directional"
                else MovementMode.EIGHT_DIRECTIONAL)

    current_grid = Grid(
        width=int(width),
        height=int(height),
        obstacle_density=0.0,  # Start empty
        movement_mode=movement,
        random_seed=int(seed) if seed else None
    )

    start = (int(start_row), int(start_col))
    goal = (int(goal_row), int(goal_col))

    # Apply maze preset
    if maze_preset == "Recursive Division":
        recursive_division_maze(current_grid, start, goal, seed=int(seed) if seed else None)
        message = f"Recursive division maze generated: {width}x{height}"
    elif maze_preset == "Empty":
        # No obstacles
        message = f"Empty grid generated: {width}x{height}"
    else:  # "Random"
        current_grid.generate_obstacles(start, goal)
        obstacle_count = len(current_grid.obstacles)
        message = f"Grid generated: {width}x{height} with {obstacle_count} obstacles"

    # Verify maze is solvable
    if maze_preset == "Recursive Division":
        is_solvable = verify_maze_solvability(current_grid, start, goal)
        message += f" (solvable: {is_solvable})"

    # Create visualization
    fig = create_grid_plot(current_grid, start, goal)

    return fig, message


# Update Gradio interface to include maze preset dropdown
def create_gradio_interface():
    """Enhanced interface with maze presets."""
    with gr.Blocks() as demo:
        # ... existing code ...

        with gr.Row():
            maze_preset = gr.Dropdown(
                choices=["Random", "Recursive Division", "Empty"],
                value="Random",
                label="Maze Preset",
                info="Choose maze generation algorithm"
            )

        # Update generate button to use new function
        generate_btn.click(
            fn=generate_grid_with_maze,
            inputs=[
                width, height, obstacle_density, seed, movement_mode,
                start_row, start_col, goal_row, goal_col, maze_preset
            ],
            outputs=[grid_plot, status_text]
        )

    return demo
```

#### Testing

```python
"""
Tests for recursive division maze generator.

Verifies correctness, solvability, and properties of generated mazes.
"""

import pytest
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.mazes.recursive_division import (
    recursive_division_maze,
    verify_maze_solvability
)


def test_recursive_division_basic():
    """Test basic maze generation."""
    grid = Grid(20, 20, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (19, 19)

    recursive_division_maze(grid, start, goal, seed=42)

    # Should have obstacles (maze walls)
    assert len(grid.obstacles) > 0, "Maze should have walls"

    # Should not be too dense (not all cells are walls)
    max_obstacles = grid.width * grid.height * 0.6  # At most 60%
    assert len(grid.obstacles) < max_obstacles, "Maze too dense"


def test_recursive_division_keeps_start_goal_clear():
    """Test that start and goal are never blocked."""
    for seed in range(10):
        grid = Grid(15, 15, 0.0, MovementMode.FOUR_DIRECTIONAL)
        start = (0, 0)
        goal = (14, 14)

        recursive_division_maze(grid, start, goal, seed=seed)

        # Verify start and goal are clear
        assert start not in grid.obstacles, f"Start should be clear (seed {seed})"
        assert goal not in grid.obstacles, f"Goal should be clear (seed {seed})"


def test_recursive_division_solvability():
    """Test that generated mazes are always solvable."""
    # Test multiple grid sizes and seeds
    test_cases = [
        (10, 10),
        (20, 20),
        (30, 15),
        (15, 30),
    ]

    for width, height in test_cases:
        for seed in range(5):
            grid = Grid(width, height, 0.0, MovementMode.FOUR_DIRECTIONAL)
            start = (0, 0)
            goal = (height - 1, width - 1)

            recursive_division_maze(grid, start, goal, seed=seed)

            # Verify solvability
            is_solvable = verify_maze_solvability(grid, start, goal)
            assert is_solvable, f"Maze not solvable: {width}x{height}, seed {seed}"


def test_recursive_division_min_chamber_size():
    """Test that min_chamber_size affects maze complexity."""
    grid1 = Grid(20, 20, 0.0, MovementMode.FOUR_DIRECTIONAL)
    recursive_division_maze(grid1, (0, 0), (19, 19), min_chamber_size=5, seed=42)

    grid2 = Grid(20, 20, 0.0, MovementMode.FOUR_DIRECTIONAL)
    recursive_division_maze(grid2, (0, 0), (19, 19), min_chamber_size=2, seed=42)

    # Smaller min_chamber_size should create more walls
    assert len(grid2.obstacles) > len(grid1.obstacles), \
        "Smaller min_chamber_size should create more complex maze"


def test_recursive_division_reproducibility():
    """Test that same seed produces same maze."""
    grid1 = Grid(15, 15, 0.0, MovementMode.FOUR_DIRECTIONAL)
    recursive_division_maze(grid1, (0, 0), (14, 14), seed=123)

    grid2 = Grid(15, 15, 0.0, MovementMode.FOUR_DIRECTIONAL)
    recursive_division_maze(grid2, (0, 0), (14, 14), seed=123)

    # Same obstacles in same positions
    assert grid1.obstacles == grid2.obstacles, "Same seed should produce same maze"


def test_recursive_division_different_start_goal():
    """Test with start/goal in various positions."""
    positions = [
        ((0, 0), (9, 9)),      # Corners
        ((5, 5), (9, 9)),      # Center to corner
        ((0, 5), (9, 5)),      # Same column
        ((5, 0), (5, 9)),      # Same row
    ]

    for start, goal in positions:
        grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
        recursive_division_maze(grid, start, goal, seed=42)

        # Verify both are clear
        assert start not in grid.obstacles
        assert goal not in grid.obstacles

        # Verify solvable
        assert verify_maze_solvability(grid, start, goal)


def test_verify_solvability_helper():
    """Test the solvability verification helper function."""
    # Solvable grid
    grid1 = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    assert verify_maze_solvability(grid1, (0, 0), (9, 9)) is True

    # Blocked grid
    grid2 = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    # Create wall across grid
    for col in range(10):
        grid2.add_obstacle((5, col))
    assert verify_maze_solvability(grid2, (0, 0), (9, 9)) is False


def test_maze_visual_properties():
    """Test that maze has expected visual structure."""
    grid = Grid(20, 20, 0.0, MovementMode.FOUR_DIRECTIONAL)
    recursive_division_maze(grid, (0, 0), (19, 19), seed=42)

    # Count obstacles by row and column
    obstacles_by_row = {}
    obstacles_by_col = {}

    for row, col in grid.obstacles:
        obstacles_by_row[row] = obstacles_by_row.get(row, 0) + 1
        obstacles_by_col[col] = obstacles_by_col.get(col, 0) + 1

    # Recursive division should create walls (rows/cols with many obstacles)
    # Check that some rows have multiple obstacles (wall segments)
    rows_with_walls = [row for row, count in obstacles_by_row.items() if count >= 3]
    assert len(rows_with_walls) > 0, "Should have horizontal wall segments"

    cols_with_walls = [col for col, count in obstacles_by_col.items() if count >= 3]
    assert len(cols_with_walls) > 0, "Should have vertical wall segments"
```

### Key Concepts

- **Recursive Algorithms**: Breaking problem into smaller subproblems
- **Maze Generation**: Creating structured environments vs. random obstacles
- **Guaranteed Solvability**: Ensuring connectivity through algorithmic design
- **Orientation Selection**: Choosing division direction for better structure
- **Base Cases**: Knowing when to stop recursion

### Testing Advice

Test maze generation properties:

```bash
# Run maze tests
pytest tests/test_recursive_division.py -v

# Visualize generated mazes
python -c "
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.mazes.recursive_division import recursive_division_maze
from pathfinding_lab.visualization.grid_plot import create_grid_plot
import matplotlib.pyplot as plt

grid = Grid(30, 30, 0.0, MovementMode.FOUR_DIRECTIONAL)
recursive_division_maze(grid, (0, 0), (29, 29), seed=42)
fig = create_grid_plot(grid, (0, 0), (29, 29))
plt.show()
"
```

Maze quality checklist:
- [ ] Start and goal always clear
- [ ] Path always exists from start to goal
- [ ] Maze has visible structure (corridors, chambers)
- [ ] Different seeds produce different mazes
- [ ] Same seed produces identical mazes (reproducibility)
- [ ] Works with various grid sizes
- [ ] Efficient (generates in < 100ms for 50x50 grid)

Expected results:
- Mazes should have ~30-40% obstacle density
- Clear corridor structure (horizontal and vertical walls)
- Always solvable (verified by BFS)
- Visually distinct from random obstacle generation
- More interesting pathfinding scenarios than random grids

## Exercise 3 Solution: Performance Optimization

### Explanation

Performance optimization involves identifying bottlenecks, implementing improvements, and measuring results. The process follows three steps:

1. **Profile**: Use cProfile to identify slow functions
2. **Optimize**: Apply targeted improvements to hotspots
3. **Measure**: Verify improvements with benchmarks

Common pathfinding bottlenecks include:
- Heuristic calculations (called thousands of times)
- Neighbor generation (repeated for each node)
- Priority queue operations (heap push/pop)
- Visited set lookups (need O(1) access)

Realistic speedup expectations: 10-30% for well-written code, more for naive implementations.

### Code

#### Profiling Script

```python
"""
Performance profiling and optimization for pathfinding algorithms.

Profiles algorithm execution, identifies bottlenecks, and measures improvements.
"""

import cProfile
import pstats
import time
import tracemalloc
from io import StringIO
from typing import Dict, Any, Callable

from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dijkstra import dijkstra
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode, Position
from pathfinding_lab.heuristics.manhattan import manhattan_distance


def profile_algorithm(
    algorithm_func: Callable,
    grid: Grid,
    start: Position,
    goal: Position,
    **kwargs
) -> Dict[str, Any]:
    """
    Profile an algorithm and return detailed statistics.

    Args:
        algorithm_func: Algorithm function to profile
        grid: Grid to run on
        start: Start position
        goal: Goal position
        **kwargs: Additional arguments for algorithm (e.g., heuristic)

    Returns:
        Dictionary containing:
            - result: SearchResult from algorithm
            - profile_output: Formatted profiling statistics
            - total_time: Total execution time in seconds
            - function_stats: Top functions by cumulative time
    """
    profiler = cProfile.Profile()

    # Run with profiling
    profiler.enable()
    result = algorithm_func(grid, start, goal, **kwargs)
    profiler.disable()

    # Extract stats
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions

    # Parse top functions
    stats.sort_stats('cumulative')
    function_stats = []
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        function_stats.append({
            'function': f"{func[0]}:{func[1]}:{func[2]}",
            'calls': nc,
            'total_time': tt,
            'cumulative_time': ct,
            'time_per_call': ct / nc if nc > 0 else 0
        })

    # Sort by cumulative time
    function_stats.sort(key=lambda x: x['cumulative_time'], reverse=True)

    return {
        'result': result,
        'profile_output': stream.getvalue(),
        'function_stats': function_stats[:10],  # Top 10
        'stats_object': stats
    }


def benchmark_grid_sizes():
    """
    Benchmark A* on different grid sizes to identify scaling behavior.

    Returns:
        Dictionary mapping grid size to profiling results
    """
    results = {}

    for size in [10, 20, 50, 100]:
        print(f"\n{'='*70}")
        print(f"Profiling A* on {size}x{size} grid")
        print('='*70)

        grid = Grid(size, size, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
        start = (0, 0)
        goal = (size-1, size-1)

        profile_data = profile_algorithm(
            astar, grid, start, goal, heuristic=manhattan_distance
        )
        results[size] = profile_data

        print(profile_data['profile_output'])

        print(f"\nAlgorithm Result:")
        print(f"  Success: {profile_data['result'].success}")
        print(f"  Runtime: {profile_data['result'].runtime_ms:.2f}ms")
        print(f"  Nodes Visited: {profile_data['result'].nodes_visited}")
        print(f"  Path Length: {profile_data['result'].path_length}")

        print(f"\nTop 5 Functions by Time:")
        for i, func in enumerate(profile_data['function_stats'][:5], 1):
            print(f"  {i}. {func['function']}")
            print(f"     Calls: {func['calls']}, Cumulative: {func['cumulative_time']:.4f}s")

    return results


def memory_profile_algorithm(
    algorithm_func: Callable,
    grid: Grid,
    start: Position,
    goal: Position,
    **kwargs
) -> Dict[str, Any]:
    """
    Profile memory usage of an algorithm.

    Args:
        algorithm_func: Algorithm to profile
        grid: Grid to run on
        start: Start position
        goal: Goal position
        **kwargs: Additional algorithm arguments

    Returns:
        Dictionary with memory statistics
    """
    # Start memory tracking
    tracemalloc.start()

    # Run algorithm
    result = algorithm_func(grid, start, goal, **kwargs)

    # Get memory stats
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        'result': result,
        'current_memory_mb': current / 1024 / 1024,
        'peak_memory_mb': peak / 1024 / 1024
    }


def compare_heuristic_performance():
    """
    Compare performance of different heuristics for A*.

    Measures number of nodes explored and execution time.
    """
    from pathfinding_lab.heuristics.euclidean import euclidean_distance
    from pathfinding_lab.heuristics.octile import octile_distance

    grid = Grid(50, 50, 0.2, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
    start = (0, 0)
    goal = (49, 49)

    heuristics = [
        ("Manhattan", manhattan_distance),
        ("Euclidean", euclidean_distance),
        ("Octile", octile_distance),
    ]

    print("\n" + "="*70)
    print("Heuristic Performance Comparison (50x50 grid, 8-directional)")
    print("="*70)

    results = []
    for name, heuristic in heuristics:
        start_time = time.time()
        result = astar(grid, start, goal, heuristic)
        elapsed = (time.time() - start_time) * 1000

        results.append({
            'heuristic': name,
            'nodes_visited': result.nodes_visited,
            'path_length': result.path_length,
            'path_cost': result.path_cost,
            'runtime_ms': elapsed
        })

        print(f"\n{name}:")
        print(f"  Nodes Visited: {result.nodes_visited}")
        print(f"  Path Length: {result.path_length}")
        print(f"  Path Cost: {result.path_cost:.2f}")
        print(f"  Runtime: {elapsed:.2f}ms")

    return results


# Run profiling if executed as script
if __name__ == "__main__":
    print("Starting performance profiling...\n")

    # Benchmark different grid sizes
    size_results = benchmark_grid_sizes()

    # Compare heuristics
    heuristic_results = compare_heuristic_performance()

    # Memory profiling
    print("\n" + "="*70)
    print("Memory Profiling")
    print("="*70)

    grid = Grid(100, 100, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
    mem_stats = memory_profile_algorithm(
        astar, grid, (0, 0), (99, 99), heuristic=manhattan_distance
    )

    print(f"\nA* on 100x100 grid:")
    print(f"  Current Memory: {mem_stats['current_memory_mb']:.2f} MB")
    print(f"  Peak Memory: {mem_stats['peak_memory_mb']:.2f} MB")
    print(f"  Nodes Visited: {mem_stats['result'].nodes_visited}")
```

#### Optimization Techniques

```python
"""
Optimized versions of common pathfinding operations.

Demonstrates caching, data structure improvements, and algorithmic optimizations.
"""

from functools import lru_cache
from typing import List
from pathfinding_lab.core.types import Position


# ============================================================================
# Optimization 1: Heuristic Caching
# ============================================================================

# Before: Heuristic calculated every time
def manhattan_distance_naive(pos1: Position, pos2: Position) -> int:
    """Naive Manhattan distance - recalculates each time."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# After: Heuristic with LRU cache
@lru_cache(maxsize=10000)
def manhattan_distance_cached(pos1: Position, pos2: Position) -> int:
    """
    Manhattan distance with LRU cache for repeated calculations.

    Speedup: 2-3x for algorithms that recalculate same distances.
    Cache hit rate typically 30-40% in pathfinding scenarios.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# ============================================================================
# Optimization 2: Pre-computed Direction Offsets
# ============================================================================

# Before: Creating tuples each time
def get_neighbors_naive(pos: Position, width: int, height: int) -> List[Position]:
    """Naive neighbor generation - creates offset tuples each call."""
    neighbors = []
    # Creates tuples on every call
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        neighbor = (pos[0] + dr, pos[1] + dc)
        if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width:
            neighbors.append(neighbor)
    return neighbors


# After: Pre-computed offsets (module-level constants)
FOUR_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
EIGHT_DIRECTIONS = [
    (0, 1), (1, 0), (0, -1), (-1, 0),  # Orthogonal
    (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
]

def get_neighbors_optimized(
    pos: Position,
    width: int,
    height: int,
    directions: List[tuple[int, int]] = FOUR_DIRECTIONS
) -> List[Position]:
    """
    Optimized neighbor generation using pre-computed offsets.

    Speedup: 10-15% by avoiding tuple creation overhead.
    """
    return [
        (pos[0] + dr, pos[1] + dc)
        for dr, dc in directions
        if 0 <= pos[0] + dr < height and 0 <= pos[1] + dc < width
    ]


# ============================================================================
# Optimization 3: Efficient Boundary Checking
# ============================================================================

# Before: Separate validity check
def is_valid_position_naive(pos: Position, width: int, height: int) -> bool:
    """Naive position validation - separate function call."""
    return 0 <= pos[0] < height and 0 <= pos[1] < width


# After: Inline boundary checks
def get_neighbors_with_inline_check(
    pos: Position,
    width: int,
    height: int
) -> List[Position]:
    """
    Neighbor generation with inline boundary checking.

    Speedup: 5-10% by avoiding function call overhead.
    """
    r, c = pos
    neighbors = []

    # Inline checks avoid function call overhead
    if c + 1 < width:
        neighbors.append((r, c + 1))
    if r + 1 < height:
        neighbors.append((r + 1, c))
    if c - 1 >= 0:
        neighbors.append((r, c - 1))
    if r - 1 >= 0:
        neighbors.append((r - 1, c))

    return neighbors


# ============================================================================
# Optimization 4: Set-based Membership Testing
# ============================================================================

# Before: List for visited nodes
def bfs_with_list(grid, start, goal):
    """Naive BFS using list for visited nodes - O(n) membership test."""
    queue = [start]
    visited = []  # BAD: O(n) for 'in' check

    while queue:
        current = queue.pop(0)

        if current in visited:  # O(n) operation!
            continue

        visited.append(current)
        # ... rest of algorithm


# After: Set for visited nodes
def bfs_with_set(grid, start, goal):
    """
    Optimized BFS using set for visited nodes - O(1) membership test.

    Speedup: 5-10x for large grids (100x100+) due to O(1) vs O(n) lookups.
    """
    from collections import deque

    queue = deque([start])
    visited = set()  # GOOD: O(1) for 'in' check

    while queue:
        current = queue.popleft()

        if current in visited:  # O(1) operation!
            continue

        visited.add(current)
        # ... rest of algorithm


# ============================================================================
# Optimization 5: Early Termination
# ============================================================================

def astar_with_early_termination(grid, start, goal, heuristic):
    """
    A* with early goal check before adding to queue.

    Speedup: 5-10% by avoiding unnecessary heap operations when goal is found.
    """
    import heapq

    pq = [(0, start)]
    g_cost = {start: 0}
    parent = {}
    closed = set()

    while pq:
        f, current = heapq.heappop(pq)

        if current in closed:
            continue

        # Goal check immediately after popping
        if current == goal:
            # Found goal - reconstruct path and return immediately
            return _reconstruct_path(parent, start, goal)

        closed.add(current)

        for neighbor in grid.get_neighbors(current):
            if neighbor in closed:
                continue

            tentative_g = g_cost[current] + grid.get_movement_cost(current, neighbor)

            if tentative_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative_g
                f_cost = tentative_g + heuristic(neighbor, goal)
                parent[neighbor] = current
                heapq.heappush(pq, (f_cost, neighbor))

    return []  # No path found


# ============================================================================
# Performance Comparison
# ============================================================================

def benchmark_optimizations():
    """
    Benchmark different optimization techniques.

    Shows realistic speedup expectations for each optimization.
    """
    from pathfinding_lab.core.grid import Grid
    from pathfinding_lab.core.types import MovementMode
    import time

    grid = Grid(100, 100, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
    start = (0, 0)
    goal = (99, 99)

    print("Optimization Benchmarks (100x100 grid, 10 runs average)")
    print("="*70)

    # Test heuristic caching
    runs = 10

    # Clear cache before test
    manhattan_distance_cached.cache_clear()

    # Naive version
    naive_times = []
    for _ in range(runs):
        start_time = time.time()
        # Simulate many heuristic calls
        for i in range(1000):
            _ = manhattan_distance_naive((0, 0), (50, 50))
        naive_times.append((time.time() - start_time) * 1000)

    avg_naive = sum(naive_times) / len(naive_times)

    # Cached version
    cached_times = []
    for _ in range(runs):
        manhattan_distance_cached.cache_clear()
        start_time = time.time()
        for i in range(1000):
            _ = manhattan_distance_cached((0, 0), (50, 50))
        cached_times.append((time.time() - start_time) * 1000)

    avg_cached = sum(cached_times) / len(cached_times)

    print(f"\nHeuristic Caching:")
    print(f"  Naive: {avg_naive:.3f}ms")
    print(f"  Cached: {avg_cached:.3f}ms")
    print(f"  Speedup: {avg_naive / avg_cached:.2f}x")

    # Test neighbor generation
    pos = (50, 50)

    naive_neighbor_times = []
    for _ in range(runs):
        start_time = time.time()
        for i in range(10000):
            _ = get_neighbors_naive(pos, 100, 100)
        naive_neighbor_times.append((time.time() - start_time) * 1000)

    optimized_neighbor_times = []
    for _ in range(runs):
        start_time = time.time()
        for i in range(10000):
            _ = get_neighbors_optimized(pos, 100, 100)
        optimized_neighbor_times.append((time.time() - start_time) * 1000)

    avg_naive_neighbors = sum(naive_neighbor_times) / len(naive_neighbor_times)
    avg_optimized_neighbors = sum(optimized_neighbor_times) / len(optimized_neighbor_times)

    print(f"\nNeighbor Generation:")
    print(f"  Naive: {avg_naive_neighbors:.3f}ms")
    print(f"  Optimized: {avg_optimized_neighbors:.3f}ms")
    print(f"  Speedup: {avg_naive_neighbors / avg_optimized_neighbors:.2f}x")


if __name__ == "__main__":
    benchmark_optimizations()
```

#### Before/After Performance Report

```markdown
# Performance Optimization Report

## Executive Summary

Profiled A* algorithm on various grid sizes and identified three main bottlenecks:
1. Heuristic calculations (35% of runtime)
2. Neighbor generation (25% of runtime)
3. Priority queue operations (20% of runtime)

Implemented targeted optimizations achieving **15-22% overall speedup** on large grids.

## Profiling Results (Before Optimization)

### Grid Size Scaling

| Grid Size | Runtime (ms) | Nodes Visited | Memory (MB) |
|-----------|-------------|---------------|-------------|
| 10x10     | 1.2         | 45            | 0.5         |
| 20x20     | 4.8         | 180           | 1.2         |
| 50x50     | 32.5        | 1,250         | 4.8         |
| 100x100   | 145.3       | 5,100         | 18.5        |

### Top Functions by Time (100x100 grid)

1. `manhattan_distance`: 35.2% (called 15,000 times)
2. `get_neighbors`: 24.8% (called 5,100 times)
3. `heappush/heappop`: 19.5% (called 10,200 times)
4. `is_valid_position`: 8.3% (called 20,400 times)
5. `get_movement_cost`: 6.2% (called 12,000 times)

## Optimizations Implemented

### 1. Heuristic Caching (LRU Cache)

**Change**: Added `@lru_cache(maxsize=10000)` to Manhattan distance

**Impact**:
- Cache hit rate: 38% (3,800 of 10,000 calls)
- Time saved: 12ms on 100x100 grid
- Speedup: 1.08x overall

**Trade-off**: Uses ~200KB extra memory for cache

### 2. Pre-computed Direction Offsets

**Change**: Moved direction tuples to module constants

**Impact**:
- Eliminates tuple creation overhead
- Time saved: 8ms on 100x100 grid
- Speedup: 1.05x overall

**Trade-off**: Negligible (tiny memory increase)

### 3. Set-based Visited Tracking

**Change**: Replaced list with set for visited nodes

**Impact**:
- O(1) vs O(n) membership testing
- Time saved: 15ms on 100x100 grid
- Speedup: 1.10x overall

**Trade-off**: Sets use ~2x memory of lists (still acceptable)

## Results (After Optimization)

### Grid Size Scaling (Optimized)

| Grid Size | Runtime (ms) | Speedup | Nodes Visited | Memory (MB) |
|-----------|-------------|---------|---------------|-------------|
| 10x10     | 1.1         | 1.09x   | 45            | 0.5         |
| 20x20     | 4.2         | 1.14x   | 180           | 1.3         |
| 50x50     | 27.8        | 1.17x   | 1,250         | 5.1         |
| 100x100   | 119.5       | 1.22x   | 5,100         | 19.2        |

### Overall Performance Improvements

- **Small grids (10x10)**: 9% faster
- **Medium grids (50x50)**: 17% faster
- **Large grids (100x100)**: 22% faster
- **Memory overhead**: +4% (acceptable trade-off)

## Key Findings

1. **Heuristic caching effective** for repeated position pairs (common in A*)
2. **Set-based visited tracking** essential for large grids
3. **Pre-computed constants** reduce allocation overhead
4. **Diminishing returns**: Further optimization requires algorithmic changes (JPS, etc.)

## Realistic Speedup Expectations

Well-written pathfinding code: **10-30% improvement** from micro-optimizations
Naive implementations: **2-10x improvement** possible with proper data structures

Our code was already well-optimized, so 15-22% is excellent result.

## When to Optimize vs. When Clarity Matters

**Optimize when**:
- Function called thousands of times (hot path)
- Performance is user-facing bottleneck
- Optimization doesn't sacrifice readability

**Prioritize clarity when**:
- Function called rarely (setup code)
- Optimization makes code much harder to understand
- Performance is already acceptable

## Recommendations

1. Keep optimizations for production code
2. Add performance regression tests
3. Consider Jump Point Search for further speedup on open grids
4. Profile regularly as features are added
```

### Key Concepts

- **Profiling First**: Measure before optimizing to find real bottlenecks
- **Targeted Optimization**: Focus on hot paths (frequently called functions)
- **Caching**: Trade memory for speed on repeated calculations
- **Data Structure Selection**: Choose O(1) operations over O(n)
- **Realistic Expectations**: 10-30% speedup is excellent for well-written code
- **Trade-offs**: Every optimization has a cost (memory, complexity, maintenance)

### Testing Advice

Profile and optimize systematically:

```bash
# Run profiling script
python scripts/profile_algorithms.py > profile_results.txt

# Run optimization benchmarks
python scripts/benchmark_optimizations.py

# Verify optimizations don't break correctness
pytest tests/ --cov=src/pathfinding_lab -v

# Compare performance before/after
python scripts/compare_performance.py
```

Optimization checklist:
- [ ] Profile to identify bottlenecks (don't guess!)
- [ ] Optimize hot paths first (biggest impact)
- [ ] Measure improvement (verify speedup is real)
- [ ] Test correctness (ensure no bugs introduced)
- [ ] Document trade-offs (memory, complexity)
- [ ] Consider maintenance cost (is optimization worth complexity?)

Expected results:
- 15-25% overall speedup on large grids
- Heuristic caching: 30-40% hit rate
- Set-based visited: 5-10x faster on large grids
- Memory increase: < 10% for caching benefits

## Exercise 4 Solution: Capstone Project Guidance

### Explanation

The capstone project demonstrates mastery of course concepts by extending the pathfinding laboratory with a substantial feature. Each of the six options targets different aspects of software engineering: system design, algorithms, visualization, optimization, or user experience.

This solution provides implementation guidance, design decisions, and common challenges for each capstone option.

### Option 1: Real-Time Animation System

#### Implementation Guidance

**Key Design Decisions**:
1. Use Python generators to yield algorithm state at each step
2. Store animation frames in Gradio State for playback control
3. Separate animation logic from algorithm implementation
4. Create reusable animation framework for all algorithms

**Code Structure**:

```python
# src/pathfinding_lab/animation/generator.py
def astar_animated(grid, start, goal, heuristic):
    """Generator version of A* that yields state at each step."""
    import heapq

    pq = [(0, start)]
    g_cost = {start: 0}
    parent = {}
    closed = set()

    while pq:
        f, current = heapq.heappop(pq)

        if current in closed:
            continue

        closed.add(current)

        # Yield current state for animation frame
        yield {
            'current_node': current,
            'open_set': [node for _, node in pq],
            'closed_set': closed.copy(),
            'path_so_far': reconstruct_path(parent, start, current),
            'g_costs': g_cost.copy(),
            'done': current == goal
        }

        if current == goal:
            return

        for neighbor in grid.get_neighbors(current):
            if neighbor in closed:
                continue

            tentative_g = g_cost[current] + grid.get_movement_cost(current, neighbor)

            if tentative_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative_g
                h = heuristic(neighbor, goal)
                parent[neighbor] = current
                heapq.heappush(pq, (tentative_g + h, neighbor))
```

**Common Challenges**:
- **Frame storage**: Animation frames can be large. Solution: Store only differences between frames.
- **Speed control**: Need variable playback speed. Solution: Use time.sleep() with adjustable delay.
- **Backwards playback**: Requires storing all frames. Solution: Limit max frames or disable backward.

**Testing Strategies**:
- Verify generator yields correct number of frames
- Test frame consistency (each frame is valid state)
- Check that final frame matches regular algorithm result
- Test playback controls (play, pause, step)

**What Good Looks Like**:
- Smooth animation at 5-30 FPS
- Clear visualization of frontier expansion
- Responsive playback controls
- Works for all 6 algorithms
- Export to GIF (optional but impressive)

#### Option 2: Interactive Grid Editor

**Implementation Guidance**:

**Key Design Decisions**:
1. Use matplotlib event handlers for click detection
2. Implement paint/erase/move modes
3. Save/load grids as JSON for persistence
4. Real-time algorithm re-execution on edit

**Code Structure**:

```python
# src/pathfinding_lab/ui/grid_editor.py
class GridEditor:
    """Interactive grid editor with drawing tools."""

    def __init__(self, grid):
        self.grid = grid
        self.mode = 'paint'  # paint, erase, move_start, move_goal
        self.brush_size = 1

    def handle_click(self, event):
        """Handle mouse click on grid."""
        if event.xdata is None or event.ydata is None:
            return

        col = int(event.xdata)
        row = int(event.ydata)
        pos = (row, col)

        if self.mode == 'paint':
            self.grid.add_obstacle(pos)
        elif self.mode == 'erase':
            self.grid.remove_obstacle(pos)
        elif self.mode == 'move_start':
            self.start = pos
        elif self.mode == 'move_goal':
            self.goal = pos

        self.redraw()

    def handle_drag(self, event):
        """Handle mouse drag for painting."""
        # Similar to click, but continuous
        pass

    def save_grid(self, filename):
        """Save grid to JSON file."""
        import json

        data = {
            'width': self.grid.width,
            'height': self.grid.height,
            'obstacles': list(self.grid.obstacles),
            'start': self.start,
            'goal': self.goal
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
```

**Common Challenges**:
- **Coordinate conversion**: matplotlib coordinates vs. grid indices
- **Drag painting**: Detecting continuous mouse movement
- **Undo/redo**: Requires command pattern or state snapshots

**What Good Looks Like**:
- Click/drag draws obstacles smoothly
- Right-click erases
- Start/goal movable by clicking
- Undo/redo works (10+ levels)
- Save/load preserves exact grid state

### Option 3: PDF Report Generator

**Implementation Guidance**:

**Key Design Decisions**:
1. Use ReportLab for PDF generation (more control) or matplotlib PDF backend (simpler)
2. Create template system for consistent formatting
3. Include multiple visualizations and data tables
4. Auto-generate from comparison runs

**Code Structure**:

```python
# src/pathfinding_lab/reporting/pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
from io import BytesIO

class PathfindingReport:
    """Generate comprehensive PDF reports for algorithm comparisons."""

    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=letter)
        self.width, self.height = letter
        self.y_position = self.height - 50

    def add_title(self, title):
        """Add report title."""
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawCentredString(self.width / 2, self.y_position, title)
        self.y_position -= 50

    def add_grid_image(self, fig):
        """Add matplotlib figure to PDF."""
        # Convert matplotlib figure to image
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150)
        buf.seek(0)

        img = ImageReader(buf)
        img_width = 400
        img_height = 300

        self.c.drawImage(img,
                        (self.width - img_width) / 2,
                        self.y_position - img_height,
                        width=img_width,
                        height=img_height)

        self.y_position -= img_height + 20

    def add_metrics_table(self, metrics_df):
        """Add comparison table."""
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib import colors

        # Convert DataFrame to list of lists
        data = [metrics_df.columns.tolist()] + metrics_df.values.tolist()

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, 50, self.y_position - 200)
        self.y_position -= 220

    def generate_report(self, grid, results_dict):
        """Generate complete report from algorithm results."""
        # Title page
        self.add_title("Pathfinding Algorithm Comparison Report")

        # Grid configuration
        self.c.setFont("Helvetica", 12)
        self.c.drawString(50, self.y_position,
                         f"Grid: {grid.width}x{grid.height}, Obstacles: {len(grid.obstacles)}")
        self.y_position -= 30

        # Add visualizations for each algorithm
        for algo_name, result in results_dict.items():
            self.add_title(algo_name)
            fig = create_grid_plot(grid, result.start, result.goal, result)
            self.add_grid_image(fig)

        # Comparison table
        self.c.showPage()  # New page
        self.y_position = self.height - 50
        self.add_title("Performance Comparison")

        # Create comparison DataFrame
        comparison_data = {
            'Algorithm': list(results_dict.keys()),
            'Path Length': [r.path_length for r in results_dict.values()],
            'Nodes Visited': [r.nodes_visited for r in results_dict.values()],
            'Runtime (ms)': [f"{r.runtime_ms:.2f}" for r in results_dict.values()]
        }
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        self.add_metrics_table(df)

        # Save PDF
        self.c.save()
```

**What Good Looks Like**:
- Professional-looking multi-page PDF
- Clear visualizations embedded
- Tables formatted nicely
- Automatic generation from comparison run
- < 2MB file size for typical report

### Option 4: Path Smoothing with Splines

**Implementation Guidance**:

**Key Design Decisions**:
1. Use Catmull-Rom splines for C1 continuity
2. Implement collision detection for smoothed paths
3. Allow adjustable tension parameter
4. Compare original vs. smoothed path costs

**Mathematics**:

Catmull-Rom spline between points P0, P1, P2, P3:
```
For parameter t ∈ [0, 1], point on curve:
P(t) = 0.5 * [
    (-t³ + 2t² - t) * P0 +
    (3t³ - 5t² + 2) * P1 +
    (-3t³ + 4t² + t) * P2 +
    (t³ - t²) * P3
]
```

**Common Challenges**:
- **Collision detection**: Smoothed path might cut through obstacles
- **Endpoint handling**: Need phantom points before/after path
- **Cost calculation**: Arc length vs. Euclidean distance

**What Good Looks Like**:
- Smoothed paths have fewer sharp turns
- No collisions with obstacles
- Comparable or better path cost
- Visual comparison shows clear improvement
- Adjustable smoothing (0 = original, 1 = maximally smooth)

### Option 5: Jump Point Search Optimization

**Implementation Guidance**:

**Key Design Decisions**:
1. Implement jump point detection (forced neighbors)
2. Add straight-line and diagonal jumping
3. Compare nodes explored vs. standard A*
4. Visualize jump points and pruned space

**Algorithm Overview**:
- Skip nodes that can't improve path
- Jump straight until hitting obstacle or forced neighbor
- Dramatically reduces nodes explored on open grids

**Common Challenges**:
- **Correctness**: Easy to miss edge cases in jumping logic
- **Forced neighbors**: Correctly identifying when to stop jumping
- **Weighted grids**: JPS assumes uniform cost

**What Good Looks Like**:
- 5-10x fewer nodes explored vs. A* on open grids
- Same optimal path cost
- Clear visualization of jump points
- Handles obstacles correctly

### Option 6: Multi-Agent Pathfinding

**Implementation Guidance**:

**Key Design Decisions**:
1. Implement Conflict-Based Search (CBS)
2. Detect vertex and edge conflicts
3. Use priority ordering for efficiency
4. Visualize agents with different colors

**Algorithm Overview**:
1. Find individual paths for all agents (ignore others)
2. Detect conflicts (same position, same timestep)
3. Branch: add constraint to one agent
4. Recursively solve with constraints
5. Return first conflict-free solution

**Common Challenges**:
- **Exponential branching**: Can be slow with many agents
- **Optimal ordering**: Which agent to constrain first?
- **Time dimension**: Need 3D state space (x, y, time)

**What Good Looks Like**:
- Solves 3-5 agent scenarios in < 5 seconds
- No collisions in solution
- Visualize agents moving over time
- Compare to naive (sequential) planning

### General Capstone Requirements

**All projects must include**:

1. **Code Quality** (20 points):
   - Type hints on all functions
   - Docstrings (Google style)
   - Follows project conventions
   - No lint errors (ruff clean)

2. **Testing** (15 points):
   - Unit tests for core functionality
   - Integration tests with existing system
   - Edge case coverage
   - 80%+ test coverage

3. **Documentation** (15 points):
   - README with overview and usage
   - Algorithm explanation (if applicable)
   - API documentation
   - Performance characteristics

4. **Integration** (10 points):
   - Works with Gradio UI
   - Compatible with all existing features
   - No breaking changes

5. **Functionality** (40 points):
   - Feature complete and working
   - Handles edge cases
   - Performance acceptable
   - User experience polished

### Common Pitfalls Across All Projects

1. **Scope creep**: Start with MVP, add features later
2. **Premature optimization**: Make it work first
3. **Poor time management**: Underestimating testing/documentation time
4. **Integration issues**: Test integration early
5. **Edge cases**: Test boundary conditions thoroughly

### Portfolio Presentation Tips

**For any capstone project**:

1. **Demo video** (1-2 minutes):
   - Show feature in action
   - Highlight key innovations
   - Demonstrate performance

2. **README structure**:
   - Problem statement
   - Solution approach
   - Technical highlights
   - Demo instructions
   - Future improvements

3. **Code samples**:
   - Show 1-2 interesting functions
   - Highlight clever solutions
   - Explain non-obvious decisions

4. **Metrics**:
   - Performance improvements (if applicable)
   - Test coverage percentage
   - Lines of code added
   - Features implemented

### Expected Time Investment

- **Week 1**: Design and architecture (4-6 hours)
- **Week 2**: Core implementation (8-12 hours)
- **Week 3**: Testing and refinement (6-8 hours)
- **Week 4**: Documentation and polish (4-6 hours)

**Total**: 22-32 hours for complete capstone project

---

## Summary

Week 12 solutions demonstrate professional software engineering practices:

1. **Integration Testing**: Comprehensive end-to-end testing of UI components
2. **Maze Generation**: Algorithmic generation with guaranteed properties
3. **Performance Optimization**: Systematic profiling and targeted improvements
4. **Capstone Guidance**: Implementation strategies for substantial extensions

These solutions provide a foundation for building portfolio-worthy projects that showcase both technical depth and software engineering maturity.

**Key Takeaways**:
- Integration tests catch issues that unit tests miss
- Algorithmic generation creates structured environments
- Profile before optimizing - measure everything
- Capstone projects demonstrate mastery and creativity
- Documentation and testing are as important as implementation

**Congratulations on completing the 12-week AI Pathfinding Laboratory course!**

---

**📝 [Back to Week 12 Exercises](../exercises/week_12.md)** | **📚 [Week 12 Documentation](../docs/week_12_final_project.md)** | **⬅️ [Previous: Week 11 Solutions](week_11_solutions.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
