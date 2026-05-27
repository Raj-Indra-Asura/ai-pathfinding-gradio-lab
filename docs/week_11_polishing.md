# Week 11: Testing, Documentation, and Project Polishing

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 10](week_10_ml_heuristic.md)** | **📝 [Week 11 Exercises](../exercises/week_11.md)** | **✅ [Week 11 Solutions](../solutions/week_11_solutions.md)** | **➡️ [Next: Week 12](week_12_final_project.md)**

---

## Learning Goals

By the end of this week, you will understand:
- How to write comprehensive unit tests using pytest
- Best practices for documenting code with docstrings and type hints
- Using code quality tools (ruff, mypy) to maintain standards
- Professional Python project organization patterns
- Preparing code for sharing in portfolios or open source

## Theory

### Why Testing Matters in Algorithm Implementation

Testing is crucial for pathfinding algorithms because:

1. **Correctness Verification**: Algorithms must find valid paths when they exist
2. **Optimality Guarantees**: Some algorithms (A*, Dijkstra) guarantee optimal paths
3. **Edge Case Handling**: Empty grids, blocked paths, and start==goal scenarios
4. **Performance Regression**: Ensure optimizations don't break correctness
5. **Refactoring Safety**: Change implementation details confidently

In educational contexts, tests serve as executable documentation showing how algorithms should behave.

### Test-Driven Development (TDD) Basics

The TDD cycle for algorithms:

```
1. Write a failing test (Red)
   - Define expected behavior for a specific scenario
   - Example: "BFS should find shortest path in unweighted grid"

2. Implement minimal code to pass (Green)
   - Write just enough algorithm code to satisfy the test
   - Don't worry about optimization yet

3. Refactor and improve (Refactor)
   - Clean up code while keeping tests passing
   - Improve performance, readability, or structure
```

**Benefits for Algorithm Development:**
- Forces you to think about behavior before implementation
- Creates a safety net for optimizations
- Documents expected behavior through examples
- Catches regressions immediately

### Testing Pyramid for Pathfinding Projects

```
        /\
       /  \      Integration Tests (UI + algorithms)
      /____\
     /      \
    /  Unit  \   Unit Tests (individual functions)
   /  Tests   \
  /____________\
```

**Unit Tests** (80% of tests):
- Grid neighbor generation
- Heuristic calculations
- Individual algorithm steps
- Metric calculations

**Integration Tests** (20% of tests):
- Full pathfinding with visualization
- UI component interactions
- Benchmark suites

### Documentation as Communication

Good documentation answers three questions:

1. **What does this do?** (Summary)
   ```python
   """Calculate Manhattan distance between two points."""
   ```

2. **How do I use it?** (Parameters, Returns, Examples)
   ```python
   """
   Args:
       pos1: Starting position (row, col)
       pos2: Target position (row, col)

   Returns:
       Manhattan distance as integer

   Example:
       >>> manhattan_distance((0, 0), (3, 4))
       7
   """
   ```

3. **Why does it work this way?** (Algorithm explanation, complexity)
   ```python
   """
   Manhattan distance sums absolute differences in coordinates.
   This is the optimal heuristic for 4-directional grids since
   it never overestimates the actual path cost.

   Time Complexity: O(1)
   Space Complexity: O(1)
   """
   ```

### Code Quality Metrics

**Ruff** (Fast Python linter):
- Checks style consistency (PEP 8)
- Finds common errors (unused imports, undefined names)
- Enforces modern Python idioms
- Combines speed of Rust with Python ecosystem knowledge

**Mypy** (Static type checker):
- Catches type errors before runtime
- Documents expected types through annotations
- Improves IDE autocomplete and refactoring
- Helps prevent bugs like passing string to numeric function

**Coverage** (Test completeness):
- Measures % of code executed by tests
- Identifies untested branches
- Target 80%+ for algorithm code
- 100% coverage doesn't guarantee correctness, but <50% is risky

### Professional Python Project Structure

```
pathfinding-lab/
├── src/pathfinding_lab/      # Main package
│   ├── __init__.py           # Package exports
│   ├── algorithms/           # Algorithm implementations
│   ├── core/                 # Grid, types, constants
│   ├── heuristics/           # Distance functions
│   └── metrics/              # Evaluation tools
├── tests/                    # Test suite (mirrors src/)
│   ├── test_grid.py
│   ├── test_bfs.py
│   └── test_astar.py
├── docs/                     # Documentation
├── pyproject.toml           # Dependencies and tool config
└── README.md                # Project overview
```

**Key Principles:**
- `src/` layout prevents import confusion
- Tests mirror source structure
- `pyproject.toml` centralizes all configuration
- Clear separation between code, tests, and docs

## Code Walkthrough

### Understanding pytest Fundamentals

#### Test Discovery and Naming

Pytest automatically finds tests following these patterns:
- Files named `test_*.py` or `*_test.py`
- Functions named `test_*`
- Classes named `Test*`

```python
# tests/test_grid.py
def test_grid_creation():
    """pytest finds this automatically"""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    assert grid.width == 10
```

#### Assertions - The Core of Testing

```python
# Basic assertions
assert result == expected               # Equality
assert result.success is True          # Boolean checks
assert len(neighbors) == 4             # Numeric comparison

# Approximate equality for floats
import pytest
assert cost == pytest.approx(1.414, rel=0.01)  # Within 1% tolerance

# Membership checks
assert start not in grid.obstacles     # Item not in collection
assert (4, 5) in neighbors             # Item in collection
```

### Review: test_grid.py

**Grid Creation Tests:**
```python
def test_grid_creation():
    """Test basic grid creation."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    assert grid.width == 10
    assert grid.height == 10
    assert len(grid.obstacles) == 0
```

**What it tests:** Basic object initialization
**Why it matters:** Ensures constructor sets up valid state

**Neighbor Generation Tests:**
```python
def test_neighbors_4_directional():
    """Test 4-directional neighbor generation."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    neighbors = grid.get_neighbors((5, 5))

    assert len(neighbors) == 4
    assert (4, 5) in neighbors  # Up
    assert (6, 5) in neighbors  # Down
    assert (5, 4) in neighbors  # Left
    assert (5, 6) in neighbors  # Right
```

**What it tests:** Correct neighbor calculation for movement mode
**Why it matters:** Algorithms depend on accurate neighbor generation

**Boundary Handling:**
```python
def test_boundary_handling():
    """Test grid boundary handling."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)

    # Corner position should have 2 neighbors
    neighbors = grid.get_neighbors((0, 0))
    assert len(neighbors) == 2

    # Edge position should have 3 neighbors
    neighbors = grid.get_neighbors((0, 2))
    assert len(neighbors) == 3
```

**What it tests:** Edge case handling at grid boundaries
**Why it matters:** Prevents index errors and ensures algorithms work at edges

### Review: test_bfs.py

**Path Finding Test:**
```python
def test_bfs_simple_path():
    """Test BFS finds a path in open grid."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result = bfs(grid, start, goal)

    assert result.success is True
    assert result.path_length > 0
    assert result.path[0] == start
    assert result.path[-1] == goal
```

**What it tests:** Basic pathfinding functionality
**Why it matters:** Verifies algorithm finds valid paths

**Optimality Test:**
```python
def test_bfs_shortest_path():
    """Test BFS finds shortest path."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = bfs(grid, start, goal)

    # In 4-directional, shortest path is Manhattan distance
    expected_length = abs(goal[0] - start[0]) + abs(goal[1] - start[1]) + 1
    assert result.path_length == expected_length
```

**What it tests:** BFS optimality guarantee
**Why it matters:** BFS must find shortest path in unweighted graphs

### Review: test_astar.py

**Heuristic Comparison:**
```python
def test_astar_different_heuristics():
    """Test A* with different heuristics."""
    grid = Grid(5, 5, 0.0, MovementMode.EIGHT_DIRECTIONAL)
    start = (0, 0)
    goal = (4, 4)

    result_manhattan = astar(grid, start, goal, manhattan_distance)
    result_euclidean = astar(grid, start, goal, euclidean_distance)

    # Both should find same optimal cost (admissible heuristics)
    assert result_manhattan.path_cost == pytest.approx(
        result_euclidean.path_cost, rel=0.01
    )
```

**What it tests:** Admissible heuristics produce optimal paths
**Why it matters:** Verifies A* theoretical guarantees

**Efficiency Test:**
```python
def test_astar_better_than_dijkstra():
    """Test A* explores fewer nodes than Dijkstra."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (9, 9)

    astar_result = astar(grid, start, goal, manhattan_distance)
    dijkstra_result = dijkstra(grid, start, goal)

    # A* should visit fewer or equal nodes
    assert astar_result.nodes_visited <= dijkstra_result.nodes_visited
```

**What it tests:** A* efficiency gain over Dijkstra
**Why it matters:** Shows practical benefit of heuristic guidance

### Review: test_heuristics.py

**Admissibility Test:**
```python
def test_heuristic_admissibility():
    """Test that heuristics never overestimate."""
    pos1 = (0, 0)
    pos2 = (3, 4)
    actual_cost = 7  # Minimum steps in 4-directional

    h_manhattan = manhattan_distance(pos1, pos2)
    h_euclidean = euclidean_distance(pos1, pos2)

    assert h_manhattan == actual_cost
    assert h_euclidean <= actual_cost
```

**What it tests:** Heuristic admissibility property
**Why it matters:** A* optimality requires admissible heuristics

### Review: test_metrics.py

**Evaluation Test:**
```python
def test_evaluate_result():
    """Test result evaluation."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = bfs(grid, (0, 0), (2, 2))
    metrics = evaluate_result(result)

    assert 'algorithm' in metrics
    assert 'success' in metrics
    assert 'path_length' in metrics
    assert 'efficiency' in metrics
```

**What it tests:** Metrics calculation completeness
**Why it matters:** Benchmarking depends on accurate metrics

### Advanced pytest Features

#### Fixtures - Reusable Test Setup

```python
import pytest
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

@pytest.fixture
def empty_grid():
    """Provide a clean 10x10 grid."""
    return Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)

@pytest.fixture
def grid_with_wall():
    """Provide a grid with vertical wall in middle."""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    for row in range(10):
        grid.add_obstacle((row, 5))
    return grid

def test_using_fixture(empty_grid):
    """Tests automatically receive fixtures as parameters."""
    assert empty_grid.width == 10
    assert len(empty_grid.obstacles) == 0
```

**Benefits:**
- Reduces code duplication
- Ensures consistent test setup
- Makes tests more readable

#### Parametrize - Multiple Test Cases

```python
@pytest.mark.parametrize("start,goal,expected_distance", [
    ((0, 0), (0, 0), 0),      # Same position
    ((0, 0), (3, 4), 7),      # Positive coordinates
    ((5, 5), (2, 3), 5),      # Reverse direction
    ((0, 0), (10, 0), 10),    # Horizontal line
    ((0, 0), (0, 10), 10),    # Vertical line
])
def test_manhattan_parametrized(start, goal, expected_distance):
    """Test Manhattan distance with multiple cases."""
    assert manhattan_distance(start, goal) == expected_distance
```

**Benefits:**
- Tests multiple scenarios with one function
- Makes test cases explicit and readable
- Easy to add new test cases

## Common Mistakes

### 1. Testing Implementation Instead of Behavior

**Problem:**
```python
def test_bfs_uses_queue():
    """Bad: Tests how BFS works internally"""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = bfs(grid, (0, 0), (4, 4))

    # Checking internal queue structure
    assert isinstance(result._internal_queue, deque)  # Fragile!
```

**Why it's wrong:** Tests become brittle when implementation changes. If you switch from `deque` to a different queue, tests break even though behavior is correct.

**Solution:**
```python
def test_bfs_finds_shortest_path():
    """Good: Tests what BFS guarantees"""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = bfs(grid, (0, 0), (2, 2))

    # Test the guarantee: BFS finds optimal path
    expected = abs(2-0) + abs(2-0) + 1
    assert result.path_length == expected
```

### 2. Missing Edge Cases

**Problem:**
```python
def test_astar_basic():
    """Only tests happy path"""
    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = astar(grid, (0, 0), (9, 9), manhattan_distance)
    assert result.success is True
```

**What's missing:**
- Empty grid (1x1 or 0x0)
- Start equals goal
- No path exists (completely blocked)
- Start or goal out of bounds
- Negative coordinates

**Solution:**
```python
def test_astar_start_equals_goal():
    """Edge case: start and goal are same"""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result = astar(grid, (2, 2), (2, 2), manhattan_distance)

    assert result.success is True
    assert result.path_length == 1  # Just the start position
    assert result.path_cost == 0.0

def test_astar_no_path():
    """Edge case: goal is unreachable"""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)

    # Surround goal completely
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        grid.add_obstacle((4+dx, 4+dy))

    result = astar(grid, (0, 0), (4, 4), manhattan_distance)
    assert result.success is False
    assert len(result.path) == 0
```

### 3. Poor Test Organization

**Problem:**
```python
# test_everything.py - 2000 lines
def test_grid_and_bfs_and_astar():
    """One giant test for everything"""
    # Tests 50 different things...
```

**Why it's wrong:**
- Hard to identify what failed
- Can't run specific tests
- Difficult to maintain

**Solution:**
```
tests/
├── test_grid.py          # Grid-specific tests
├── test_bfs.py           # BFS algorithm tests
├── test_astar.py         # A* algorithm tests
└── test_heuristics.py    # Heuristic function tests
```

Each test should verify ONE behavior:
```python
def test_grid_neighbors_respect_obstacles():
    """Single, clear purpose"""
    # Test one specific thing
```

### 4. Missing or Poor Docstrings

**Problem:**
```python
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
```

**Why it's wrong:**
- No explanation of purpose
- Parameter types unclear
- No usage examples
- Missing complexity analysis

**Solution:**
```python
def manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """Calculate Manhattan distance between two grid positions.

    Manhattan distance is the sum of absolute differences in coordinates.
    Also known as L1 distance or taxicab distance. This is the optimal
    admissible heuristic for 4-directional grid movement.

    Args:
        pos1: Starting position as (row, col) tuple
        pos2: Target position as (row, col) tuple

    Returns:
        Manhattan distance as non-negative integer

    Examples:
        >>> manhattan_distance((0, 0), (3, 4))
        7
        >>> manhattan_distance((5, 5), (5, 5))
        0

    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
```

### 5. Inconsistent Code Style

**Problem:**
```python
# Mixing styles
def calculateDistance(Pos1,pos2):  # camelCase + inconsistent spacing
    x=abs(Pos1[0]-pos2[0])        # no spaces around operators
    Y = abs(Pos1[1] - pos2[1])     # inconsistent variable names
    return x+Y
```

**Why it's wrong:**
- Hard to read
- Looks unprofessional
- Makes code reviews difficult

**Solution:** Use ruff to enforce consistent style:
```bash
ruff check src/
ruff format src/
```

Result:
```python
def manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """Calculate Manhattan distance between two positions."""
    x_diff = abs(pos1[0] - pos2[0])
    y_diff = abs(pos1[1] - pos2[1])
    return x_diff + y_diff
```

### 6. Hardcoded Values in Tests

**Problem:**
```python
def test_various_distances():
    """Hardcoded test values"""
    assert manhattan_distance((0, 0), (3, 4)) == 7
    assert manhattan_distance((0, 0), (5, 12)) == 17
    assert manhattan_distance((2, 3), (7, 8)) == 10
    # Where do these numbers come from?
```

**Why it's wrong:**
- Hard to verify correctness
- Can't see the pattern or logic
- Difficult to maintain

**Solution:**
```python
@pytest.mark.parametrize("start,goal", [
    ((0, 0), (3, 4)),
    ((0, 0), (5, 12)),
    ((2, 3), (7, 8)),
])
def test_manhattan_matches_sum_of_differences(start, goal):
    """Manhattan should equal sum of coordinate differences."""
    expected = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    actual = manhattan_distance(start, goal)
    assert actual == expected, f"Failed for {start} -> {goal}"
```

## Mini Project Task

### This Week's Challenge: Achieve Professional Code Quality

Your goal is to bring the pathfinding lab to professional standards suitable for sharing or portfolio inclusion.

### Task 1: Write 10 New Edge Case Tests

Create `tests/test_edge_cases.py` covering:

1. **Empty grid test**: 0x0 or 1x1 grid
2. **Start equals goal**: Should return immediate success
3. **Completely blocked goal**: No path exists
4. **Out of bounds**: Start or goal outside grid
5. **Negative coordinates**: Invalid positions
6. **Obstacles at start/goal**: Invalid configuration
7. **Single valid path**: Grid forces one route
8. **Large grid performance**: 100x100 or larger
9. **All diagonal movements**: Test 8-directional thoroughly
10. **Heuristic edge cases**: Zero distance, same row/col

Example structure:
```python
"""Edge case tests for pathfinding algorithms."""
import pytest
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def test_empty_grid():
    """Test behavior with minimal 1x1 grid."""
    # Your implementation

def test_start_equals_goal():
    """Test when start and goal are the same position."""
    # Your implementation

# ... 8 more tests
```

### Task 2: Comprehensive README Documentation

Update `/home/runner/work/ai-pathfinding-gradio-lab/ai-pathfinding-gradio-lab/README.md` with:

1. **Project Overview**: What it does and why
2. **Features List**: Algorithms, visualizations, benchmarks
3. **Installation Instructions**: Step-by-step setup
4. **Quick Start Guide**: Basic usage example
5. **Usage Examples**: Code snippets for common tasks
6. **Algorithm Descriptions**: Brief explanation of each
7. **Project Structure**: Directory organization
8. **Development Setup**: Running tests, linting
9. **Contributing Guidelines**: How others can help
10. **License**: MIT license information

Aim for 150-200 lines of clear, helpful documentation.

### Task 3: Run Code Quality Tools

Run ruff and mypy to find and fix issues:

```bash
# Install tools if needed
pip install ruff mypy

# Check code style
ruff check src/pathfinding_lab

# Format code automatically
ruff format src/pathfinding_lab

# Run type checking
mypy src/pathfinding_lab

# Run tests with coverage
pytest --cov=src/pathfinding_lab --cov-report=html
```

**Fix at least 5 issues** found by these tools. Common fixes:
- Add missing type hints
- Remove unused imports
- Fix line length violations (>100 chars)
- Add docstrings to public functions
- Fix inconsistent naming

### Task 4: Document One Algorithm Thoroughly

Choose one algorithm (BFS, A*, or Dijkstra) and add comprehensive documentation:

1. **Module docstring**: Algorithm overview and references
2. **Function docstring**: Complete with Args, Returns, Examples
3. **Inline comments**: Explain non-obvious logic
4. **Type hints**: All parameters and return types
5. **Complexity analysis**: Time and space in docstring

Example:
```python
"""Breadth-First Search (BFS) pathfinding algorithm.

BFS explores nodes in order of increasing distance from start, guaranteeing
the shortest path in unweighted graphs. Uses a FIFO queue to process nodes.

References:
    - Introduction to Algorithms (CLRS), Chapter 22.2
    - https://en.wikipedia.org/wiki/Breadth-first_search
"""

def bfs(
    grid: Grid,
    start: tuple[int, int],
    goal: tuple[int, int]
) -> PathfindingResult:
    """Find shortest path using Breadth-First Search.

    Args:
        grid: Grid object containing obstacles and movement rules
        start: Starting position (row, col)
        goal: Target position (row, col)

    Returns:
        PathfindingResult with path, cost, and statistics

    Raises:
        ValueError: If start or goal is out of bounds or in obstacle

    Examples:
        >>> grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
        >>> result = bfs(grid, (0, 0), (9, 9))
        >>> print(f"Path length: {result.path_length}")
        Path length: 19

    Time Complexity: O(V + E) where V is vertices, E is edges
    Space Complexity: O(V) for queue and visited set
    """
    # Implementation...
```

### Success Criteria

- ✅ 10 new edge case tests in `tests/test_edge_cases.py`
- ✅ All tests pass when running `pytest`
- ✅ README.md has 150+ lines with all required sections
- ✅ No ruff errors: `ruff check src/` returns clean
- ✅ Code formatted: `ruff format src/` applied
- ✅ At least 5 mypy issues fixed
- ✅ One algorithm has complete documentation
- ✅ Test coverage above 80% for core modules
- ✅ All public functions have docstrings
- ✅ Project structure follows professional standards

### Bonus Challenges

- Add GitHub Actions CI/CD workflow
- Generate API documentation with Sphinx
- Add pre-commit hooks for automatic formatting
- Write property-based tests with Hypothesis
- Add performance benchmarks to test suite

## Reflection Questions

1. **Test Coverage Analysis**: After running pytest with coverage, which parts of your code have low coverage? Why might some code be harder to test than others? What strategies could you use to test visualization or UI code?

2. **Documentation Quality**: Compare the documentation in your project before and after this week. What makes documentation "good"? How would you evaluate if your README is helpful to a newcomer? What's the right balance between too little and too much documentation?

3. **Code Quality Tools**: Which issues did ruff and mypy find most frequently in your code? Were any surprising? How do these tools change your coding habits? What are the limitations of automated tools - what can't they catch?

4. **Testing Philosophy**: Should you test private/internal functions or only public APIs? When is it okay to have less than 100% test coverage? How do you decide what's important to test versus what's not worth the effort?

5. **Professional Standards**: What makes code "professional" or "production-ready"? How does this project compare to open source projects you've seen on GitHub? What would you need to add to make this suitable for your portfolio or resume?

## Additional Resources

### pytest Documentation
- [pytest Official Docs](https://docs.pytest.org/) - Comprehensive guide
- [pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html) - Reusable test setup
- [pytest Parametrize](https://docs.pytest.org/en/stable/parametrize.html) - Multiple test cases

### Code Quality Tools
- [Ruff Documentation](https://docs.astral.sh/ruff/) - Fast Python linter
- [Mypy Documentation](https://mypy.readthedocs.io/) - Static type checker
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/) - Python style conventions
- [Type Hints Tutorial](https://docs.python.org/3/library/typing.html) - Python typing module

### Documentation Guides
- [Write the Docs](https://www.writethedocs.org/) - Documentation community
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) - Docstring examples
- [NumPy Documentation Guide](https://numpydoc.readthedocs.io/) - Scientific Python docs
- [README Template](https://github.com/othneildrew/Best-README-Template) - Professional README examples

### Testing Best Practices
- [Testing Best Practices](https://testdriven.io/blog/testing-best-practices/) - Comprehensive guide
- [Effective Python Testing](https://realpython.com/pytest-python-testing/) - pytest tutorial
- [Test-Driven Development](https://www.obeythetestinggoat.com/) - TDD book online

### Project Structure
- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/) - Official guide
- [Python Application Layouts](https://realpython.com/python-application-layouts/) - Structure patterns
- [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) - Modern tooling

## Next Week Preview

**Week 12: Capstone Project - Build Your Own Pathfinding Challenge**

Next week, you'll design and implement a custom pathfinding scenario:
- Create a unique maze or obstacle pattern
- Implement a custom heuristic or algorithm variant
- Build a complete visualization and benchmark comparison
- Present your findings with graphs and analysis

This is your chance to be creative and showcase everything you've learned. Think about interesting scenarios like:
- Maze with moving obstacles
- Multi-agent pathfinding
- Terrain with variable costs (mud, water, roads)
- 3D pathfinding on multiple floors

Start brainstorming ideas now!

---

**Continue to Week 12: Capstone Project →**
