# Week 11: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 10 Exercises](week_10.md)** | **📚 [Week 11 Documentation](../docs/week_11_polishing.md)** | **✅ [Week 11 Solutions](../solutions/week_11_solutions.md)** | **➡️ [Next: Week 12 Exercises](week_12.md)**

---

This week focuses on professional software development practices: writing comprehensive tests, documenting code properly, and using quality assurance tools.

## Exercise 1: Write Edge Case Tests (Beginner)

### Task

Write comprehensive pytest test functions covering edge cases that are often overlooked in pathfinding algorithms. Edge cases are important because they reveal bugs that only appear under unusual conditions.

### Requirements

Write 5 pytest test functions in a file called `test_edge_cases.py`:

1. `test_empty_grid_no_obstacles()` - Test pathfinding on a grid with no obstacles
2. `test_completely_blocked_path()` - Test when start and goal are separated by a wall
3. `test_start_equals_goal()` - Test when start position is the same as goal
4. `test_single_cell_grid()` - Test on a 1x1 grid
5. `test_all_algorithms_same_path_length()` - Test that BFS, Dijkstra, and A* all find paths of the same length on an open grid

Each test should:
- Use proper assertions with meaningful error messages
- Test both `success` status and path properties
- Use fixtures for common setup (grid creation, positions)

### Starter Code

```python
"""Edge case tests for pathfinding algorithms."""

import pytest
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dijkstra import dijkstra
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance


@pytest.fixture
def empty_grid():
    """Fixture for a 5x5 grid with no obstacles."""
    # TODO: Create and return a Grid with obstacle_density=0.0
    pass


@pytest.fixture
def blocked_grid():
    """Fixture for a grid with a vertical wall separating start and goal."""
    # TODO: Create a grid and add obstacles to block the path
    pass


def test_empty_grid_no_obstacles(empty_grid):
    """Test that algorithms work correctly on grids with no obstacles."""
    start = (0, 0)
    goal = (4, 4)

    # TODO: Run A* on the empty grid
    # TODO: Assert success is True
    # TODO: Assert path exists and has correct start/goal
    # TODO: Assert path_length equals Manhattan distance + 1
    pass


def test_completely_blocked_path(blocked_grid):
    """Test that algorithms correctly report failure when no path exists."""
    start = (0, 0)
    goal = (0, 4)

    # TODO: Run A* on the blocked grid
    # TODO: Assert success is False
    # TODO: Assert path is empty
    # TODO: Assert message indicates no path found
    pass


def test_start_equals_goal():
    """Test behavior when start and goal are the same position."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (2, 2)
    goal = (2, 2)

    # TODO: Run A*
    # TODO: Assert success is True
    # TODO: Assert path length is 1 (just the starting position)
    # TODO: Assert path_cost is 0
    pass


def test_single_cell_grid():
    """Test pathfinding on a 1x1 grid."""
    grid = Grid(1, 1, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (0, 0)

    # TODO: Run A*
    # TODO: Assert success is True
    # TODO: Assert path is [(0, 0)]
    pass


def test_all_algorithms_same_path_length(empty_grid):
    """Verify all algorithms find optimal paths on open grids."""
    start = (0, 0)
    goal = (3, 3)

    # TODO: Run BFS, Dijkstra, and A* on the same grid
    # TODO: Assert all succeed
    # TODO: Assert all have the same path_length
    # TODO: Assert path_cost is consistent (within tolerance for diagonal moves)
    pass
```

### Expected Output

When you run `pytest test_edge_cases.py -v`, you should see:

```
test_edge_cases.py::test_empty_grid_no_obstacles PASSED
test_edge_cases.py::test_completely_blocked_path PASSED
test_edge_cases.py::test_start_equals_goal PASSED
test_edge_cases.py::test_single_cell_grid PASSED
test_edge_cases.py::test_all_algorithms_same_path_length PASSED

====== 5 passed in 0.12s ======
```

### Hints

- For `test_completely_blocked_path`, create a vertical wall: `grid.add_obstacle((i, 2))` for i in range(5)
- The start-equals-goal case might need special handling in the algorithm
- For the single cell test, ensure your algorithm handles grids with no neighbors
- Use `pytest.approx()` when comparing floating-point path costs
- Consider whether your algorithms correctly handle the edge case of starting at the goal

---

## Exercise 2: Add Comprehensive Documentation (Intermediate)

### Task

Document the A* algorithm module (`algorithms/astar.py`) with professional-quality documentation that follows Google's Python Style Guide. Good documentation helps other developers understand your code without reading the implementation.

### Requirements

Add the following documentation to `astar.py`:

1. Module-level docstring explaining what the module contains
2. Complete function docstrings using Google style for:
   - `astar()` function
   - `_reconstruct_path()` helper function
3. Type hints for all function parameters and return values
4. Usage examples in docstrings
5. Notes about algorithm complexity and behavior

Your documentation should follow this structure:

**Module Docstring:**
- One-line summary
- Detailed description
- Example usage
- Reference to algorithm source/paper

**Function Docstrings (Google Style):**
- Short description
- Args section with type and description for each parameter
- Returns section with type and description
- Raises section (if applicable)
- Examples section
- Notes section for complexity/behavior

### Starter Code

```python
"""A* Search algorithm.

TODO: Add detailed module description here.
TODO: Add example usage.
TODO: Add references.
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
    """
    TODO: Expand this docstring with:
    - Complete description of A* algorithm
    - Detailed explanation of parameters
    - Return value description
    - Example usage
    - Complexity analysis
    - Notes about optimality conditions

    Args:
        grid: TODO
        start: TODO
        goal: TODO
        heuristic: TODO

    Returns:
        TODO

    Example:
        TODO: Add example code

    Note:
        TODO: Add complexity and optimality notes
    """
    # Implementation remains the same
    pass


def _reconstruct_path(
    parent: Dict[Position, Position],
    start: Position,
    goal: Position
) -> list[Position]:
    """
    TODO: Add complete docstring

    Args:
        parent: TODO
        start: TODO
        goal: TODO

    Returns:
        TODO

    Example:
        TODO
    """
    # Implementation remains the same
    pass
```

### Steps to Complete

1. Read existing documentation in the codebase for examples
2. Write comprehensive module docstring with usage example
3. Expand function docstrings following Google style
4. Add type hints where missing
5. Test documentation with `pydoc`:
   ```bash
   python -m pydoc pathfinding_lab.algorithms.astar
   ```
6. Verify HTML documentation looks good:
   ```bash
   python -m pydoc -w pathfinding_lab.algorithms.astar
   ```

### Expected Output

Running `pydoc` should produce clean, readable documentation:

```
Help on module pathfinding_lab.algorithms.astar:

NAME
    pathfinding_lab.algorithms.astar - A* Search algorithm implementation.

DESCRIPTION
    This module implements the A* (A-star) pathfinding algorithm, which...

FUNCTIONS
    astar(grid: Grid, start: Position, goal: Position,
          heuristic: Callable[[Position, Position], float]) -> SearchResult

        Perform A* Search to find the optimal path from start to goal.

        A* combines the benefits of Dijkstra's algorithm...
```

### Hints

- Look at Google's Python Style Guide for docstring examples
- Include concrete code examples in docstrings
- Mention time complexity: O((V + E) log V) for A*
- Note that A* is optimal when heuristic is admissible
- Document the priority queue structure and tie-breaking strategy
- Explain what makes a heuristic "admissible"

---

## Exercise 3: Code Quality Tools (Advanced)

### Task

Use professional code quality tools to analyze and improve the codebase. Modern Python projects use linters, type checkers, and automated tools to maintain code quality.

### Requirements

1. Install and run `ruff` (fast Python linter) to find style issues
2. Install and run `mypy` (static type checker) to find type errors
3. Fix at least 10 issues found by these tools
4. Create a pre-commit configuration to run checks automatically
5. Write a test that verifies all pathfinding algorithms return correct `SearchResult` types

### Part A: Setup Quality Tools

Install the tools:

```bash
pip install ruff mypy pre-commit
```

Run initial analysis:

```bash
# Run ruff for style issues
ruff check src/

# Run mypy for type checking
mypy src/pathfinding_lab/
```

### Part B: Create Pre-commit Configuration

Create `.pre-commit-config.yaml`:

```yaml
# TODO: Configure pre-commit hooks
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0  # Use latest version
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        # TODO: Add arguments for strict checking

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      # TODO: Add hooks for:
      # - trailing-whitespace
      # - end-of-file-fixer
      # - check-yaml
```

### Part C: Type Safety Test

Create `test_type_safety.py`:

```python
"""Tests to verify type correctness of algorithms."""

import pytest
from typing import get_type_hints

from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dijkstra import dijkstra
from pathfinding_lab.core.result import SearchResult
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance


def test_astar_returns_search_result():
    """Verify A* returns correct type."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = astar(grid, (0, 0), (4, 4), manhattan_distance)

    assert isinstance(result, SearchResult)
    assert isinstance(result.success, bool)
    assert isinstance(result.path, list)
    assert isinstance(result.nodes_visited, int)
    assert isinstance(result.runtime_ms, float)


def test_all_algorithms_return_search_result():
    """Verify all algorithms return SearchResult type."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start, goal = (0, 0), (4, 4)

    algorithms = [
        (bfs, [grid, start, goal]),
        (dijkstra, [grid, start, goal]),
        (astar, [grid, start, goal, manhattan_distance]),
    ]

    for algo_func, args in algorithms:
        result = algo_func(*args)
        assert isinstance(result, SearchResult), \
            f"{algo_func.__name__} must return SearchResult"


def test_search_result_has_required_fields():
    """Verify SearchResult has all required fields."""
    grid = Grid(3, 3, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = astar(grid, (0, 0), (2, 2), manhattan_distance)

    # TODO: Check for required fields
    required_fields = [
        'algorithm_name', 'success', 'path', 'visited_order',
        'path_length', 'path_cost', 'nodes_visited', 'runtime_ms'
    ]

    for field in required_fields:
        assert hasattr(result, field), f"Missing field: {field}"


def test_function_signatures_have_type_hints():
    """Verify key functions have type hints."""
    # TODO: Check that astar has proper type hints
    hints = get_type_hints(astar)

    assert 'grid' in hints
    assert 'start' in hints
    assert 'goal' in hints
    assert 'heuristic' in hints
    assert 'return' in hints
    assert hints['return'] == SearchResult
```

### Expected Output

After fixing issues:

```bash
$ ruff check src/
All checks passed!

$ mypy src/pathfinding_lab/
Success: no issues found in 25 source files

$ pytest test_type_safety.py -v
test_type_safety.py::test_astar_returns_search_result PASSED
test_type_safety.py::test_all_algorithms_return_search_result PASSED
test_type_safety.py::test_search_result_has_required_fields PASSED
test_type_safety.py::test_function_signatures_have_type_hints PASSED

====== 4 passed in 0.08s ======
```

### Common Issues to Fix

1. **Missing type hints**: Add type annotations to function parameters
2. **Unused imports**: Remove imports that aren't used
3. **Line too long**: Break long lines (max 88 characters for ruff)
4. **Mutable default arguments**: Use `None` instead of `[]` or `{}`
5. **Missing return type**: Add `-> ReturnType` to functions
6. **Type incompatibility**: Fix cases where types don't match
7. **Unused variables**: Remove or prefix with `_`
8. **Incorrect comparisons**: Use `is` for `None`, `==` for values
9. **Missing docstrings**: Add docstrings to public functions
10. **Inconsistent naming**: Follow PEP 8 naming conventions

### Hints

- Run ruff with `--fix` to automatically fix many issues
- Use `# type: ignore[error-code]` sparingly for unavoidable type issues
- Pre-commit hooks run automatically before each git commit
- Use `mypy --strict` for maximum type safety
- Consider adding a CI/CD pipeline to run these checks

---

## Exercise 4: Debugging Challenge (Advanced)

### Task

The following test code has multiple bugs and bad practices. Your job is to identify and fix all the issues. This teaches you to recognize common testing anti-patterns.

### Buggy Code

```python
"""Buggy tests with common testing anti-patterns."""

import time
import pytest
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance


# BUG 1: Magic numbers everywhere
def test_pathfinding_performance():
    """Test that algorithms complete in reasonable time."""
    grid = Grid(20, 20, 0.3, MovementMode.FOUR_DIRECTIONAL)
    grid.generate_obstacles((0, 0), (19, 19))

    start_time = time.time()
    result = astar(grid, (0, 0), (19, 19), manhattan_distance)
    elapsed = time.time() - start_time

    # Should complete in under 100ms
    assert elapsed < 0.1
    assert result.path_length < 50


# BUG 2: No cleanup of test fixtures
test_grid = Grid(10, 10, 0.2, MovementMode.FOUR_DIRECTIONAL)

def test_first_algorithm():
    """Test BFS on shared grid."""
    test_grid.generate_obstacles((0, 0), (9, 9))
    result = bfs(test_grid, (0, 0), (9, 9))
    assert result.success

def test_second_algorithm():
    """Test A* on shared grid - will fail because grid already has obstacles!"""
    result = astar(test_grid, (0, 0), (9, 9), manhattan_distance)
    assert result.success


# BUG 3: Flaky test - timing dependent
def test_algorithm_faster_than_threshold():
    """Test that algorithm completes quickly."""
    grid = Grid(50, 50, 0.4, MovementMode.FOUR_DIRECTIONAL)
    grid.generate_obstacles((0, 0), (49, 49))

    start = time.time()
    result = astar(grid, (0, 0), (49, 49), manhattan_distance)
    duration = time.time() - start

    # This will fail randomly based on system load
    assert duration < 0.05, "Algorithm too slow!"


# BUG 4: Testing implementation details instead of behavior
def test_astar_uses_heapq():
    """Test that A* uses a priority queue internally."""
    import heapq
    from unittest.mock import patch

    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)

    with patch('heapq.heappop') as mock_heappop:
        result = astar(grid, (0, 0), (4, 4), manhattan_distance)
        # Checking implementation detail, not behavior
        assert mock_heappop.call_count > 0


# BUG 5: Missing assertions
def test_path_validity():
    """Test that returned path is valid."""
    grid = Grid(10, 10, 0.2, MovementMode.FOUR_DIRECTIONAL)
    grid.generate_obstacles((0, 0), (9, 9))

    result = astar(grid, (0, 0), (9, 9), manhattan_distance)

    # TODO: Add assertions!
    result.path
    result.success


# BUG 6: Test doesn't test what it claims
def test_optimal_path_length():
    """Test that A* finds the optimal path."""
    grid = Grid(5, 5, 0.3, MovementMode.FOUR_DIRECTIONAL)
    grid.generate_obstacles((0, 0), (4, 4))

    result = astar(grid, (0, 0), (4, 4), manhattan_distance)

    # This doesn't verify optimality!
    assert result.path_length > 0
```

### What's Wrong?

Your task is to identify and fix these bugs:

1. **Magic Numbers**: Replace hard-coded values with named constants
2. **No Fixture Cleanup**: Tests share state and interfere with each other
3. **Flaky Tests**: Tests that fail randomly based on timing or system state
4. **Testing Implementation**: Tests should verify behavior, not how it's implemented
5. **Missing Assertions**: Tests that don't actually verify anything
6. **Misleading Test Names**: Test doesn't verify what the name claims

### Requirements

1. Identify all 6 bug categories in the code
2. Fix each issue following testing best practices
3. Add proper pytest fixtures with cleanup
4. Replace magic numbers with named constants or fixtures
5. Remove timing-dependent assertions
6. Add missing assertions with meaningful error messages
7. Make test names accurately reflect what they test

### Expected Fixed Code Structure

```python
"""Fixed tests following best practices."""

import pytest
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance


# Constants for test configuration
SMALL_GRID_SIZE = 5
MEDIUM_GRID_SIZE = 10
LARGE_GRID_SIZE = 20
LOW_OBSTACLE_DENSITY = 0.2
MEDIUM_OBSTACLE_DENSITY = 0.3


@pytest.fixture
def small_grid():
    """Create a fresh small grid for each test."""
    # TODO: Create and return clean grid with proper size
    pass


@pytest.fixture
def medium_grid_with_obstacles():
    """Create a medium grid with obstacles."""
    # TODO: Create grid, add obstacles, yield, then cleanup
    pass


def test_pathfinding_completes():
    """Test that algorithms complete successfully on various grid sizes."""
    # TODO: Fix by testing behavior, not performance
    # Don't assert on timing - that's flaky!
    pass


def test_algorithms_with_isolated_grids():
    """Test that algorithms work independently."""
    # TODO: Use fixtures to ensure each test gets a clean grid
    pass


def test_path_is_valid_and_connected():
    """Test that returned path is valid and forms connected sequence."""
    # TODO: Add proper assertions checking:
    # - Path starts at start position
    # - Path ends at goal position
    # - Each step is adjacent to the next
    # - No positions are obstacles
    pass


def test_astar_finds_path_when_one_exists():
    """Test A* behavior: finds path on open grid."""
    # TODO: Test behavior (does it find a path?), not implementation
    pass
```

### Hints

- Use `@pytest.fixture` with proper cleanup (yield, then reset)
- Define constants at module level in UPPER_CASE
- Remove all time-based assertions - test behavior instead
- Mock testing should be rare - prefer testing behavior
- Every test needs at least one meaningful assertion
- Test names should clearly describe what behavior is being verified
- Consider using `pytest.mark.parametrize` for testing multiple inputs

### Expected Output

After fixing:

```bash
$ pytest test_debugging_challenge.py -v
test_debugging_challenge.py::test_pathfinding_completes PASSED
test_debugging_challenge.py::test_algorithms_with_isolated_grids PASSED
test_debugging_challenge.py::test_path_is_valid_and_connected PASSED
test_debugging_challenge.py::test_astar_finds_path_when_one_exists PASSED

====== 4 passed in 0.15s ======
```

---

## Summary

In this week, you practiced professional software engineering skills:

1. **Edge Case Testing**: Learned to test boundary conditions that reveal bugs
2. **Documentation**: Practiced writing clear, comprehensive documentation
3. **Code Quality Tools**: Used linters and type checkers to maintain code quality
4. **Test Quality**: Learned to recognize and fix common testing anti-patterns

These skills are essential for maintaining large, professional codebases.

**See solutions/week_11_solutions.md for detailed solutions**

---

**✅ [See Solutions](../solutions/week_11_solutions.md)** | **📚 [Back to Week 11 Docs](../docs/week_11_polishing.md)** | **➡️ [Next: Week 12 Exercises](week_12.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
