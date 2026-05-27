# Week 11: Testing, Documentation, and Code Quality Solutions

## Exercise 1 Solution: Edge Case Tests

### Explanation
Edge case testing is critical for pathfinding algorithms because they must handle unusual scenarios that occur in real applications. These tests verify boundary conditions, empty inputs, invalid configurations, and performance under stress. Well-designed edge case tests catch bugs before they reach production and serve as documentation of expected behavior in unusual situations.

The five test functions below cover common edge cases: minimal grids, identical start/goal positions, blocked paths, boundary violations, and diagonal movement edge cases. Each test follows pytest conventions with clear naming, descriptive docstrings, and explicit assertions.

### Code

```python
"""Edge case tests for pathfinding algorithms."""
import pytest
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance


def test_minimal_grid():
    """Test pathfinding on smallest possible grid (1x1).

    A 1x1 grid is the minimal valid grid. If start equals goal,
    the algorithm should return success with a single-node path.
    This tests proper initialization and termination conditions.
    """
    grid = Grid(1, 1, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (0, 0)

    result = astar(grid, start, goal, manhattan_distance)

    # Should succeed with path containing just the start position
    assert result.success is True
    assert result.path_length == 1
    assert result.path == [start]
    assert result.path_cost == 0.0
    assert result.nodes_visited == 1


def test_start_equals_goal():
    """Test when start and goal are the same position.

    This is a common edge case in applications where the agent
    is already at the target. The algorithm should recognize this
    immediately and return without exploring neighbors.
    """
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (5, 5)
    goal = (5, 5)

    result = bfs(grid, start, goal)

    # Should succeed immediately
    assert result.success is True
    assert result.path_length == 1
    assert result.path == [start]
    assert result.path_cost == 0.0
    # Should visit only the start node (minimal exploration)
    assert result.nodes_visited == 1


def test_completely_blocked_goal():
    """Test when goal is surrounded by obstacles (no path exists).

    This tests the algorithm's ability to detect unreachable goals
    and fail gracefully. Essential for applications where obstacles
    might completely block the target.
    """
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (5, 5)

    # Surround goal with obstacles (4-directional blocking)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor = (goal[0] + dx, goal[1] + dy)
        grid.add_obstacle(neighbor)

    result = astar(grid, start, goal, manhattan_distance)

    # Should fail gracefully
    assert result.success is False
    assert result.path_length == 0
    assert len(result.path) == 0
    # Should still have explored nodes trying to reach goal
    assert result.nodes_visited > 0


def test_boundary_corner_neighbors():
    """Test neighbor generation at grid corners.

    Corner positions have the fewest neighbors. This tests that
    the grid correctly limits neighbors to valid positions and
    doesn't attempt to access out-of-bounds coordinates.
    """
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)

    # Test all four corners
    corner_neighbors = {
        (0, 0): 2,  # Top-left: right and down
        (0, 4): 2,  # Top-right: left and down
        (4, 0): 2,  # Bottom-left: right and up
        (4, 4): 2,  # Bottom-right: left and up
    }

    for corner, expected_count in corner_neighbors.items():
        neighbors = grid.get_neighbors(corner)
        assert len(neighbors) == expected_count, \
            f"Corner {corner} should have {expected_count} neighbors, got {len(neighbors)}"

        # Verify all neighbors are within bounds
        for neighbor in neighbors:
            assert 0 <= neighbor[0] < grid.height
            assert 0 <= neighbor[1] < grid.width


def test_eight_directional_diagonal_only():
    """Test 8-directional movement with diagonal-only path.

    In 8-directional movement, diagonal moves are valid. This tests
    that the algorithm correctly handles diagonal moves and that
    movement costs are properly calculated (diagonal vs. orthogonal).
    """
    grid = Grid(10, 10, 0.0, MovementMode.EIGHT_DIRECTIONAL)
    start = (0, 0)
    goal = (5, 5)

    # Create a corridor that forces diagonal movement
    # Block all positions except diagonal path
    for row in range(10):
        for col in range(10):
            # Allow only diagonal and one orthogonal path
            if not (row == col or (row == 0 and col == 0) or (row == 5 and col == 5)):
                if row <= 5 and col <= 5:
                    # Block most of the path area except the diagonal
                    if abs(row - col) > 1:
                        grid.add_obstacle((row, col))

    result = astar(grid, start, goal, manhattan_distance)

    # Should find a path using diagonals
    assert result.success is True
    assert result.path_length > 0
    assert result.path[0] == start
    assert result.path[-1] == goal

    # Path should contain diagonal moves
    has_diagonal = False
    for i in range(len(result.path) - 1):
        current = result.path[i]
        next_pos = result.path[i + 1]
        row_diff = abs(next_pos[0] - current[0])
        col_diff = abs(next_pos[1] - current[1])
        # Diagonal move has diff of 1 in both dimensions
        if row_diff == 1 and col_diff == 1:
            has_diagonal = True
            break

    assert has_diagonal, "Path should contain at least one diagonal move"


# Additional edge case tests for completeness

def test_obstacle_at_start():
    """Test behavior when start position is an obstacle.

    This is an invalid configuration that should be handled gracefully.
    The algorithm should fail immediately since the start is unreachable.
    """
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (2, 2)
    goal = (4, 4)

    grid.add_obstacle(start)

    result = bfs(grid, start, goal)

    # Should fail since start is blocked
    assert result.success is False


def test_obstacle_at_goal():
    """Test behavior when goal position is an obstacle.

    Similar to obstacle at start, this is an invalid configuration.
    The algorithm should detect that the goal is unreachable.
    """
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    grid.add_obstacle(goal)

    result = astar(grid, start, goal, manhattan_distance)

    # Should fail since goal is blocked
    assert result.success is False


def test_single_valid_path():
    """Test grid with only one valid path (narrow corridor).

    This tests the algorithm's ability to find paths in highly
    constrained environments. Creates a maze with one solution.
    """
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    # Create a snake-like corridor
    # Block all cells except a specific path
    for row in range(5):
        for col in range(5):
            # Allow only specific corridor cells
            if not (
                (row == 0 and col <= 4) or  # Top row
                (col == 4 and row <= 4) or  # Right column
                (row == 4)                   # Bottom row
            ):
                if (row, col) not in [start, goal]:
                    grid.add_obstacle((row, col))

    result = bfs(grid, start, goal)

    # Should find the unique path
    assert result.success is True
    assert result.path_length > 0
    # BFS guarantees shortest path
    expected_length = 9  # Along the corridor
    assert result.path_length == expected_length
```

### Key Concepts

- **Edge Case Identification**: Recognizing boundary conditions, empty inputs, and invalid states
- **Test Isolation**: Each test verifies one specific scenario independently
- **Assertions with Context**: Using descriptive assertion messages for debugging
- **Boundary Testing**: Validating behavior at grid edges and corners
- **Negative Testing**: Verifying graceful failure for invalid inputs

### Testing Advice

Run these tests with pytest:

```bash
# Run all edge case tests
pytest tests/test_edge_cases.py -v

# Run specific test
pytest tests/test_edge_cases.py::test_minimal_grid -v

# Run with coverage to see what code paths are tested
pytest tests/test_edge_cases.py --cov=src/pathfinding_lab --cov-report=html
```

Expected behavior:
- All tests should pass if algorithms handle edge cases correctly
- If tests fail, they indicate bugs in boundary handling or termination conditions
- Use `-v` flag for verbose output showing which tests pass/fail
- Coverage report helps identify untested edge cases

## Exercise 2 Solution: Comprehensive Documentation

### Explanation

Good documentation transforms code from a personal project into a professional library that others can understand and use. Documentation serves three audiences: users (how to use it), maintainers (how it works), and your future self (why decisions were made).

Google-style docstrings are the standard for scientific Python projects because they're readable both in code and when rendered by documentation generators like Sphinx. Type hints complement docstrings by making types explicit and enabling static analysis tools.

Below is a fully documented version of the A* algorithm file, demonstrating best practices for module docstrings, function documentation, type hints, and usage examples.

### Code

```python
"""A* Search algorithm implementation with heuristic guidance.

This module implements the A* (A-star) pathfinding algorithm, which combines
Dijkstra's algorithm with heuristic guidance to find optimal paths efficiently.
A* is widely used in game AI, robotics, and navigation systems.

The algorithm maintains two cost functions:
- g(n): Actual cost from start to node n
- h(n): Heuristic estimate from n to goal
- f(n) = g(n) + h(n): Total estimated cost

A* expands nodes in order of increasing f-cost, guaranteeing optimal paths
when using admissible heuristics (h(n) never overestimates actual cost).

Typical Usage Example:

    from pathfinding_lab.algorithms.astar import astar
    from pathfinding_lab.core.grid import Grid
    from pathfinding_lab.core.types import MovementMode
    from pathfinding_lab.heuristics.manhattan import manhattan_distance

    # Create a grid and run A*
    grid = Grid(20, 20, 0.2, MovementMode.FOUR_DIRECTIONAL)
    result = astar(grid, (0, 0), (19, 19), manhattan_distance)

    if result.success:
        print(f"Path found: {result.path_length} steps")
        print(f"Cost: {result.path_cost:.2f}")
        print(f"Nodes visited: {result.nodes_visited}")
    else:
        print("No path exists")

References:
    Hart, P. E., Nilsson, N. J., & Raphael, B. (1968).
    A Formal Basis for the Heuristic Determination of Minimum Cost Paths.
    IEEE Transactions on Systems Science and Cybernetics, 4(2), 100-107.

    Introduction to Algorithms (CLRS), Chapter 24.3

    Wikipedia: https://en.wikipedia.org/wiki/A*_search_algorithm

Author: Pathfinding Lab Contributors
License: MIT
"""

import heapq
import time
from typing import Callable, Dict

from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.result import SearchResult
from pathfinding_lab.core.types import Position


def astar(
    grid: Grid,
    start: Position,
    goal: Position,
    heuristic: Callable[[Position, Position], float]
) -> SearchResult:
    """Find optimal path from start to goal using A* search algorithm.

    A* explores nodes in order of estimated total cost f(n) = g(n) + h(n),
    where g(n) is the known cost from start to n, and h(n) is the heuristic
    estimate from n to goal. When the heuristic is admissible (never overestimates),
    A* guarantees finding the optimal path.

    The algorithm uses a priority queue to efficiently select the most promising
    node to expand next. It maintains a closed set to avoid revisiting nodes and
    parent pointers to reconstruct the path once the goal is reached.

    Args:
        grid: Grid object containing obstacles, dimensions, and movement rules.
            The grid defines which positions are walkable and the cost of moving
            between adjacent cells.
        start: Starting position as (row, col) tuple. Must be within grid bounds
            and not be an obstacle.
        goal: Goal position as (row, col) tuple. Must be within grid bounds
            and not be an obstacle.
        heuristic: Function that estimates distance between two positions.
            Signature: (Position, Position) -> float
            Should be admissible (never overestimate) for optimal paths.
            Common choices: manhattan_distance, euclidean_distance, octile_distance

    Returns:
        SearchResult object containing:
            - success (bool): True if path found, False otherwise
            - path (List[Position]): Positions from start to goal (empty if no path)
            - visited_order (List[Position]): Order nodes were explored
            - path_cost (float): Total cost of the path
            - nodes_visited (int): Number of nodes explored
            - runtime_ms (float): Execution time in milliseconds
            - message (str): Status message ("Optimal path found" or "No path found")

    Raises:
        ValueError: If start or goal is out of bounds or in an obstacle
            (Note: Current implementation doesn't raise, but robust version should)

    Examples:
        Basic usage with Manhattan distance:

        >>> from pathfinding_lab.core.grid import Grid
        >>> from pathfinding_lab.core.types import MovementMode
        >>> from pathfinding_lab.heuristics.manhattan import manhattan_distance
        >>> grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
        >>> result = astar(grid, (0, 0), (9, 9), manhattan_distance)
        >>> result.success
        True
        >>> result.path_length
        19
        >>> result.path[0]
        (0, 0)
        >>> result.path[-1]
        (9, 9)

        Handling obstacles:

        >>> grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
        >>> for i in range(10):
        ...     grid.add_obstacle((5, i))  # Horizontal wall
        >>> result = astar(grid, (0, 5), (9, 5), manhattan_distance)
        >>> result.success
        False

        Comparing different heuristics:

        >>> from pathfinding_lab.heuristics.euclidean import euclidean_distance
        >>> grid = Grid(20, 20, 0.1, MovementMode.EIGHT_DIRECTIONAL)
        >>> result_manhattan = astar(grid, (0, 0), (19, 19), manhattan_distance)
        >>> result_euclidean = astar(grid, (0, 0), (19, 19), euclidean_distance)
        >>> # Both should find optimal path, but explore different nodes
        >>> result_manhattan.path_cost == result_euclidean.path_cost
        True
        >>> result_euclidean.nodes_visited < result_manhattan.nodes_visited
        True  # Euclidean is more informed for 8-directional

    Time Complexity:
        O(E + V log V) where V is the number of nodes and E is the number of edges.
        In a grid with 4-directional movement: E ≈ 4V, so O(V log V).
        In worst case (exploring entire grid): O(width * height * log(width * height)).

    Space Complexity:
        O(V) for the priority queue, g_cost dict, parent dict, and closed set.
        In a grid: O(width * height) in worst case.

    Algorithm Details:
        1. Initialize priority queue with start node (f_cost = h(start, goal))
        2. While queue not empty:
            a. Pop node with lowest f_cost
            b. If node is goal, reconstruct and return path
            c. Mark node as visited (add to closed set)
            d. For each neighbor:
                - Skip if already visited
                - Calculate g_cost through current node
                - If this is better path, update costs and parent
                - Add neighbor to queue with f_cost = g_cost + h_cost
        3. If queue empties without finding goal, return failure

    Performance Notes:
        - Efficiency depends heavily on heuristic quality
        - Admissible heuristics guarantee optimality but may explore more nodes
        - Consistent heuristics (h(n) ≤ cost(n, n') + h(n')) improve efficiency
        - Use Manhattan distance for 4-directional grids
        - Use Octile distance for 8-directional grids
        - Use Euclidean distance when movement is truly continuous

    See Also:
        - algorithms.dijkstra: A* with h(n) = 0 (no heuristic)
        - algorithms.bfs: Unweighted version, simpler but less flexible
        - heuristics.manhattan: Standard heuristic for 4-directional
        - heuristics.octile: Better heuristic for 8-directional
    """
    start_time = time.time()

    # Initialize data structures
    # Priority queue stores tuples of (f_cost, g_cost, position)
    # We include g_cost as a tiebreaker to prefer nodes closer to start
    h_start = heuristic(start, goal)
    pq = [(h_start, 0.0, start)]

    # Cost from start to each node (g_cost in A* terminology)
    g_cost: Dict[Position, float] = {start: 0.0}

    # Parent pointers for path reconstruction
    parent: Dict[Position, Position] = {}

    # Track exploration order for visualization
    visited_order = []

    # Closed set: nodes we've finished processing
    closed_set = set()

    # Main A* loop - continue until queue is empty
    while pq:
        # Get node with lowest f_cost (f = g + h)
        f, current_g, current = heapq.heappop(pq)

        # Skip if we've already processed this node
        # (Can happen when same node is added to queue multiple times)
        if current in closed_set:
            continue

        # Mark as visited
        closed_set.add(current)
        visited_order.append(current)

        # Goal check - we found the optimal path!
        if current == goal:
            # Reconstruct path from start to goal using parent pointers
            path = _reconstruct_path(parent, start, goal)
            runtime_ms = (time.time() - start_time) * 1000

            return SearchResult(
                algorithm_name="A* Search",
                success=True,
                path=path,
                visited_order=visited_order,
                path_cost=g_cost[goal],
                nodes_visited=len(visited_order),
                runtime_ms=runtime_ms,
                message="Optimal path found"
            )

        # Explore all neighbors of current node
        for neighbor in grid.get_neighbors(current):
            # Skip if already fully processed
            if neighbor in closed_set:
                continue

            # Calculate cost to reach neighbor through current node
            move_cost = grid.get_movement_cost(current, neighbor)
            tentative_g = current_g + move_cost

            # If this path to neighbor is better than any previous path
            if tentative_g < g_cost.get(neighbor, float('inf')):
                # Update best known cost to neighbor
                g_cost[neighbor] = tentative_g

                # Calculate heuristic and total estimated cost
                h = heuristic(neighbor, goal)
                f_cost = tentative_g + h

                # Update parent pointer for path reconstruction
                parent[neighbor] = current

                # Add to priority queue for future expansion
                # Note: We might add same neighbor multiple times with different costs
                # The closed_set check ensures we only process it once
                heapq.heappush(pq, (f_cost, tentative_g, neighbor))

    # Queue is empty and we haven't found goal - no path exists
    runtime_ms = (time.time() - start_time) * 1000
    return SearchResult(
        algorithm_name="A* Search",
        success=False,
        visited_order=visited_order,
        nodes_visited=len(visited_order),
        runtime_ms=runtime_ms,
        message="No path found"
    )


def _reconstruct_path(
    parent: Dict[Position, Position],
    start: Position,
    goal: Position
) -> list[Position]:
    """Reconstruct path from start to goal using parent pointers.

    Traces back from goal to start using the parent dictionary,
    then reverses the result to get the forward path.

    Args:
        parent: Dictionary mapping each position to its parent in the path.
            Built during the search by recording where we came from.
        start: Starting position (path begins here).
        goal: Goal position (path ends here).

    Returns:
        List of positions forming the path from start to goal (inclusive).
        Example: [(0, 0), (1, 0), (1, 1), (2, 1)] for a 4-step path.

    Examples:
        >>> parent = {(1, 0): (0, 0), (1, 1): (1, 0), (2, 1): (1, 1)}
        >>> _reconstruct_path(parent, (0, 0), (2, 1))
        [(0, 0), (1, 0), (1, 1), (2, 1)]

    Time Complexity: O(path_length)
    Space Complexity: O(path_length) for the path list
    """
    path = []
    current = goal

    # Trace backwards from goal to start
    while current != start:
        path.append(current)
        current = parent[current]

    # Add start position
    path.append(start)

    # Reverse to get forward path
    path.reverse()

    return path
```

### Key Concepts

- **Module Docstrings**: Provide overview, usage examples, and references at file level
- **Google-Style Docstrings**: Structured format with Args, Returns, Raises, Examples sections
- **Type Hints**: Explicit parameter and return types for static analysis and IDE support
- **Usage Examples**: Concrete code snippets showing how to use the function
- **Complexity Analysis**: Document time and space complexity for performance understanding
- **Inline Comments**: Explain non-obvious logic and algorithmic steps

### Testing Advice

Verify documentation quality:

```bash
# Generate HTML documentation with Sphinx
sphinx-build -b html docs/ docs/_build/

# Check docstring completeness with pydocstyle
pydocstyle src/pathfinding_lab/algorithms/astar.py

# Verify type hints with mypy
mypy src/pathfinding_lab/algorithms/astar.py

# Test doctests (examples in docstrings)
python -m doctest src/pathfinding_lab/algorithms/astar.py -v
```

Documentation checklist:
- [ ] Module has descriptive docstring with usage example
- [ ] All public functions have docstrings
- [ ] Docstrings include Args, Returns, and Examples sections
- [ ] Type hints are complete and accurate
- [ ] Complexity analysis is provided for algorithms
- [ ] Examples in docstrings actually run (test with doctest)

## Exercise 3 Solution: Code Quality and Type Safety

### Explanation

Code quality tools like ruff and mypy help maintain consistency, catch bugs early, and make code more maintainable. Ruff enforces style guidelines (PEP 8) and identifies common errors, while mypy verifies type correctness. Pre-commit hooks automate these checks, preventing issues from reaching version control.

This solution demonstrates common issues found by these tools and how to fix them, plus a complete pre-commit configuration.

### Code

#### Common Ruff Issues and Fixes

```python
# ============================================================================
# Issue 1: Unused imports
# ============================================================================

# BAD - Ruff error: F401 'typing.List' imported but unused
from typing import List, Dict, Tuple

def process_path(path):
    return len(path)

# GOOD - Remove unused imports
from typing import Tuple  # Only import what's used

def process_path(path: list[tuple[int, int]]) -> int:
    """Use built-in list/tuple types in Python 3.9+"""
    return len(path)


# ============================================================================
# Issue 2: Line too long (>100 characters)
# ============================================================================

# BAD - Ruff error: E501 line too long (127 > 100 characters)
def calculate_metrics(result, grid_width, grid_height, obstacle_density, movement_mode, heuristic_name, benchmark_iterations):
    pass

# GOOD - Break into multiple lines
def calculate_metrics(
    result: SearchResult,
    grid_width: int,
    grid_height: int,
    obstacle_density: float,
    movement_mode: MovementMode,
    heuristic_name: str,
    benchmark_iterations: int
) -> dict:
    """Calculate performance metrics for benchmarking."""
    pass


# ============================================================================
# Issue 3: Undefined name
# ============================================================================

# BAD - Ruff error: F821 undefined name 'manhatten_distance'
result = astar(grid, start, goal, manhatten_distance)  # Typo!

# GOOD - Fix typo or add import
from pathfinding_lab.heuristics.manhattan import manhattan_distance

result = astar(grid, start, goal, manhattan_distance)


# ============================================================================
# Issue 4: Mutable default argument
# ============================================================================

# BAD - Ruff error: B006 Do not use mutable data structures for argument defaults
def create_grid(obstacles=[]):
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    for obs in obstacles:
        grid.add_obstacle(obs)
    return grid

# GOOD - Use None and create new list inside function
def create_grid(obstacles: list[Position] | None = None) -> Grid:
    """Create grid with optional obstacles."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    if obstacles is not None:
        for obs in obstacles:
            grid.add_obstacle(obs)
    return grid


# ============================================================================
# Issue 5: Comparison to True/False/None
# ============================================================================

# BAD - Ruff error: E712 comparison to True should be 'if cond:' or 'if cond is True:'
if result.success == True:
    print("Found path")

if obstacles == None:
    return

# GOOD - Use identity check or implicit boolean
if result.success:  # Preferred for boolean values
    print("Found path")

if obstacles is None:  # Use 'is' for None
    return
```

#### Common Mypy Issues and Fixes

```python
# ============================================================================
# Issue 1: Missing type annotations
# ============================================================================

# BAD - Mypy error: Function is missing a type annotation
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# GOOD - Add complete type hints
def manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """Calculate Manhattan distance between two positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# ============================================================================
# Issue 2: Incompatible types in assignment
# ============================================================================

# BAD - Mypy error: Incompatible types in assignment (expression has type "float", variable has type "int")
def calculate_cost(distance: int) -> int:
    cost = distance * 1.5  # Returns float!
    return cost

# GOOD - Fix return type or use explicit conversion
def calculate_cost(distance: int) -> float:
    """Calculate cost with 1.5x multiplier."""
    cost: float = distance * 1.5
    return cost

# OR if you need int:
def calculate_cost_int(distance: int) -> int:
    """Calculate cost with 1.5x multiplier, rounded."""
    cost: float = distance * 1.5
    return int(cost)


# ============================================================================
# Issue 3: Returning Any from function
# ============================================================================

# BAD - Mypy warning: Function is missing a return type annotation
def get_neighbors(grid, pos):
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        neighbor = (pos[0] + dx, pos[1] + dy)
        if is_valid(grid, neighbor):
            neighbors.append(neighbor)
    return neighbors

# GOOD - Explicit return type
def get_neighbors(grid: Grid, pos: Position) -> list[Position]:
    """Get valid neighbors of a position."""
    neighbors: list[Position] = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        neighbor: Position = (pos[0] + dx, pos[1] + dy)
        if is_valid(grid, neighbor):
            neighbors.append(neighbor)
    return neighbors


# ============================================================================
# Issue 4: Optional type handling
# ============================================================================

# BAD - Mypy error: Item "None" has no attribute "path"
def print_path(result: SearchResult | None):
    print(f"Path length: {result.path_length}")  # result might be None!

# GOOD - Handle None case explicitly
def print_path(result: SearchResult | None) -> None:
    """Print path length if result exists."""
    if result is None:
        print("No result available")
        return

    print(f"Path length: {result.path_length}")

# OR use type narrowing with assert
def print_path_assert(result: SearchResult | None) -> None:
    """Print path length (result must not be None)."""
    assert result is not None, "Result cannot be None"
    print(f"Path length: {result.path_length}")
```

#### SearchResult Type Verification Test

```python
"""Test for SearchResult type safety and structure."""
import pytest
from pathfinding_lab.core.result import SearchResult
from pathfinding_lab.core.types import Position


def test_search_result_type_completeness():
    """Verify SearchResult has all required fields with correct types.

    This test ensures the SearchResult dataclass maintains type safety
    and includes all fields needed for comprehensive result reporting.
    """
    # Create a complete SearchResult
    result = SearchResult(
        algorithm_name="Test Algorithm",
        success=True,
        path=[(0, 0), (1, 0), (1, 1)],
        visited_order=[(0, 0), (1, 0), (0, 1), (1, 1)],
        path_length=3,
        path_cost=2.0,
        nodes_visited=4,
        runtime_ms=1.5,
        message="Test complete"
    )

    # Verify types of all fields
    assert isinstance(result.algorithm_name, str)
    assert isinstance(result.success, bool)
    assert isinstance(result.path, list)
    assert isinstance(result.visited_order, list)
    assert isinstance(result.path_length, int)
    assert isinstance(result.path_cost, float)
    assert isinstance(result.nodes_visited, int)
    assert isinstance(result.runtime_ms, float)
    assert isinstance(result.message, str)

    # Verify list contents are Position tuples
    for pos in result.path:
        assert isinstance(pos, tuple)
        assert len(pos) == 2
        assert isinstance(pos[0], int)
        assert isinstance(pos[1], int)


def test_search_result_defaults():
    """Verify SearchResult default values are correct."""
    # Minimal SearchResult
    result = SearchResult(
        algorithm_name="Minimal",
        success=False
    )

    # Check defaults
    assert result.path == []
    assert result.visited_order == []
    assert result.path_length == 0
    assert result.path_cost == 0.0
    assert result.nodes_visited == 0
    assert result.runtime_ms == 0.0
    assert result.message == ""


def test_search_result_post_init():
    """Verify __post_init__ calculates derived fields correctly."""
    # Create result with path but no path_length
    result = SearchResult(
        algorithm_name="Test",
        success=True,
        path=[(0, 0), (1, 0), (2, 0), (2, 1)]
    )

    # path_length should be auto-calculated
    assert result.path_length == 4

    # Create result with empty path
    result_no_path = SearchResult(
        algorithm_name="Test",
        success=False,
        path=[]
    )

    # path_length should be 0
    assert result_no_path.path_length == 0
```

#### Pre-commit Configuration File

```yaml
# .pre-commit-config.yaml
# Configuration for pre-commit hooks that run before each commit
# Install with: pip install pre-commit && pre-commit install

repos:
  # Ruff - Fast Python linter and formatter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      # Run linter
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
        # Check and auto-fix common issues

      # Run formatter
      - id: ruff-format
        # Auto-format code to match style guide

  # Mypy - Static type checker
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--strict, --ignore-missing-imports]
        # Enforce strict type checking

  # Basic code quality checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      # Prevent committing large files
      - id: check-added-large-files
        args: [--maxkb=500]

      # Ensure files end with newline
      - id: end-of-file-fixer

      # Remove trailing whitespace
      - id: trailing-whitespace

      # Check YAML syntax
      - id: check-yaml

      # Check for merge conflicts
      - id: check-merge-conflict

      # Verify Python syntax
      - id: check-ast

      # Sort imports alphabetically
      - id: check-docstring-first

  # Pytest - Run tests before commit
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [tests/, -v, --tb=short]
        # Run tests and fail commit if any test fails

# Configuration for individual tools
# These settings are also in pyproject.toml but included here for reference

# Ruff configuration (in pyproject.toml):
# [tool.ruff]
# line-length = 100
# target-version = "py39"
#
# [tool.ruff.lint]
# select = ["E", "F", "B", "W", "I"]
# ignore = ["E501"]  # Line too long (handled by formatter)

# Mypy configuration (in pyproject.toml):
# [tool.mypy]
# python_version = "3.9"
# warn_return_any = true
# warn_unused_configs = true
# disallow_untyped_defs = true
```

### Key Concepts

- **Static Analysis**: Catch errors before runtime through code inspection
- **Type Safety**: Use type hints to prevent type-related bugs
- **Code Consistency**: Enforce uniform style across the codebase
- **Automation**: Pre-commit hooks run checks automatically before commits
- **Tool Configuration**: Centralize settings in pyproject.toml

### Testing Advice

Set up and run code quality tools:

```bash
# Install tools
pip install ruff mypy pre-commit

# Run ruff linter
ruff check src/pathfinding_lab/

# Auto-fix ruff issues
ruff check src/pathfinding_lab/ --fix

# Format code with ruff
ruff format src/pathfinding_lab/

# Run mypy type checker
mypy src/pathfinding_lab/ --strict

# Install pre-commit hooks
pre-commit install

# Run pre-commit manually on all files
pre-commit run --all-files

# Test a commit (hooks run automatically)
git add .
git commit -m "Test commit"  # Hooks run here!
```

Expected workflow:
1. Write code with type hints
2. Run `ruff format` to auto-format
3. Run `ruff check --fix` to auto-fix simple issues
4. Run `mypy` to verify types
5. Fix any remaining issues manually
6. Commit (pre-commit hooks run automatically)

## Exercise 4 Solution: Debugging Test Code

### Explanation

Test code can have bugs just like production code. Common issues include incorrect assertions, improper test setup, flaky tests that sometimes pass/fail, and tests that don't actually verify the intended behavior. This exercise identifies and fixes 5+ common test bugs.

### Bugs Found

#### Bug 1: Incorrect Assertion Comparison

**Problem:**
```python
def test_path_length():
    result = bfs(grid, (0, 0), (2, 2))
    assert result.path_length = 5  # WRONG: assignment instead of comparison
```

**Why it's wrong:** Uses single `=` (assignment) instead of `==` (comparison). This is a syntax error in Python.

**Fix:**
```python
def test_path_length():
    """Test that BFS finds correct path length."""
    result = bfs(grid, (0, 0), (2, 2))
    assert result.path_length == 5  # Correct: equality comparison
```

#### Bug 2: Missing Test Fixture Setup

**Problem:**
```python
def test_grid_with_obstacles():
    # Missing grid creation!
    grid.add_obstacle((5, 5))
    result = astar(grid, (0, 0), (9, 9), manhattan_distance)
    assert result.success is True
```

**Why it's wrong:** References `grid` variable that doesn't exist. Test will fail with `NameError: name 'grid' is not defined`.

**Fix:**
```python
def test_grid_with_obstacles():
    """Test pathfinding with obstacles."""
    # Create grid first
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    grid.add_obstacle((5, 5))

    result = astar(grid, (0, 0), (9, 9), manhattan_distance)
    assert result.success is True
```

#### Bug 3: Flaky Test Due to Floating Point Comparison

**Problem:**
```python
def test_diagonal_cost():
    result = astar(grid, (0, 0), (5, 5), euclidean_distance)
    assert result.path_cost == 7.071067811865476  # Exact float comparison
```

**Why it's wrong:** Floating point arithmetic can have tiny rounding errors. This test might fail on different systems or Python versions.

**Fix:**
```python
import pytest

def test_diagonal_cost():
    """Test diagonal movement cost calculation."""
    grid = Grid(10, 10, 0.0, MovementMode.EIGHT_DIRECTIONAL)
    result = astar(grid, (0, 0), (5, 5), euclidean_distance)

    # Use approximate comparison with tolerance
    expected_cost = 5 * 1.41421356  # 5 diagonal moves
    assert result.path_cost == pytest.approx(expected_cost, rel=0.01)
```

#### Bug 4: Test Doesn't Actually Test Anything

**Problem:**
```python
def test_algorithm_runs():
    """Test that algorithm runs."""
    result = bfs(grid, (0, 0), (9, 9))
    # No assertions! Test always passes
```

**Why it's wrong:** Missing assertions means test passes even if result is completely wrong. Only verifies the code doesn't crash.

**Fix:**
```python
def test_algorithm_runs_and_succeeds():
    """Test that BFS finds a path in open grid."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = bfs(grid, (0, 0), (9, 9))

    # Assert expected behavior
    assert result.success is True, "Should find path in open grid"
    assert result.path_length > 0, "Path should not be empty"
    assert result.path[0] == (0, 0), "Path should start at start position"
    assert result.path[-1] == (9, 9), "Path should end at goal position"
```

#### Bug 5: Test Order Dependency (Not Isolated)

**Problem:**
```python
# Global variable modified by tests
test_grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)

def test_first():
    test_grid.add_obstacle((5, 5))
    result = astar(test_grid, (0, 0), (9, 9), manhattan_distance)
    assert result.success is True

def test_second():
    # Depends on test_first not running!
    # If test_first runs first, obstacle is present
    result = astar(test_grid, (0, 0), (9, 9), manhattan_distance)
    assert len(test_grid.obstacles) == 0  # FAILS if test_first ran first!
```

**Why it's wrong:** Tests should be independent and isolated. Running tests in different orders gives different results.

**Fix:**
```python
import pytest

@pytest.fixture
def clean_grid():
    """Provide a fresh grid for each test."""
    return Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)

def test_first(clean_grid):
    """Test with obstacle."""
    clean_grid.add_obstacle((5, 5))
    result = astar(clean_grid, (0, 0), (9, 9), manhattan_distance)
    assert result.success is True

def test_second(clean_grid):
    """Test without obstacle."""
    # Gets fresh grid, independent of test_first
    result = astar(clean_grid, (0, 0), (9, 9), manhattan_distance)
    assert len(clean_grid.obstacles) == 0  # Always passes
```

#### Bug 6: Overly Specific Assertion

**Problem:**
```python
def test_visited_nodes():
    result = bfs(grid, (0, 0), (5, 5))
    # Too specific - brittle if implementation changes
    assert result.nodes_visited == 42
```

**Why it's wrong:** Tests implementation details rather than behavior. If algorithm explores nodes in different order, test fails even though behavior is correct.

**Fix:**
```python
def test_visited_nodes():
    """Test that BFS visits reasonable number of nodes."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = bfs(grid, (0, 0), (5, 5))

    # Test behavior, not exact implementation
    assert result.nodes_visited > 0, "Should visit at least one node"
    assert result.nodes_visited <= 100, "Shouldn't visit more nodes than grid has"
    # More specific: BFS explores at most all reachable nodes
    max_possible = grid.width * grid.height
    assert result.nodes_visited <= max_possible
```

#### Bug 7: Missing Import

**Problem:**
```python
def test_manhattan_heuristic():
    result = astar(grid, (0, 0), (9, 9), manhattan_distance)
    # NameError: name 'manhattan_distance' is not defined
    assert result.success is True
```

**Why it's wrong:** References function without importing it.

**Fix:**
```python
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def test_manhattan_heuristic():
    """Test A* with Manhattan heuristic."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = astar(grid, (0, 0), (9, 9), manhattan_distance)
    assert result.success is True
```

### Corrected Code

Complete corrected test file:

```python
"""Corrected pathfinding tests demonstrating best practices."""
import pytest
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.heuristics.euclidean import euclidean_distance


@pytest.fixture
def empty_grid():
    """Provide a clean 10x10 grid for each test."""
    return Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)


@pytest.fixture
def grid_with_diagonal():
    """Provide an 8-directional grid for diagonal movement tests."""
    return Grid(10, 10, 0.0, MovementMode.EIGHT_DIRECTIONAL)


def test_path_length_correct(empty_grid):
    """Test that BFS calculates correct path length."""
    result = bfs(empty_grid, (0, 0), (2, 2))

    # In 4-directional, shortest path is Manhattan distance
    expected_length = abs(2 - 0) + abs(2 - 0) + 1  # 5 nodes
    assert result.path_length == expected_length


def test_grid_with_obstacles_proper_setup(empty_grid):
    """Test pathfinding with obstacles using proper test setup."""
    # Grid comes from fixture, properly initialized
    empty_grid.add_obstacle((5, 5))

    result = astar(empty_grid, (0, 0), (9, 9), manhattan_distance)

    # Should find path around obstacle
    assert result.success is True
    assert (5, 5) not in result.path


def test_diagonal_cost_approximate(grid_with_diagonal):
    """Test diagonal movement cost with proper float comparison."""
    result = astar(grid_with_diagonal, (0, 0), (5, 5), euclidean_distance)

    # 5 diagonal moves at cost ~1.414 each
    expected_cost = 5 * 1.41421356

    # Use pytest.approx for float comparison
    assert result.path_cost == pytest.approx(expected_cost, rel=0.01)


def test_algorithm_with_meaningful_assertions(empty_grid):
    """Test that algorithm produces valid, complete results."""
    result = bfs(empty_grid, (0, 0), (9, 9))

    # Multiple meaningful assertions
    assert result.success is True, "Should find path in open grid"
    assert result.path_length > 0, "Path should not be empty"
    assert result.path[0] == (0, 0), "Path should start at start"
    assert result.path[-1] == (9, 9), "Path should end at goal"
    assert result.nodes_visited > 0, "Should visit at least one node"
    assert result.runtime_ms >= 0, "Runtime should be non-negative"


def test_isolated_with_fixture(empty_grid):
    """Test using fixture ensures isolation."""
    # Each test gets fresh grid from fixture
    assert len(empty_grid.obstacles) == 0

    empty_grid.add_obstacle((5, 5))
    assert len(empty_grid.obstacles) == 1


def test_another_isolated_test(empty_grid):
    """Another test - proves isolation works."""
    # Gets fresh grid, independent of previous test
    assert len(empty_grid.obstacles) == 0


def test_visited_nodes_behavioral(empty_grid):
    """Test visited nodes with behavioral assertions."""
    result = bfs(empty_grid, (0, 0), (5, 5))

    # Test behavior, not exact numbers
    assert result.nodes_visited > 0
    assert result.nodes_visited <= empty_grid.width * empty_grid.height

    # More specific: for BFS, nodes_visited >= path_length
    assert result.nodes_visited >= result.path_length


def test_with_all_imports():
    """Test that demonstrates proper imports."""
    # All needed imports at top of file
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = astar(grid, (0, 0), (9, 9), manhattan_distance)

    assert result.success is True


# Parametrized test demonstrating multiple scenarios
@pytest.mark.parametrize("start,goal,should_succeed", [
    ((0, 0), (9, 9), True),   # Normal path
    ((0, 0), (0, 0), True),   # Start equals goal
    ((5, 5), (5, 5), True),   # Start equals goal (center)
])
def test_multiple_scenarios(empty_grid, start, goal, should_succeed):
    """Test multiple scenarios with parametrize."""
    result = bfs(empty_grid, start, goal)

    assert result.success == should_succeed
    if should_succeed:
        assert result.path_length > 0
        assert result.path[0] == start
        assert result.path[-1] == goal
```

### Key Concepts

- **Test Isolation**: Each test should be independent and not affect others
- **Proper Assertions**: Tests must verify expected behavior, not just run without errors
- **Fixture Usage**: pytest fixtures provide clean test setup and teardown
- **Float Comparison**: Use `pytest.approx()` for floating point comparisons
- **Behavioral Testing**: Test what code does, not how it does it (avoid implementation details)

### Testing Advice

Best practices for reliable tests:

```bash
# Run tests with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_debugging.py::test_path_length_correct -v

# Run tests with coverage
pytest tests/ --cov=src/pathfinding_lab --cov-report=term-missing

# Run tests in random order to catch dependencies
pytest tests/ --random-order

# Run tests with strict markers (catch typos in @pytest.mark)
pytest tests/ --strict-markers
```

Checklist for good tests:
- [ ] Each test has descriptive name and docstring
- [ ] Tests use fixtures for setup (no shared global state)
- [ ] All tests have meaningful assertions
- [ ] Float comparisons use pytest.approx()
- [ ] Tests are independent (can run in any order)
- [ ] All imports are present and correct
- [ ] Tests verify behavior, not implementation details

---

## Summary

This week covered professional code quality practices:

1. **Edge Case Testing**: Identified and tested boundary conditions, empty inputs, and invalid states
2. **Documentation**: Wrote comprehensive docstrings with type hints, examples, and complexity analysis
3. **Code Quality Tools**: Used ruff and mypy to enforce consistency and catch type errors
4. **Test Reliability**: Fixed common test bugs and improved test isolation and assertions

These practices transform a personal project into professional, maintainable code suitable for portfolios, collaboration, and production use.

**Key Takeaways:**
- Edge cases often reveal bugs that normal testing misses
- Good documentation makes code accessible to others (and your future self)
- Automated tools catch many issues before they become bugs
- Test code deserves the same care and quality as production code

**Next: Week 12 Capstone Project →**
