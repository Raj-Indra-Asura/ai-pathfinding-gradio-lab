# Week 6: Solutions

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 5 Solutions](week_05_solutions.md)** | **📚 [Week 6 Documentation](../docs/week_06_heuristics.md)** | **📝 [Week 6 Exercises](../exercises/week_06.md)** | **➡️ [Next: Week 7 Solutions](week_07_solutions.md)**

---

## Beginner Exercise Solution: Distance Metric Calculator

### Explanation

This exercise teaches you to implement the four fundamental distance metrics used in pathfinding. Each metric has different properties and is suited for different grid configurations:

- **Manhattan**: Best for 4-directional grids (taxicab geometry)
- **Euclidean**: Straight-line distance, good for continuous spaces
- **Chebyshev**: Best for 8-directional grids with uniform costs
- **Octile**: Most accurate for standard 8-directional grids (diagonals cost √2)

The key is understanding when each metric is admissible and how they compare in different scenarios.

### Code

```python
import math
from typing import Dict


def compare_distances(pos1: tuple[int, int], pos2: tuple[int, int]) -> Dict[str, float]:
    """
    Calculate all four standard distance metrics between two positions.

    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)

    Returns:
        Dictionary with all four distance metrics
    """
    row1, col1 = pos1
    row2, col2 = pos2

    # Calculate absolute differences
    dx = abs(row1 - row2)
    dy = abs(col1 - col2)

    # Manhattan distance (L1 norm)
    manhattan = dx + dy

    # Euclidean distance (L2 norm)
    euclidean = math.sqrt(dx**2 + dy**2)

    # Chebyshev distance (L∞ norm)
    chebyshev = max(dx, dy)

    # Octile distance (optimal for 8-directional with diagonal cost √2)
    D = 1.0  # Cardinal cost
    D2 = math.sqrt(2)  # Diagonal cost
    octile = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    return {
        'Manhattan': manhattan,
        'Euclidean': euclidean,
        'Chebyshev': chebyshev,
        'Octile': octile
    }


def analyze_distances():
    """Run test cases and analyze the results."""
    test_cases = [
        ((0, 0), (10, 10), "Pure diagonal"),
        ((0, 0), (10, 0), "Horizontal only"),
        ((0, 0), (0, 10), "Vertical only"),
        ((0, 0), (5, 15), "L-shaped"),
        ((5, 5), (5, 5), "Same position"),
    ]

    print("Distance Metric Comparison")
    print("=" * 80)

    for pos1, pos2, description in test_cases:
        distances = compare_distances(pos1, pos2)
        print(f"\n{description}: {pos1} -> {pos2}")
        print("-" * 80)
        for metric, value in distances.items():
            print(f"  {metric:12s}: {value:8.3f}")

        # Find min and max
        min_metric = min(distances, key=distances.get)
        max_metric = max(distances, key=distances.get)
        print(f"  Smallest: {min_metric} ({distances[min_metric]:.3f})")
        print(f"  Largest: {max_metric} ({distances[max_metric]:.3f})")


if __name__ == "__main__":
    analyze_distances()
```

### Example Output

```
Distance Metric Comparison
================================================================================

Pure diagonal: (0, 0) -> (10, 10)
--------------------------------------------------------------------------------
  Manhattan   :   20.000
  Euclidean   :   14.142
  Chebyshev   :   10.000
  Octile      :   14.142
  Smallest: Chebyshev (10.000)
  Largest: Manhattan (20.000)

Horizontal only: (0, 0) -> (10, 0)
--------------------------------------------------------------------------------
  Manhattan   :   10.000
  Euclidean   :   10.000
  Chebyshev   :   10.000
  Octile      :   10.000
  Smallest: Manhattan (10.000)
  Largest: Manhattan (10.000)

L-shaped: (0, 0) -> (5, 15)
--------------------------------------------------------------------------------
  Manhattan   :   20.000
  Euclidean   :   15.811
  Chebyshev   :   15.000
  Octile      :   17.071
  Smallest: Chebyshev (15.000)
  Largest: Manhattan (20.000)
```

### Key Concepts

- **Manhattan is always the largest or tied** (sum of absolute differences)
- **Chebyshev is always the smallest or tied** (max of absolute differences)
- **Euclidean and Octile are close** for diagonal-heavy paths
- **All metrics agree** on purely horizontal or vertical paths
- **Manhattan significantly overestimates** on diagonal-heavy paths (40% for pure diagonal)

### Testing Advice

1. Test with **edge cases**: same position, zero distance in one dimension
2. **Verify admissibility**: All four should be ≤ actual path cost for their intended use
3. Test with **negative coordinates** if your system supports them
4. **Compare to known values**: (3, 4) triangle gives Euclidean = 5.0 (Pythagorean triple)
5. **Visualize on paper**: Draw the grid and manually count the minimum steps

## Intermediate Exercise Solution: Admissibility Tester

### Explanation

This exercise tests whether a heuristic is **admissible** by comparing its estimates against ground truth from Dijkstra's algorithm. A heuristic h(n) is admissible if it never overestimates: `h(n) ≤ h*(n)` for all nodes n.

**Key insights**:
- Run Dijkstra from sampled positions to the goal to get h*(n)
- Compare heuristic estimate h(n) against this true cost
- Track violations, max overestimate, and accuracy statistics
- Admissible heuristics might underestimate, but never overestimate

### Code

```python
import random
from typing import Callable, Dict, List
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import Position
from pathfinding_lab.algorithms.dijkstra import dijkstra


def test_admissibility(
    grid: Grid,
    start: Position,
    goal: Position,
    heuristic: Callable[[Position, Position], float],
    sample_size: int = 20
) -> Dict:
    """
    Test whether a heuristic is admissible by comparing against Dijkstra's true costs.

    Args:
        grid: The grid to test on
        start: Starting position (not used, but kept for consistency)
        goal: Goal position
        heuristic: Heuristic function to test
        sample_size: Number of random positions to sample

    Returns:
        Dictionary with admissibility test results
    """
    violations: List[Position] = []
    overestimates: List[float] = []
    percentage_errors: List[float] = []

    # Sample random valid positions on the grid
    sample_positions = []
    attempts = 0
    while len(sample_positions) < sample_size and attempts < sample_size * 10:
        row = random.randint(0, grid.height - 1)
        col = random.randint(0, grid.width - 1)
        pos = (row, col)

        # Only sample walkable positions different from goal
        if grid.is_walkable(pos) and pos != goal:
            sample_positions.append(pos)
        attempts += 1

    # Test each sampled position
    for pos in sample_positions:
        # Get heuristic estimate
        h_estimate = heuristic(pos, goal)

        # Get true cost using Dijkstra
        result = dijkstra(grid, pos, goal)

        if not result.success:
            # Skip unreachable positions
            continue

        h_true = result.path_cost

        # Check for overestimation (admissibility violation)
        if h_estimate > h_true + 1e-6:  # Small epsilon for floating point errors
            violations.append(pos)
            overestimate = h_estimate - h_true
            overestimates.append(overestimate)

        # Calculate percentage error
        if h_true > 0:
            pct_error = ((h_estimate - h_true) / h_true) * 100
            percentage_errors.append(pct_error)

    # Compile results
    is_admissible = len(violations) == 0
    max_overestimate = max(overestimates) if overestimates else 0.0

    accuracy_stats = {
        'mean_pct_error': sum(percentage_errors) / len(percentage_errors) if percentage_errors else 0.0,
        'max_pct_error': max(percentage_errors) if percentage_errors else 0.0,
        'min_pct_error': min(percentage_errors) if percentage_errors else 0.0,
    }

    return {
        'admissible': is_admissible,
        'violations': violations,
        'max_overestimate': max_overestimate,
        'accuracy_stats': accuracy_stats,
        'samples_tested': len(sample_positions)
    }


def run_admissibility_tests():
    """Run comprehensive admissibility tests on various heuristics."""
    from pathfinding_lab.heuristics.manhattan import manhattan_distance
    from pathfinding_lab.heuristics.euclidean import euclidean_distance
    from pathfinding_lab.heuristics.octile import octile_distance

    print("Admissibility Testing Results")
    print("=" * 80)

    # Test 1: Manhattan on 4-directional grid
    print("\nTest 1: Manhattan on 4-directional grid")
    print("-" * 80)
    grid_4dir = Grid(20, 20)
    grid_4dir.allow_diagonal = False
    result = test_admissibility(grid_4dir, (0, 0), (19, 19), manhattan_distance, sample_size=30)
    print(f"Admissible: {result['admissible']}")
    print(f"Violations: {len(result['violations'])}")
    print(f"Mean % error: {result['accuracy_stats']['mean_pct_error']:.2f}%")
    print(f"Max % error: {result['accuracy_stats']['max_pct_error']:.2f}%")

    # Test 2: Manhattan on 8-directional grid (should underestimate)
    print("\nTest 2: Manhattan on 8-directional grid")
    print("-" * 80)
    grid_8dir = Grid(20, 20)
    grid_8dir.allow_diagonal = True
    result = test_admissibility(grid_8dir, (0, 0), (19, 19), manhattan_distance, sample_size=30)
    print(f"Admissible: {result['admissible']}")
    print(f"Violations: {len(result['violations'])}")
    print(f"Mean % error: {result['accuracy_stats']['mean_pct_error']:.2f}%")
    print("Note: Negative % means underestimate (still admissible)")

    # Test 3: Octile on 8-directional grid
    print("\nTest 3: Octile on 8-directional grid")
    print("-" * 80)
    result = test_admissibility(grid_8dir, (0, 0), (19, 19), octile_distance, sample_size=30)
    print(f"Admissible: {result['admissible']}")
    print(f"Violations: {len(result['violations'])}")
    print(f"Mean % error: {result['accuracy_stats']['mean_pct_error']:.2f}%")

    # Test 4: Weighted heuristic that overestimates
    print("\nTest 4: Weighted Manhattan (w=1.2) on 4-directional grid")
    print("-" * 80)
    weighted_heuristic = lambda p1, p2: manhattan_distance(p1, p2) * 1.2
    result = test_admissibility(grid_4dir, (0, 0), (19, 19), weighted_heuristic, sample_size=30)
    print(f"Admissible: {result['admissible']}")
    print(f"Violations: {len(result['violations'])}")
    print(f"Max overestimate: {result['max_overestimate']:.2f}")
    print(f"Max % error: {result['accuracy_stats']['max_pct_error']:.2f}%")


if __name__ == "__main__":
    run_admissibility_tests()
```

### Key Concepts

- **Admissibility requires h(n) ≤ h*(n)** for ALL nodes, not just most
- **Dijkstra gives ground truth** - it always finds optimal costs
- **Underestimating is okay** - Manhattan on 8-directional grids underestimates but is still admissible
- **Sampling is practical** - Testing all nodes is expensive, random sampling catches violations
- **Floating point tolerance** - Use epsilon (1e-6) when comparing due to numerical errors

### Testing Advice

1. **Test on different grid types**: 4-directional, 8-directional, with obstacles
2. **Sample size matters**: Use at least 20-30 samples for reliable results
3. **Check negative errors**: Negative % error means underestimate (admissible, but inefficient)
4. **Test corner cases**: Positions near goal, far from goal, blocked paths
5. **Verify with known inadmissible heuristics**: Weighted heuristics with w > 1.0 should fail

## Advanced Exercise Solution: Heuristic Performance Analyzer

### Explanation

This comprehensive benchmarking framework measures the speed-optimality tradeoff for different heuristics. It quantifies how much speed you gain by using weighted heuristics at the cost of suboptimal paths.

**Key metrics**:
- **Nodes visited**: Lower is better (efficiency)
- **Path cost**: Should match optimal for admissible heuristics
- **Runtime**: Real-world speed in milliseconds
- **Suboptimality ratio**: `path_cost / optimal_cost` (1.0 = optimal)

### Code

```python
import time
from typing import Callable, List, Dict, Tuple, Optional
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import Position
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.dijkstra import dijkstra


class HeuristicBenchmark:
    """Comprehensive benchmarking framework for heuristic comparison."""

    def __init__(self):
        self.heuristics: List[Tuple[str, Callable, float]] = []
        self.test_cases: List[Tuple[Grid, Position, Position, str]] = []
        self.results: List[Dict] = []

    def add_heuristic(self, name: str, heuristic: Callable, weight: float = 1.0):
        """
        Add a heuristic to benchmark.

        Args:
            name: Display name for the heuristic
            heuristic: Heuristic function
            weight: Weight multiplier (1.0 = standard, >1.0 = weighted A*)
        """
        self.heuristics.append((name, heuristic, weight))

    def add_test_case(self, grid: Grid, start: Position, goal: Position, name: str):
        """
        Add a test case to benchmark.

        Args:
            grid: Grid to test on
            start: Starting position
            goal: Goal position
            name: Description of this test case
        """
        self.test_cases.append((grid, start, goal, name))

    def run_benchmarks(self) -> List[Dict]:
        """
        Run all benchmarks and collect results.

        Returns:
            List of result dictionaries
        """
        self.results = []

        for grid, start, goal, test_name in self.test_cases:
            # First, run Dijkstra to get optimal cost
            dijkstra_result = dijkstra(grid, start, goal)
            optimal_cost = dijkstra_result.path_cost if dijkstra_result.success else float('inf')

            print(f"\nRunning benchmarks for: {test_name}")
            print("-" * 60)

            # Test each heuristic
            for heuristic_name, heuristic_func, weight in self.heuristics:
                # Create weighted heuristic if needed
                if weight == 1.0:
                    weighted_heuristic = heuristic_func
                else:
                    weighted_heuristic = lambda p1, p2, h=heuristic_func, w=weight: w * h(p1, p2)

                # Run A* with this heuristic
                start_time = time.time()
                result = astar(grid, start, goal, weighted_heuristic)
                runtime_ms = (time.time() - start_time) * 1000

                # Calculate metrics
                if result.success:
                    suboptimality = result.path_cost / optimal_cost if optimal_cost > 0 else 1.0
                else:
                    suboptimality = float('inf')

                # Store results
                self.results.append({
                    'test_case': test_name,
                    'heuristic': heuristic_name,
                    'weight': weight,
                    'nodes_visited': result.nodes_visited,
                    'path_cost': result.path_cost if result.success else float('inf'),
                    'runtime_ms': runtime_ms,
                    'path_length': len(result.path) if result.success else 0,
                    'suboptimality': suboptimality,
                    'optimal_cost': optimal_cost,
                    'success': result.success
                })

                print(f"  {heuristic_name:20s} - Nodes: {result.nodes_visited:4d}, "
                      f"Cost: {result.path_cost:.2f}, Time: {runtime_ms:.2f}ms")

        return self.results

    def generate_report(self) -> str:
        """Generate a formatted summary report."""
        if not self.results:
            return "No results to report. Run benchmarks first."

        report_lines = ["", "Heuristic Performance Benchmark Results", "=" * 80, ""]

        # Group results by test case
        test_cases = {}
        for result in self.results:
            test_name = result['test_case']
            if test_name not in test_cases:
                test_cases[test_name] = []
            test_cases[test_name].append(result)

        # Generate report for each test case
        for test_name, results in test_cases.items():
            report_lines.append(f"Test Case: {test_name}")
            report_lines.append("-" * 80)
            report_lines.append(f"{'Heuristic':<20} | {'Nodes':>6} | {'Path Cost':>10} | {'Runtime':>8} | {'Subopt':>8}")
            report_lines.append("-" * 80)

            for result in results:
                heuristic_label = result['heuristic']
                if result['weight'] != 1.0:
                    heuristic_label += f" (w={result['weight']:.1f})"

                report_lines.append(
                    f"{heuristic_label:<20} | "
                    f"{result['nodes_visited']:>6} | "
                    f"{result['path_cost']:>10.2f} | "
                    f"{result['runtime_ms']:>7.2f}ms | "
                    f"{result['suboptimality']:>7.3f}x"
                )

            report_lines.append("")

        # Add summary analysis
        report_lines.append("Summary Analysis:")
        report_lines.append("-" * 80)

        # Find best admissible heuristic (suboptimality = 1.0)
        admissible_results = [r for r in self.results if abs(r['suboptimality'] - 1.0) < 0.01]
        if admissible_results:
            best_admissible = min(admissible_results, key=lambda r: r['nodes_visited'])
            report_lines.append(f"- Most efficient admissible: {best_admissible['heuristic']} "
                              f"({best_admissible['nodes_visited']} nodes avg)")

        # Analyze weighted heuristics
        weighted_results = [r for r in self.results if r['weight'] > 1.0]
        if weighted_results:
            avg_speedup = sum(r['nodes_visited'] for r in admissible_results) / len(admissible_results) if admissible_results else 0
            avg_weighted = sum(r['nodes_visited'] for r in weighted_results) / len(weighted_results)
            speedup_pct = ((avg_speedup - avg_weighted) / avg_speedup * 100) if avg_speedup > 0 else 0

            avg_subopt = sum(r['suboptimality'] for r in weighted_results) / len(weighted_results)
            report_lines.append(f"- Weighted heuristics: ~{speedup_pct:.0f}% fewer nodes, "
                              f"~{(avg_subopt - 1) * 100:.1f}% longer paths")

        return "\n".join(report_lines)


def run_comprehensive_benchmark():
    """Run a complete benchmark suite."""
    from pathfinding_lab.heuristics.manhattan import manhattan_distance
    from pathfinding_lab.heuristics.euclidean import euclidean_distance
    from pathfinding_lab.heuristics.octile import octile_distance

    benchmark = HeuristicBenchmark()

    # Add heuristics
    zero_heuristic = lambda p1, p2: 0.0
    benchmark.add_heuristic("Zero (Dijkstra)", zero_heuristic)
    benchmark.add_heuristic("Manhattan", manhattan_distance)
    benchmark.add_heuristic("Euclidean", euclidean_distance)
    benchmark.add_heuristic("Octile", octile_distance)
    benchmark.add_heuristic("Weighted (1.3)", manhattan_distance, weight=1.3)
    benchmark.add_heuristic("Weighted (1.5)", manhattan_distance, weight=1.5)

    # Create test grids
    # Test 1: Open grid
    grid_open = Grid(30, 30)
    grid_open.allow_diagonal = True
    benchmark.add_test_case(grid_open, (2, 2), (28, 28), "Open 30x30 Grid")

    # Test 2: Maze (add some obstacles)
    grid_maze = Grid(30, 30)
    grid_maze.allow_diagonal = True
    # Add vertical walls with gaps
    for row in range(5, 25):
        if row % 4 != 0:  # Leave gaps every 4 rows
            grid_maze.set_obstacle((row, 10))
            grid_maze.set_obstacle((row, 20))
    benchmark.add_test_case(grid_maze, (1, 1), (28, 28), "Maze 30x30 Grid")

    # Test 3: Weighted terrain
    grid_weighted = Grid(30, 30)
    grid_weighted.allow_diagonal = True
    # Add some mud tiles (higher cost)
    for row in range(10, 20):
        for col in range(10, 20):
            grid_weighted.set_weight((row, col), 3.0)
    benchmark.add_test_case(grid_weighted, (2, 2), (28, 28), "Weighted Terrain 30x30")

    # Run benchmarks
    results = benchmark.run_benchmarks()

    # Generate and print report
    report = benchmark.generate_report()
    print(report)

    return results


if __name__ == "__main__":
    run_comprehensive_benchmark()
```

### Key Concepts

- **Zero heuristic = Dijkstra** - No heuristic guidance, explores uniformly
- **Octile is most efficient** for standard 8-directional grids among admissible heuristics
- **Weighted A* trades optimality for speed** - Weight 1.5 typically 30-50% faster with 5-8% longer paths
- **Grid type matters** - Heuristic choice has bigger impact on open grids vs mazes
- **Suboptimality is bounded** - Weight w guarantees path cost ≤ w × optimal cost

### Testing Advice

1. **Run on diverse grids**: Open, maze, weighted terrain, different sizes
2. **Multiple test runs**: Average results over 3-5 runs for stability
3. **Vary start/goal positions**: Test short, medium, and long-distance paths
4. **Compare to baseline**: Always include zero heuristic (Dijkstra) as reference
5. **Analyze tradeoffs**: Plot nodes vs suboptimality for different weights

## Debugging Challenge Solution: Broken Distance Functions

### Bugs Found

#### Bug 1: Manhattan Distance - Missing Absolute Value

**Problem**: Only taking absolute value of row difference, not column difference
```python
return abs(row1 - row2) + (col1 - col2)  # Bug: col1 - col2 can be negative
```

**Fix**:
```python
return abs(row1 - row2) + abs(col1 - col2)  # Both must be absolute values
```

**Why it matters**: Without abs() on both dimensions, the distance can be negative or incorrect, breaking admissibility.

#### Bug 2: Euclidean Distance - Forgot Square Root

**Problem**: Returning sum of squared differences instead of taking square root
```python
return (row1 - row2) ** 2 + (col1 - col2) ** 2  # Bug: missing sqrt()
```

**Fix**:
```python
return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)
```

**Why it matters**: The squared distance is always larger than the actual distance, causing massive overestimation and breaking admissibility.

#### Bug 3: Chebyshev Distance - Min Instead of Max

**Problem**: Using min() instead of max() for Chebyshev distance
```python
return min(abs(row1 - row2), abs(col1 - col2))  # Bug: should be max()
```

**Fix**:
```python
return max(abs(row1 - row2), abs(col1 - col2))
```

**Why it matters**: Chebyshev distance represents the king's move on a chessboard (maximum of dimensions), not minimum. Using min() severely underestimates diagonal distances.

#### Bug 4: Octile Distance - Max Instead of Min

**Problem**: Using max(dx, dy) for diagonal calculation instead of min(dx, dy)
```python
return D * (dx + dy) + (D2 - 2 * D) * max(dx, dy)  # Bug: should be min()
```

**Fix**:
```python
return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
```

**Why it matters**: You can only move diagonally min(dx, dy) times (limited by the shorter dimension). Using max() overestimates diagonal moves and breaks admissibility.

#### Bug 5: Weighted Manhattan - Division Instead of Multiplication

**Problem**: Dividing by weight instead of multiplying
```python
return manhattan / weight  # Bug: should multiply, not divide
```

**Fix**:
```python
return manhattan * weight
```

**Why it matters**: Dividing by weight > 1 makes the heuristic SMALLER (more admissible but less efficient). We want to multiply to make it larger (greedier search).

### Corrected Code

```python
import math
from pathfinding_lab.core.types import Position


def fixed_manhattan(pos1: Position, pos2: Position) -> float:
    """Manhattan distance - corrected."""
    row1, col1 = pos1
    row2, col2 = pos2
    return abs(row1 - row2) + abs(col1 - col2)


def fixed_euclidean(pos1: Position, pos2: Position) -> float:
    """Euclidean distance - corrected."""
    row1, col1 = pos1
    row2, col2 = pos2
    return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)


def fixed_chebyshev(pos1: Position, pos2: Position) -> float:
    """Chebyshev distance - corrected."""
    row1, col1 = pos1
    row2, col2 = pos2
    return max(abs(row1 - row2), abs(col1 - col2))


def fixed_octile(pos1: Position, pos2: Position) -> float:
    """Octile distance - corrected."""
    row1, col1 = pos1
    row2, col2 = pos2

    dx = abs(row1 - row2)
    dy = abs(col1 - col2)

    D = 1.0
    D2 = math.sqrt(2)

    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


def fixed_weighted_manhattan(pos1: Position, pos2: Position, weight: float = 1.5) -> float:
    """Weighted Manhattan distance - corrected."""
    row1, col1 = pos1
    row2, col2 = pos2
    manhattan = abs(row1 - row2) + abs(col1 - col2)
    return manhattan * weight


def test_fixed_functions():
    """Test all fixed functions with known values."""
    pos1 = (0, 0)
    pos2 = (3, 4)

    print("Testing fixed distance functions:")
    print(f"Positions: {pos1} to {pos2}")
    print("-" * 40)

    manhattan = fixed_manhattan(pos1, pos2)
    print(f"Manhattan: {manhattan:.2f} (expected: 7.0)")
    assert abs(manhattan - 7.0) < 0.01

    euclidean = fixed_euclidean(pos1, pos2)
    print(f"Euclidean: {euclidean:.2f} (expected: 5.0)")
    assert abs(euclidean - 5.0) < 0.01

    chebyshev = fixed_chebyshev(pos1, pos2)
    print(f"Chebyshev: {chebyshev:.2f} (expected: 4.0)")
    assert abs(chebyshev - 4.0) < 0.01

    octile = fixed_octile(pos1, pos2)
    print(f"Octile: {octile:.2f} (expected: ~5.83)")
    assert 5.8 < octile < 5.9

    weighted = fixed_weighted_manhattan(pos1, pos2, weight=1.5)
    print(f"Weighted (1.5): {weighted:.2f} (expected: 10.5)")
    assert abs(weighted - 10.5) < 0.01

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_fixed_functions()
```

### What You Should Understand

1. **Absolute values are critical**: Distance metrics must return non-negative values
2. **Formula precision matters**: Each metric has a specific mathematical definition
3. **Min vs Max changes everything**: Chebyshev uses max, Octile diagonal uses min
4. **Square roots can't be forgotten**: Euclidean is defined with sqrt, not squared distance
5. **Operation order matters**: Multiply for weighted heuristics, not divide
6. **Testing is essential**: Simple test cases like (0,0) to (3,4) catch most bugs
7. **Admissibility depends on correctness**: Wrong formulas can break optimality guarantees

### Additional Testing

```python
# Edge case tests
assert fixed_manhattan((5, 5), (5, 5)) == 0.0  # Same position
assert fixed_manhattan((0, 0), (10, 0)) == 10.0  # Horizontal
assert fixed_manhattan((0, 0), (0, 10)) == 10.0  # Vertical
assert fixed_euclidean((0, 0), (10, 10)) == math.sqrt(200)  # Pure diagonal
assert fixed_chebyshev((0, 0), (5, 5)) == 5.0  # Diagonal = max dimension
```

---

**Next: Week 7 Visualization Techniques →**

---

**📝 [Back to Week 6 Exercises](../exercises/week_06.md)** | **📚 [Week 6 Documentation](../docs/week_06_heuristics.md)** | **➡️ [Next: Week 7 Solutions](week_07_solutions.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
