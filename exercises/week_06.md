# Week 6: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 5 Exercises](week_05.md)** | **📚 [Week 6 Documentation](../docs/week_06_heuristics.md)** | **✅ [Week 6 Solutions](../solutions/week_06_solutions.md)** | **➡️ [Next: Week 7 Exercises](week_07.md)**

---

## Beginner Exercise: Distance Metric Calculator

### Task

Create a function that computes all four standard distance metrics (Manhattan, Euclidean, Chebyshev, Octile) between two positions and displays the results. This will help you understand how different heuristics estimate distance.

### Requirements

- Write a function `compare_distances(pos1: tuple[int, int], pos2: tuple[int, int]) -> dict[str, float]`
- Return a dictionary with keys: "Manhattan", "Euclidean", "Chebyshev", "Octile"
- Each value should be the computed distance using that metric
- Test with at least 5 different position pairs
- Identify which metric gives the smallest/largest estimates for each test case

### Hints

- Manhattan: `|x1 - x2| + |y1 - y2|`
- Euclidean: `sqrt((x1 - x2)^2 + (y1 - y2)^2)`
- Chebyshev: `max(|x1 - x2|, |y1 - y2|)`
- Octile: `(dx + dy) + (sqrt(2) - 2) * min(dx, dy)` where `dx = |x1 - x2|`, `dy = |y1 - y2|`
- Use `math.sqrt()` for square roots
- Consider edge cases: same position, horizontal/vertical only, pure diagonal

### Example Output

```python
pos1 = (0, 0)
pos2 = (10, 10)
distances = compare_distances(pos1, pos2)
print(distances)
# Output:
# {
#   'Manhattan': 20.0,
#   'Euclidean': 14.142135623730951,
#   'Chebyshev': 10.0,
#   'Octile': 14.142135623730951
# }
```

### Test Cases

1. **Pure diagonal**: `(0, 0)` to `(10, 10)` - Octile and Euclidean should be most accurate
2. **Horizontal only**: `(0, 0)` to `(10, 0)` - All metrics should give same result
3. **Vertical only**: `(0, 0)` to `(0, 10)` - All metrics should give same result
4. **L-shaped**: `(0, 0)` to `(5, 15)` - Manhattan overestimates for diagonal movement
5. **Same position**: `(5, 5)` to `(5, 5)` - All should return 0.0

## Intermediate Exercise: Admissibility Tester

### Task

Build a tool that tests whether a given heuristic is admissible on a specific grid. Your tool should compare the heuristic's estimates against the true optimal costs computed by Dijkstra's algorithm.

### Requirements

- Write a function `test_admissibility(grid: Grid, start: Position, goal: Position, heuristic: Callable, sample_size: int = 20) -> dict`
- Sample `sample_size` random positions on the grid
- For each position, compare `heuristic(position, goal)` against Dijkstra's true cost from that position to goal
- Return a dictionary with:
  - `"admissible": bool` - True if all samples satisfy h(n) ≤ h*(n)
  - `"violations": list` - List of positions where heuristic overestimated
  - `"max_overestimate": float` - Maximum amount of overestimation found
  - `"accuracy_stats": dict` - Mean and max percentage error
- Test on at least 3 different heuristics (Manhattan, Euclidean, Octile)
- Test on both 4-directional and 8-directional grids

### Hints

- Run Dijkstra from each sampled position to the goal to get h*(n)
- An admissible heuristic must satisfy: `h(n) ≤ h*(n)` for all n
- Percentage error: `(h_estimate - h_true) / h_true * 100`
- Be careful with 4-directional vs 8-directional grid configurations
- Manhattan should be admissible on 4-directional, but underestimate on 8-directional
- Octile should be admissible on standard 8-directional grids

### Example Test Scenarios

```python
# Scenario 1: Manhattan on 4-directional grid
grid_4dir = Grid(20, 20, allow_diagonal=False)
result = test_admissibility(grid_4dir, (0, 0), (19, 19), manhattan_distance)
assert result["admissible"] == True

# Scenario 2: Manhattan on 8-directional grid (still admissible, just inefficient)
grid_8dir = Grid(20, 20, allow_diagonal=True)
result = test_admissibility(grid_8dir, (0, 0), (19, 19), manhattan_distance)
assert result["admissible"] == True  # Never overestimates, but underestimates

# Scenario 3: Test a weighted heuristic that overestimates
weighted_heuristic = lambda p1, p2: manhattan_distance(p1, p2) * 1.2
result = test_admissibility(grid_4dir, (0, 0), (19, 19), weighted_heuristic)
assert result["admissible"] == False
print(f"Violations found: {len(result['violations'])}")
```

## Advanced Exercise: Heuristic Performance Analyzer

### Task

Create a comprehensive benchmarking framework that compares multiple heuristics across different grid types and scenarios. Your framework should quantify the speed-optimality tradeoff.

### Requirements

- Write a class `HeuristicBenchmark` with the following methods:
  - `add_heuristic(name: str, heuristic: Callable, weight: float = 1.0)`
  - `add_test_case(grid: Grid, start: Position, goal: Position, name: str)`
  - `run_benchmarks() -> pd.DataFrame` (or return a list of dictionaries)
  - `generate_report() -> str` - Create a formatted summary table
- For each heuristic × test case combination, measure:
  - Nodes visited (efficiency)
  - Path cost (optimality)
  - Runtime in milliseconds (speed)
  - Path length (number of steps)
  - Suboptimality ratio: `path_cost / optimal_cost` (1.0 = optimal)
- Include at least 6 heuristics:
  - Zero (Dijkstra)
  - Manhattan
  - Euclidean
  - Octile
  - Weighted Manhattan (w=1.3)
  - Weighted Manhattan (w=1.5)
- Test on at least 3 different scenarios:
  - Open grid (few obstacles)
  - Maze-like grid (many obstacles)
  - Weighted terrain (varying movement costs)

### Hints

- Use A* search with different heuristics as parameters
- Run Dijkstra first to establish the true optimal cost
- Measure time with `time.time()` before/after each search
- Weighted heuristic: `f(n) = g(n) + w * h(n)`
- Create diverse test grids: open, cluttered, weighted
- Consider using a table format library or just string formatting
- Look for patterns: Does weighted A* explore fewer nodes? By how much?

### Example Output Format

```
Heuristic Performance Benchmark Results
========================================

Test Case: Open 30x30 Grid (Start: (2,2), Goal: (28,28))
---------------------------------------------------------
Heuristic         | Nodes | Path Cost | Runtime | Suboptimality
------------------|-------|-----------|---------|---------------
Zero (Dijkstra)   |   842 |     37.56 |   8.23ms|    1.000x
Manhattan         |   234 |     37.56 |   3.12ms|    1.000x
Euclidean         |   198 |     37.56 |   3.45ms|    1.000x
Octile            |   176 |     37.56 |   2.89ms|    1.000x
Weighted (1.3)    |   123 |     38.21 |   2.01ms|    1.017x
Weighted (1.5)    |    87 |     39.45 |   1.56ms|    1.050x

Test Case: Maze 30x30 Grid (Start: (1,1), Goal: (28,28))
---------------------------------------------------------
Heuristic         | Nodes | Path Cost | Runtime | Suboptimality
------------------|-------|-----------|---------|---------------
Zero (Dijkstra)   |   567 |     52.14 |   6.78ms|    1.000x
Manhattan         |   312 |     52.14 |   4.23ms|    1.000x
Euclidean         |   289 |     52.14 |   4.56ms|    1.000x
Octile            |   267 |     52.14 |   3.98ms|    1.000x
Weighted (1.3)    |   198 |     53.89 |   3.12ms|    1.034x
Weighted (1.5)    |   145 |     56.23 |   2.45ms|    1.078x

Summary:
--------
- Octile consistently explores fewest nodes on open grids
- Weighted heuristics trade 1-8% optimality for 30-50% speed improvement
- Manhattan is 2-3x faster than Dijkstra with no loss of optimality
- Weight 1.5 provides best speed gains but ~5-8% longer paths
```

### Analysis Questions

After running your benchmarks, answer:
1. Which admissible heuristic is most efficient (fewest nodes)?
2. How much does weighted A* (w=1.5) improve speed vs standard A*?
3. What's the typical suboptimality ratio for weighted A* (w=1.3)?
4. Does heuristic choice matter more on open grids or mazes?

## Debugging Challenge: Broken Distance Functions

### Buggy Code

```python
import math
from pathfinding_lab.core.types import Position


def buggy_manhattan(pos1: Position, pos2: Position) -> float:
    """Manhattan distance with bugs."""
    row1, col1 = pos1
    row2, col2 = pos2
    # Bug 1: Missing absolute value on one dimension
    return abs(row1 - row2) + (col1 - col2)


def buggy_euclidean(pos1: Position, pos2: Position) -> float:
    """Euclidean distance with bugs."""
    row1, col1 = pos1
    row2, col2 = pos2
    # Bug 2: Forgot to take square root
    return (row1 - row2) ** 2 + (col1 - col2) ** 2


def buggy_chebyshev(pos1: Position, pos2: Position) -> float:
    """Chebyshev distance with bugs."""
    row1, col1 = pos1
    row2, col2 = pos2
    # Bug 3: Using min instead of max
    return min(abs(row1 - row2), abs(col1 - col2))


def buggy_octile(pos1: Position, pos2: Position) -> float:
    """Octile distance with bugs."""
    row1, col1 = pos1
    row2, col2 = pos2

    dx = abs(row1 - row2)
    dy = abs(col1 - col2)

    D = 1.0
    D2 = math.sqrt(2)

    # Bug 4: Using max instead of min for diagonal calculation
    return D * (dx + dy) + (D2 - 2 * D) * max(dx, dy)


def buggy_weighted_manhattan(pos1: Position, pos2: Position, weight: float = 1.5) -> float:
    """Weighted Manhattan distance with bugs."""
    row1, col1 = pos1
    row2, col2 = pos2
    manhattan = abs(row1 - row2) + abs(col1 - col2)
    # Bug 5: Weight applied incorrectly (division instead of multiplication)
    return manhattan / weight
```

### Expected Behavior

Each function should correctly implement its respective distance metric:

1. **Manhattan**: Sum of absolute differences in both dimensions
2. **Euclidean**: Square root of sum of squared differences
3. **Chebyshev**: Maximum of absolute differences (not minimum)
4. **Octile**: Accounts for diagonal moves costing √2 and cardinal moves costing 1
5. **Weighted Manhattan**: Manhattan distance multiplied by weight

### Test Cases

```python
# Test positions
pos1 = (0, 0)
pos2 = (3, 4)

# Expected correct outputs:
# Manhattan: 7.0 (3 + 4)
# Euclidean: 5.0 (sqrt(9 + 16) = sqrt(25))
# Chebyshev: 4.0 (max(3, 4))
# Octile: 5.828... (approx 5.83)
# Weighted (1.5): 10.5 (7.0 * 1.5)

# Buggy outputs will differ!
```

### Hints

- Test each function with simple cases where you know the answer
- **Bug 1**: Manhattan needs absolute value on BOTH dimensions
- **Bug 2**: Euclidean is the square ROOT of sum of squares
- **Bug 3**: Chebyshev takes the MAX, not MIN (think: king's move in chess)
- **Bug 4**: Octile uses MIN(dx, dy) for diagonal moves, not MAX
- **Bug 5**: Weighted heuristic should MULTIPLY, not divide
- Try position pairs like (0, 0) to (3, 4) or (0, 0) to (10, 10)
- Compare buggy outputs to your correct implementations from Beginner Exercise

### Additional Challenge

After fixing all bugs:
1. Verify that each fixed function is admissible for its intended use case
2. Test with positions in all four quadrants (negative coordinates if supported)
3. Write unit tests to prevent these bugs from reappearing

---

**See solutions/week_06_solutions.md for complete answers and explanations**

---

**✅ [See Solutions](../solutions/week_06_solutions.md)** | **📚 [Back to Week 6 Docs](../docs/week_06_heuristics.md)** | **➡️ [Next: Week 7 Exercises](week_07.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
