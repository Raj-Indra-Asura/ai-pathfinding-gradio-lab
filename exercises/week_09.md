# Week 9 Exercises: Benchmarking and Performance Analysis

## Exercise 1: Basic Algorithm Benchmarking (Beginner)

**Goal**: Create a simple benchmarking script that compares BFS and A* on a single grid.

**Task**: Write a program that:
1. Creates a 20x20 grid with 20% obstacle density
2. Runs both BFS and A* 5 times each
3. Collects runtime and nodes visited for each run
4. Computes and displays average performance metrics
5. Determines which algorithm is faster

**Requirements**:
- Use the same grid and start/goal for both algorithms
- Run each algorithm exactly 5 times
- Calculate average runtime and average nodes visited
- Display results in a readable format
- Indicate which algorithm performed better

**Starter Code**:

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def benchmark_simple():
    """Benchmark BFS vs A* on a single grid."""
    # TODO: Create grid (20x20, obstacle_density=0.2)
    # TODO: Define start (0, 0) and goal (19, 19)
    # TODO: Generate obstacles

    # TODO: Run BFS 5 times, collect runtimes and nodes_visited
    bfs_runtimes = []
    bfs_nodes = []
    for _ in range(5):
        # Run BFS and collect metrics
        pass

    # TODO: Run A* 5 times, collect runtimes and nodes_visited
    astar_runtimes = []
    astar_nodes = []
    for _ in range(5):
        # Run A* with Manhattan heuristic and collect metrics
        pass

    # TODO: Calculate averages
    bfs_avg_runtime = 0.0
    bfs_avg_nodes = 0.0
    astar_avg_runtime = 0.0
    astar_avg_nodes = 0.0

    # TODO: Print results
    print("Benchmark Results")
    print("=" * 50)
    # Print BFS stats
    # Print A* stats
    # Print comparison

    # TODO: Determine winner
    pass

if __name__ == "__main__":
    benchmark_simple()
```

**Expected Output**:
```
Benchmark Results
==================================================
BFS:
  Average Runtime: 2.35 ms
  Average Nodes Visited: 156

A*:
  Average Runtime: 0.93 ms
  Average Nodes Visited: 38

A* is 2.53x faster than BFS
A* visited 4.11x fewer nodes than BFS
```

**Testing**:
1. Run the benchmark multiple times and verify results are consistent
2. Try different grid sizes (10x10, 30x30) and observe how performance scales
3. Try different obstacle densities and see how it affects the comparison

---

## Exercise 2: Multi-Scenario Benchmarking (Intermediate)

**Goal**: Create a comprehensive benchmarking suite that tests all 6 algorithms across 3 different scenarios.

**Task**: Build a benchmarking system that:
1. Defines 3 scenarios: Open Grid (5% obstacles), Moderate (20%), Maze (35%)
2. Tests all 6 algorithms on each scenario
3. Runs each algorithm 3 times per scenario
4. Creates comparison tables for each scenario
5. Exports all results to CSV files

**Requirements**:
- Test all 6 algorithms: BFS, DFS, Dijkstra, Greedy Best-First, A*, Bidirectional BFS
- Use appropriate heuristics for informed algorithms (Manhattan distance)
- Handle algorithm failures gracefully
- Create formatted comparison tables
- Export to CSV with scenario name in filename
- Display summary statistics (mean runtime, mean nodes visited)

**Starter Code**:

```python
import pandas as pd
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dfs import dfs
from pathfinding_lab.algorithms.dijkstra import dijkstra
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.greedy_best_first import greedy_best_first
from pathfinding_lab.algorithms.bidirectional_bfs import bidirectional_bfs
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.visualization.comparison_plot import create_comparison_table

def run_scenario_benchmark(scenario_name, obstacle_density, grid_size=20):
    """
    Benchmark all algorithms on a single scenario.

    Args:
        scenario_name: Name of the scenario
        obstacle_density: Obstacle density (0.0 to 1.0)
        grid_size: Size of the square grid
    """
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario_name}")
    print(f"Grid: {grid_size}x{grid_size}, Obstacle Density: {obstacle_density:.0%}")
    print(f"{'='*60}")

    # TODO: Create grid
    # TODO: Define start and goal
    # TODO: Generate obstacles

    # Define algorithms
    algorithms = [
        ("BFS", bfs, {}),
        ("DFS", dfs, {}),
        ("Dijkstra", dijkstra, {}),
        ("Greedy Best-First", greedy_best_first, {"heuristic": manhattan_distance}),
        ("A*", astar, {"heuristic": manhattan_distance}),
        ("Bidirectional BFS", bidirectional_bfs, {}),
    ]

    # TODO: Run each algorithm 3 times
    all_results = []
    for algo_name, algo_func, algo_kwargs in algorithms:
        runtimes = []
        nodes_visited_list = []
        path_lengths = []

        for run in range(3):
            try:
                # TODO: Run algorithm
                # TODO: Collect metrics
                pass
            except Exception as e:
                print(f"  {algo_name} failed: {e}")
                continue

        # TODO: Calculate averages
        # TODO: Store results in all_results list
        pass

    # TODO: Create DataFrame
    # TODO: Print table
    # TODO: Export to CSV

    return all_results

def main():
    """Run benchmarks on all scenarios."""
    scenarios = [
        ("Open Grid", 0.05),
        ("Moderate", 0.20),
        ("Maze", 0.35),
    ]

    # TODO: Run benchmark for each scenario
    for scenario_name, obstacle_density in scenarios:
        run_scenario_benchmark(scenario_name, obstacle_density)

    print("\n" + "="*60)
    print("Benchmark Complete!")
    print("CSV files saved with results for each scenario.")
    print("="*60)

if __name__ == "__main__":
    main()
```

**Expected Output**:
```
============================================================
Scenario: Open Grid
Grid: 20x20, Obstacle Density: 5%
============================================================
                Algorithm  Avg Runtime (ms)  Avg Nodes Visited  Avg Path Length
0                     BFS              2.31                154               28
1                     DFS              4.12                287               42
2                Dijkstra              2.38                157               28
3       Greedy Best-First              0.87                 33               29
4                      A*              0.91                 37               28
5      Bidirectional BFS              1.63                 96               28

CSV saved: benchmark_open_grid.csv

[Similar output for other scenarios...]
```

**Testing**:
1. Verify all 6 algorithms run successfully on each scenario
2. Check that CSV files are created with correct data
3. Compare results across scenarios - observe how obstacle density affects performance
4. Try with different grid sizes (30x30, 40x40) and see how performance scales

---

## Exercise 3: Statistical Analysis and Visualization (Advanced)

**Goal**: Build a complete benchmarking suite with statistical analysis, visualizations, and performance recommendations.

**Task**: Create a professional benchmarking system that:
1. Runs benchmarks with 10 runs per algorithm (for statistical reliability)
2. Calculates mean, median, standard deviation, min, and max for all metrics
3. Creates comparison bar charts for each scenario
4. Generates a comprehensive report with recommendations
5. Handles warm-up runs to avoid cold-start effects
6. Detects and reports statistical significance

**Requirements**:
- Implement warm-up runs (3 runs before collecting data)
- Calculate full statistical measures (mean, median, std dev, min, max)
- Create comparison plots using matplotlib
- Generate textual recommendations based on scenario characteristics
- Export comprehensive results to CSV
- Create a summary report comparing all scenarios

**Starter Code**:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.metrics.benchmark import benchmark_algorithm, run_comparison
from pathfinding_lab.visualization.comparison_plot import create_comparison_plot
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance
# ... import other algorithms

def calculate_statistics(values):
    """Calculate statistical measures for a list of values."""
    # TODO: Calculate mean, median, std dev, min, max
    return {
        'mean': 0.0,
        'median': 0.0,
        'std': 0.0,
        'min': 0.0,
        'max': 0.0,
    }

def run_with_warmup(algo_func, grid, start, goal, warmup_runs=3, data_runs=10, **kwargs):
    """
    Run algorithm with warm-up runs.

    Args:
        algo_func: Algorithm function to run
        grid: Grid to search on
        start: Start position
        goal: Goal position
        warmup_runs: Number of warm-up runs to discard
        data_runs: Number of data runs to collect
        **kwargs: Additional arguments for the algorithm

    Returns:
        Dictionary with runtime and nodes visited statistics
    """
    # TODO: Run warm-up runs (discard results)
    for _ in range(warmup_runs):
        pass

    # TODO: Collect data runs
    runtimes = []
    nodes_visited = []
    for _ in range(data_runs):
        # TODO: Run algorithm and collect metrics
        pass

    # TODO: Calculate statistics
    runtime_stats = calculate_statistics(runtimes)
    nodes_stats = calculate_statistics(nodes_visited)

    return {
        'runtime': runtime_stats,
        'nodes_visited': nodes_stats,
    }

def generate_recommendation(scenario_name, obstacle_density, results_df):
    """
    Generate performance recommendations based on results.

    Args:
        scenario_name: Name of the scenario
        obstacle_density: Obstacle density
        results_df: DataFrame with benchmark results

    Returns:
        String with recommendations
    """
    recommendations = []
    recommendations.append(f"\nRecommendations for {scenario_name}:")
    recommendations.append("-" * 60)

    # TODO: Analyze results and generate recommendations
    # Consider:
    # - Which algorithm has best runtime?
    # - Which finds optimal paths?
    # - Trade-offs between speed and path quality
    # - Scenario-specific advice

    if obstacle_density < 0.1:
        # Open grid recommendations
        pass
    elif obstacle_density > 0.3:
        # Maze recommendations
        pass
    else:
        # Moderate density recommendations
        pass

    return "\n".join(recommendations)

def create_scenario_plot(scenario_name, results_df, save_path=None):
    """
    Create comparison plot for a scenario.

    Args:
        scenario_name: Name of the scenario
        results_df: DataFrame with results
        save_path: Optional path to save figure
    """
    # TODO: Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # TODO: Extract data from results_df
    algorithms = []
    avg_runtimes = []
    avg_nodes = []
    avg_path_lengths = []

    # TODO: Create bar charts
    # Subplot 1: Average runtime
    # Subplot 2: Average nodes visited
    # Subplot 3: Average path length

    # TODO: Format plots (titles, labels, colors)

    plt.suptitle(f"Benchmark Results: {scenario_name}", fontsize=16)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig

def run_comprehensive_benchmark():
    """Run comprehensive benchmark suite with statistical analysis."""
    scenarios = [
        ("Open Grid", 0.05, 20),
        ("Moderate", 0.20, 20),
        ("Maze", 0.35, 20),
        ("Large Open", 0.05, 40),
        ("Large Maze", 0.35, 40),
    ]

    all_scenario_results = []

    for scenario_name, obstacle_density, grid_size in scenarios:
        print(f"\n{'='*70}")
        print(f"Running: {scenario_name} ({grid_size}x{grid_size}, {obstacle_density:.0%} obstacles)")
        print(f"{'='*70}")

        # TODO: Create grid
        # TODO: Define start and goal
        # TODO: Generate obstacles

        # TODO: Run all algorithms with warm-up
        algorithms = [
            ("BFS", bfs, {}),
            ("DFS", dfs, {}),
            ("Dijkstra", dijkstra, {}),
            ("Greedy Best-First", greedy_best_first, {"heuristic": manhattan_distance}),
            ("A*", astar, {"heuristic": manhattan_distance}),
            ("Bidirectional BFS", bidirectional_bfs, {}),
        ]

        scenario_results = []
        for algo_name, algo_func, algo_kwargs in algorithms:
            print(f"  Benchmarking {algo_name}...")
            try:
                # TODO: Run with warm-up
                stats = run_with_warmup(algo_func, grid, start, goal, **algo_kwargs)

                # TODO: Store results
                scenario_results.append({
                    'Scenario': scenario_name,
                    'Algorithm': algo_name,
                    'Mean Runtime (ms)': stats['runtime']['mean'],
                    'Std Runtime (ms)': stats['runtime']['std'],
                    'Mean Nodes': stats['nodes_visited']['mean'],
                    'Std Nodes': stats['nodes_visited']['std'],
                })
            except Exception as e:
                print(f"    Failed: {e}")

        # TODO: Create DataFrame
        results_df = pd.DataFrame(scenario_results)

        # TODO: Display results
        print(f"\n{results_df.to_string(index=False)}")

        # TODO: Generate recommendations
        recommendations = generate_recommendation(scenario_name, obstacle_density, results_df)
        print(recommendations)

        # TODO: Create and save plot
        plot_filename = f"benchmark_{scenario_name.lower().replace(' ', '_')}.png"
        create_scenario_plot(scenario_name, results_df, save_path=plot_filename)
        print(f"\nPlot saved: {plot_filename}")

        # TODO: Export to CSV
        csv_filename = f"benchmark_{scenario_name.lower().replace(' ', '_')}.csv"
        results_df.to_csv(csv_filename, index=False)
        print(f"CSV saved: {csv_filename}")

        all_scenario_results.extend(scenario_results)

    # TODO: Create overall summary
    print(f"\n{'='*70}")
    print("OVERALL SUMMARY")
    print(f"{'='*70}")

    # TODO: Analyze which algorithm performs best across all scenarios
    # TODO: Export combined results
    combined_df = pd.DataFrame(all_scenario_results)
    combined_df.to_csv("benchmark_all_scenarios.csv", index=False)
    print("\nComplete results exported to: benchmark_all_scenarios.csv")

if __name__ == "__main__":
    run_comprehensive_benchmark()
```

**Expected Output**:
```
======================================================================
Running: Open Grid (20x20, 5% obstacles)
======================================================================
  Benchmarking BFS...
  Benchmarking DFS...
  [...]

Scenario      Algorithm          Mean Runtime (ms)  Std Runtime (ms)  Mean Nodes  Std Nodes
Open Grid     BFS                            2.31              0.08         154          2
Open Grid     DFS                            4.15              0.34         289         45
Open Grid     Dijkstra                       2.37              0.07         156          1
Open Grid     Greedy Best-First              0.86              0.04          33          1
Open Grid     A*                             0.90              0.05          37          1
Open Grid     Bidirectional BFS              1.64              0.09          97          3

Recommendations for Open Grid:
------------------------------------------------------------
• A* provides optimal paths (length 28) with excellent performance
• Greedy Best-First is 4% faster but paths are 3% longer
• For applications requiring guaranteed optimality, use A*
• For maximum speed with near-optimal paths, use Greedy Best-First
• Avoid DFS in open grids (explores 7.8x more nodes than A*)

Plot saved: benchmark_open_grid.png
CSV saved: benchmark_open_grid.csv
```

**Testing**:
1. Verify warm-up runs are working (first few runs discarded)
2. Check that statistical measures are calculated correctly
3. Confirm plots are saved as PNG files
4. Verify recommendations make sense for each scenario
5. Test with different numbers of runs (5, 10, 20) and observe standard deviation changes

---

## Exercise 4: Debugging Challenge - Flawed Benchmark

**Goal**: Fix multiple issues in a buggy benchmarking script.

**Background**: A developer created a benchmarking script, but it has several problems that make the results unreliable. Your task is to identify and fix all the bugs.

**Given Code** (with bugs):

```python
import time
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def benchmark_algorithms():
    """Benchmark BFS vs A* - BUGGY VERSION"""

    # Bug 1: Creating different grids for each algorithm
    grid1 = Grid(width=20, height=20, obstacle_density=0.2)
    grid1.generate_obstacles((0, 0), (19, 19))

    grid2 = Grid(width=20, height=20, obstacle_density=0.2)
    grid2.generate_obstacles((0, 0), (19, 19))

    start = (0, 0)
    goal = (19, 19)

    # Bug 2: Single run per algorithm (no statistics)
    print("Running BFS...")
    result_bfs = bfs(grid1, start, goal)

    print("Running A*...")
    result_astar = astar(grid2, start, goal, manhattan_distance)

    # Bug 3: Using wall clock time instead of result.runtime_ms
    start_time = time.time()
    _ = bfs(grid1, start, goal)
    bfs_time = time.time() - start_time

    start_time = time.time()
    _ = astar(grid2, start, goal, manhattan_distance)
    astar_time = time.time() - start_time

    # Bug 4: Comparing times in seconds vs milliseconds
    print(f"\nResults:")
    print(f"BFS:  {bfs_time:.6f} seconds, {result_bfs.nodes_visited} nodes")
    print(f"A*:   {astar_time:.6f} seconds, {result_astar.nodes_visited} nodes")

    # Bug 5: Not checking if paths were found
    print(f"BFS path length: {result_bfs.path_length}")
    print(f"A* path length: {result_astar.path_length}")

    # Bug 6: Integer division losing precision
    speedup = bfs_time // astar_time
    print(f"\nA* is {speedup}x faster")

    # Bug 7: Not handling potential failures
    # What if no path exists?

    # Bug 8: Timing includes print statements and other overhead
    print("Computing speedup...")
    time.sleep(0.1)  # Simulating some work
    efficiency = result_astar.nodes_visited / result_bfs.nodes_visited
    print(f"A* efficiency: {efficiency:.2%}")

if __name__ == "__main__":
    benchmark_algorithms()
```

**Your Task**:
1. Identify all bugs in the code above
2. Explain why each bug makes the benchmark unreliable
3. Fix all bugs and create a corrected version
4. Test the fixed version to ensure it works correctly

**List of Bugs to Find**:
- [ ] Bug 1: Different grids for different algorithms
- [ ] Bug 2: Single run (no statistical reliability)
- [ ] Bug 3: Manual timing instead of using result.runtime_ms
- [ ] Bug 4: Mixing time units (seconds vs milliseconds)
- [ ] Bug 5: Not checking if paths were found
- [ ] Bug 6: Integer division losing precision
- [ ] Bug 7: Not handling algorithm failures
- [ ] Bug 8: Including extraneous operations in timing

**Expected Output** (after fixing):
```
Running benchmark with 10 runs per algorithm...

Results (mean ± std dev):
BFS:  2.34 ± 0.11 ms, 154 ± 2 nodes, path length: 28
A*:   0.91 ± 0.05 ms, 37 ± 1 nodes, path length: 28

A* is 2.57x faster (p < 0.01)
A* visited 76.0% fewer nodes
Both algorithms found optimal paths
```

**Hints**:
- Always use the same grid for comparing algorithms
- Run multiple times and calculate statistics
- Use `result.runtime_ms` for consistent timing
- Keep units consistent (all milliseconds or all seconds)
- Check `result.success` before accessing path metrics
- Use float division (`/`) not integer division (`//`)
- Wrap algorithm calls in try-except blocks
- Don't include print statements or sleeps in timed sections

---

## Bonus Challenge: Performance Profiling

**Goal**: Use Python's profiling tools to identify bottlenecks in pathfinding algorithms.

**Task**: Create a profiling script that:
1. Uses `cProfile` to profile A* execution
2. Identifies which functions consume the most time
3. Analyzes the priority queue operations
4. Suggests optimization opportunities

**Requirements**:
- Profile A* on a 50x50 grid with 25% obstacles
- Generate a profile report showing top 20 time-consuming functions
- Calculate percentage of time spent in different operations:
  - Priority queue operations (push/pop)
  - Heuristic calculations
  - Neighbor generation
  - Path reconstruction
- Suggest specific optimizations based on profiling data

This challenge requires understanding Python's `cProfile` and `pstats` modules!

---

## Submission Checklist

For each exercise, ensure:
- [ ] Code runs without errors
- [ ] All algorithms are tested on each scenario
- [ ] Statistical measures are calculated correctly (when applicable)
- [ ] Results are displayed in a clear, readable format
- [ ] CSV files are exported with correct data
- [ ] Plots are generated and saved (for advanced exercise)
- [ ] Edge cases are handled (failed algorithms, no path found)
- [ ] Code includes helpful comments
- [ ] Testing steps have been completed

---

**See solutions/week_09_solutions.md for answers**
