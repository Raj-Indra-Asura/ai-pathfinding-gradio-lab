# Week 9 Solutions: Benchmarking and Performance Analysis

## Exercise 1 Solution: Basic Algorithm Benchmarking (Beginner)

### Explanation

This solution demonstrates the fundamentals of benchmarking pathfinding algorithms. The key principles are:

1. **Fair Comparison**: Using the exact same grid, start position, and goal position for both algorithms ensures we're comparing apples to apples.
2. **Multiple Runs**: Running each algorithm 5 times and averaging the results reduces the impact of system noise and provides more reliable metrics.
3. **Consistent Metrics**: We collect the same metrics (runtime and nodes visited) for both algorithms from the `SearchResult` object.
4. **Clear Reporting**: Results are displayed in a readable format with comparisons showing how much faster/more efficient one algorithm is.

The solution uses BFS (uninformed) vs A* (informed with Manhattan heuristic) to show how heuristics dramatically improve performance. A* should visit far fewer nodes and run faster because it uses the heuristic to guide the search toward the goal.

### Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def benchmark_simple():
    """Benchmark BFS vs A* on a single grid."""

    # Create a 20x20 grid with 20% obstacle density
    print("Creating grid...")
    grid = Grid(width=20, height=20, obstacle_density=0.2, random_seed=42)

    # Define start and goal positions
    start = (0, 0)
    goal = (19, 19)

    # Generate obstacles (avoiding start and goal)
    grid.generate_obstacles(start, goal)
    print(f"Grid created with {len(grid.obstacles)} obstacles\n")

    # Benchmark BFS: Run 5 times
    print("Running BFS (5 times)...")
    bfs_runtimes = []
    bfs_nodes = []

    for i in range(5):
        result = bfs(grid, start, goal)
        bfs_runtimes.append(result.runtime_ms)
        bfs_nodes.append(result.nodes_visited)
        print(f"  Run {i+1}: {result.runtime_ms:.2f} ms, {result.nodes_visited} nodes")

    # Benchmark A*: Run 5 times
    print("\nRunning A* (5 times)...")
    astar_runtimes = []
    astar_nodes = []

    for i in range(5):
        result = astar(grid, start, goal, manhattan_distance)
        astar_runtimes.append(result.runtime_ms)
        astar_nodes.append(result.nodes_visited)
        print(f"  Run {i+1}: {result.runtime_ms:.2f} ms, {result.nodes_visited} nodes")

    # Calculate averages
    bfs_avg_runtime = sum(bfs_runtimes) / len(bfs_runtimes)
    bfs_avg_nodes = sum(bfs_nodes) / len(bfs_nodes)
    astar_avg_runtime = sum(astar_runtimes) / len(astar_runtimes)
    astar_avg_nodes = sum(astar_nodes) / len(astar_nodes)

    # Print results
    print("\n" + "="*50)
    print("Benchmark Results")
    print("="*50)
    print(f"BFS:")
    print(f"  Average Runtime: {bfs_avg_runtime:.2f} ms")
    print(f"  Average Nodes Visited: {bfs_avg_nodes:.0f}")
    print()
    print(f"A*:")
    print(f"  Average Runtime: {astar_avg_runtime:.2f} ms")
    print(f"  Average Nodes Visited: {astar_avg_nodes:.0f}")
    print()

    # Calculate and display comparison
    runtime_speedup = bfs_avg_runtime / astar_avg_runtime
    nodes_reduction = bfs_avg_nodes / astar_avg_nodes

    print(f"A* is {runtime_speedup:.2f}x faster than BFS")
    print(f"A* visited {nodes_reduction:.2f}x fewer nodes than BFS")

    # Calculate percentage improvements
    runtime_improvement = ((bfs_avg_runtime - astar_avg_runtime) / bfs_avg_runtime) * 100
    nodes_improvement = ((bfs_avg_nodes - astar_avg_nodes) / bfs_avg_nodes) * 100

    print(f"\nPerformance Improvements:")
    print(f"  Runtime: {runtime_improvement:.1f}% faster")
    print(f"  Nodes visited: {nodes_improvement:.1f}% fewer")
    print("="*50)

if __name__ == "__main__":
    benchmark_simple()
```

### Key Concepts

- **Statistical Reliability**: Running multiple times (5 runs) provides more reliable results than a single run. System noise, cache effects, and other factors can cause variation.
- **Fair Comparison**: Using the same grid (with random_seed=42) ensures both algorithms face identical challenges.
- **Metric Collection**: The `SearchResult` object automatically tracks runtime_ms and nodes_visited, making benchmarking straightforward.
- **Performance Ratios**: Reporting relative performance (e.g., "2.5x faster") is more meaningful than absolute times, which vary by hardware.
- **Algorithm Efficiency**: A* uses the Manhattan distance heuristic to prioritize nodes closer to the goal, dramatically reducing exploration.

### Testing Advice

1. **Verify Consistency**: Run the script multiple times. With `random_seed=42`, you should get very similar results each time (within ~10% due to timing variations).

2. **Test Different Grid Sizes**: Modify the grid to 10x10 or 30x30 to see how performance scales:
   ```python
   # Small grid: differences are less pronounced
   grid = Grid(width=10, height=10, obstacle_density=0.2, random_seed=42)

   # Large grid: differences are amplified
   grid = Grid(width=30, height=30, obstacle_density=0.2, random_seed=42)
   ```

3. **Test Different Obstacle Densities**: Try varying obstacle densities to see how they affect performance:
   ```python
   # Open grid: A* excels
   grid = Grid(width=20, height=20, obstacle_density=0.05, random_seed=42)

   # Dense maze: advantage narrows
   grid = Grid(width=20, height=20, obstacle_density=0.35, random_seed=42)
   ```

4. **Verify Path Quality**: Both algorithms should find paths of the same length (they're both optimal on unweighted grids).

5. **Check Edge Cases**: Test with no obstacles (A* should be very fast) and very high obstacles (both may struggle or fail).

---

## Exercise 2 Solution: Multi-Scenario Benchmarking (Intermediate)

### Explanation

This solution creates a comprehensive benchmarking suite that tests all 6 algorithms across 3 different scenarios. The key improvements over Exercise 1:

1. **Multiple Scenarios**: Testing on Open Grid, Moderate, and Maze scenarios reveals how algorithm performance varies with obstacle density.
2. **All Algorithms**: Comparing all 6 algorithms shows the strengths and weaknesses of uninformed (BFS, DFS, Dijkstra), informed (Greedy, A*), and bidirectional (Bidirectional BFS) approaches.
3. **Structured Data**: Using pandas DataFrame makes it easy to view, analyze, and export results.
4. **Error Handling**: Gracefully handles algorithm failures (e.g., DFS might timeout or fail on some grids).
5. **CSV Export**: Saving results to CSV files allows further analysis in Excel, Python, or other tools.

The solution demonstrates that algorithm performance is highly scenario-dependent: A* excels on open grids, BFS is reliable on mazes, and DFS can be unpredictable.

### Code

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

def run_scenario_benchmark(scenario_name, obstacle_density, grid_size=20):
    """
    Benchmark all algorithms on a single scenario.

    Args:
        scenario_name: Name of the scenario
        obstacle_density: Obstacle density (0.0 to 1.0)
        grid_size: Size of the square grid

    Returns:
        List of result dictionaries
    """
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario_name}")
    print(f"Grid: {grid_size}x{grid_size}, Obstacle Density: {obstacle_density:.0%}")
    print(f"{'='*60}")

    # Create grid with fixed random seed for reproducibility
    grid = Grid(
        width=grid_size,
        height=grid_size,
        obstacle_density=obstacle_density,
        random_seed=42
    )

    # Define start and goal
    start = (0, 0)
    goal = (grid_size - 1, grid_size - 1)

    # Generate obstacles
    grid.generate_obstacles(start, goal)
    print(f"Generated {len(grid.obstacles)} obstacles")

    # Define all algorithms with their parameters
    algorithms = [
        ("BFS", bfs, {}),
        ("DFS", dfs, {}),
        ("Dijkstra", dijkstra, {}),
        ("Greedy Best-First", greedy_best_first, {"heuristic": manhattan_distance}),
        ("A*", astar, {"heuristic": manhattan_distance}),
        ("Bidirectional BFS", bidirectional_bfs, {}),
    ]

    # Run each algorithm 3 times and collect statistics
    all_results = []

    for algo_name, algo_func, algo_kwargs in algorithms:
        print(f"\nTesting {algo_name}...")

        runtimes = []
        nodes_visited_list = []
        path_lengths = []
        path_costs = []
        success_count = 0

        for run in range(3):
            try:
                # Run the algorithm
                result = algo_func(grid, start, goal, **algo_kwargs)

                # Collect metrics
                runtimes.append(result.runtime_ms)
                nodes_visited_list.append(result.nodes_visited)

                if result.success:
                    path_lengths.append(result.path_length)
                    path_costs.append(result.path_cost)
                    success_count += 1

                print(f"  Run {run+1}: {result.runtime_ms:.2f} ms, "
                      f"{result.nodes_visited} nodes, "
                      f"{'path: ' + str(result.path_length) if result.success else 'NO PATH'}")

            except Exception as e:
                print(f"  Run {run+1}: FAILED - {e}")
                # For failed runs, we don't add to statistics

        # Calculate averages (only if we have successful runs)
        if runtimes:
            avg_runtime = sum(runtimes) / len(runtimes)
            avg_nodes = sum(nodes_visited_list) / len(nodes_visited_list)
            avg_path_length = sum(path_lengths) / len(path_lengths) if path_lengths else 0
            avg_path_cost = sum(path_costs) / len(path_costs) if path_costs else 0

            # Store results
            all_results.append({
                'Algorithm': algo_name,
                'Avg Runtime (ms)': f"{avg_runtime:.2f}",
                'Avg Nodes Visited': f"{avg_nodes:.0f}",
                'Avg Path Length': f"{avg_path_length:.0f}" if avg_path_length > 0 else "N/A",
                'Avg Path Cost': f"{avg_path_cost:.2f}" if avg_path_cost > 0 else "N/A",
                'Success Rate': f"{success_count}/3"
            })
        else:
            # Algorithm failed all runs
            all_results.append({
                'Algorithm': algo_name,
                'Avg Runtime (ms)': "FAILED",
                'Avg Nodes Visited': "FAILED",
                'Avg Path Length': "FAILED",
                'Avg Path Cost': "FAILED",
                'Success Rate': "0/3"
            })

    # Create DataFrame for easy viewing
    results_df = pd.DataFrame(all_results)

    # Print table
    print(f"\n{'='*60}")
    print("Results Summary:")
    print(f"{'='*60}")
    print(results_df.to_string(index=False))

    # Export to CSV
    csv_filename = f"benchmark_{scenario_name.lower().replace(' ', '_')}.csv"
    results_df.to_csv(csv_filename, index=False)
    print(f"\nCSV saved: {csv_filename}")

    return all_results

def main():
    """Run benchmarks on all scenarios."""
    print("="*60)
    print("Multi-Scenario Algorithm Benchmarking Suite")
    print("="*60)
    print("\nThis will test all 6 algorithms on 3 different scenarios:")
    print("  1. Open Grid (5% obstacles) - Best for A* and Greedy")
    print("  2. Moderate (20% obstacles) - Balanced scenario")
    print("  3. Maze (35% obstacles) - Best for BFS and Bidirectional")

    scenarios = [
        ("Open Grid", 0.05),
        ("Moderate", 0.20),
        ("Maze", 0.35),
    ]

    all_scenario_results = []

    # Run benchmark for each scenario
    for scenario_name, obstacle_density in scenarios:
        results = run_scenario_benchmark(scenario_name, obstacle_density)
        all_scenario_results.extend(results)

    print("\n" + "="*60)
    print("Benchmark Complete!")
    print("="*60)
    print("\nKey Findings:")
    print("  • Open Grid: A* and Greedy Best-First excel with heuristic guidance")
    print("  • Moderate: A* provides best balance of speed and optimality")
    print("  • Maze: BFS and Bidirectional BFS are most reliable")
    print("  • DFS: Unpredictable performance, may explore unnecessarily")
    print("\nCSV files saved:")
    for scenario_name, _ in scenarios:
        csv_name = f"benchmark_{scenario_name.lower().replace(' ', '_')}.csv"
        print(f"  • {csv_name}")
    print("="*60)

if __name__ == "__main__":
    main()
```

### Key Concepts

- **Scenario-Based Testing**: Different grid characteristics (obstacle density) significantly affect which algorithms perform best.
- **Comprehensive Coverage**: Testing all 6 algorithms reveals the trade-offs between uninformed, informed, and bidirectional search.
- **Statistical Reliability**: Running 3 times per algorithm reduces random variation while keeping runtime reasonable.
- **Structured Data with Pandas**: DataFrames make it easy to view, sort, filter, and export results.
- **Error Handling**: Try-except blocks ensure one algorithm's failure doesn't crash the entire benchmark.
- **CSV Export**: Saving results allows further analysis, plotting, or comparison across multiple runs.
- **Success Rate Tracking**: Recording how many runs succeeded reveals algorithm reliability.

### Testing Advice

1. **Verify All Algorithms Run**: Check that all 6 algorithms complete successfully on at least the Open Grid and Moderate scenarios.

2. **Compare Across Scenarios**: Look at the CSV files and observe:
   ```
   Open Grid: A* should be fastest with fewest nodes
   Moderate: A* still leads but margin narrows
   Maze: BFS/Bidirectional become competitive
   ```

3. **Test DFS Behavior**: DFS is often unpredictable. You might see:
   - Very fast if it happens to go in the right direction
   - Very slow if it explores wrong paths first
   - May fail or timeout on complex grids

4. **Verify Path Optimality**: Check that BFS, Dijkstra, and A* all find paths of the same length (they're all optimal on unweighted grids). Greedy may find slightly longer paths.

5. **Test Error Handling**: Intentionally create an impossible scenario (start or goal inside obstacles) and verify the benchmark handles it gracefully.

6. **Scale Testing**: Try larger grids (30x30 or 40x40) to see how performance differences amplify:
   ```python
   run_scenario_benchmark("Large Open", 0.05, grid_size=40)
   ```

---

## Exercise 3 Solution: Statistical Analysis and Visualization (Advanced)

### Explanation

This solution creates a production-quality benchmarking suite with comprehensive statistical analysis and visualizations. Key features:

1. **Warm-up Runs**: The first few runs are often slower due to JIT compilation, cache warming, etc. We run 3 warm-up iterations and discard them before collecting real data.

2. **Comprehensive Statistics**: Beyond simple averages, we calculate:
   - Mean: Central tendency
   - Median: Middle value, less affected by outliers
   - Standard Deviation: Measure of variability
   - Min/Max: Range of performance

3. **Visualization**: Bar charts comparing algorithms on three key metrics (runtime, nodes visited, path length) make results immediately understandable.

4. **Intelligent Recommendations**: The system analyzes grid characteristics and results to suggest the best algorithm for each scenario.

5. **Multiple Scenarios**: Testing 5 different scenarios (including large grids) reveals how algorithms scale.

The solution demonstrates professional benchmarking practices used in research and industry.

### Code

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dfs import dfs
from pathfinding_lab.algorithms.dijkstra import dijkstra
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.greedy_best_first import greedy_best_first
from pathfinding_lab.algorithms.bidirectional_bfs import bidirectional_bfs
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def calculate_statistics(values):
    """
    Calculate statistical measures for a list of values.

    Args:
        values: List of numeric values

    Returns:
        Dictionary with statistical measures
    """
    if not values:
        return {
            'mean': 0.0,
            'median': 0.0,
            'std': 0.0,
            'min': 0.0,
            'max': 0.0,
        }

    values_array = np.array(values)

    return {
        'mean': float(np.mean(values_array)),
        'median': float(np.median(values_array)),
        'std': float(np.std(values_array)),
        'min': float(np.min(values_array)),
        'max': float(np.max(values_array)),
    }

def run_with_warmup(algo_func, grid, start, goal, warmup_runs=3, data_runs=10, **kwargs):
    """
    Run algorithm with warm-up runs to avoid cold-start effects.

    Args:
        algo_func: Algorithm function to run
        grid: Grid to search on
        start: Start position
        goal: Goal position
        warmup_runs: Number of warm-up runs to discard
        data_runs: Number of data runs to collect
        **kwargs: Additional arguments for the algorithm

    Returns:
        Dictionary with runtime and nodes visited statistics, plus a sample result
    """
    # Warm-up runs (discard results)
    for _ in range(warmup_runs):
        try:
            _ = algo_func(grid, start, goal, **kwargs)
        except Exception:
            pass  # Ignore warm-up failures

    # Collect data runs
    runtimes = []
    nodes_visited = []
    path_lengths = []
    path_costs = []
    sample_result = None
    success_count = 0

    for _ in range(data_runs):
        try:
            result = algo_func(grid, start, goal, **kwargs)

            # Store first successful result as sample
            if sample_result is None and result.success:
                sample_result = result

            # Collect metrics
            runtimes.append(result.runtime_ms)
            nodes_visited.append(result.nodes_visited)

            if result.success:
                path_lengths.append(result.path_length)
                path_costs.append(result.path_cost)
                success_count += 1

        except Exception as e:
            print(f"    Run failed: {e}")
            continue

    # Calculate statistics
    runtime_stats = calculate_statistics(runtimes)
    nodes_stats = calculate_statistics(nodes_visited)
    path_length_stats = calculate_statistics(path_lengths)
    path_cost_stats = calculate_statistics(path_costs)

    return {
        'runtime': runtime_stats,
        'nodes_visited': nodes_stats,
        'path_length': path_length_stats,
        'path_cost': path_cost_stats,
        'success_count': success_count,
        'total_runs': data_runs,
        'sample_result': sample_result
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
    recommendations.append(f"\n{'='*70}")
    recommendations.append(f"Recommendations for {scenario_name}")
    recommendations.append(f"{'='*70}")

    # Find best performers
    # Convert string values to float for comparison (filter out "N/A")
    runtime_data = []
    for idx, row in results_df.iterrows():
        try:
            runtime = float(row['Mean Runtime (ms)'])
            runtime_data.append((row['Algorithm'], runtime))
        except (ValueError, TypeError):
            pass

    if runtime_data:
        fastest = min(runtime_data, key=lambda x: x[1])
        recommendations.append(f"\nFastest Algorithm: {fastest[0]} ({fastest[1]:.2f} ms)")

    # Scenario-specific advice
    if obstacle_density < 0.1:
        recommendations.append("\nOpen Grid Scenario:")
        recommendations.append("• A* with Manhattan heuristic is recommended for optimal paths with excellent speed")
        recommendations.append("• Greedy Best-First is fastest but may find suboptimal paths")
        recommendations.append("• Bidirectional BFS is a good choice when heuristics are unavailable")
        recommendations.append("• Avoid DFS on open grids (explores unnecessarily)")

    elif obstacle_density > 0.3:
        recommendations.append("\nMaze Scenario (High Obstacle Density):")
        recommendations.append("• BFS is most reliable - guarantees shortest path")
        recommendations.append("• Bidirectional BFS is often fastest by meeting in the middle")
        recommendations.append("• A* advantage is reduced in mazes (heuristic less helpful)")
        recommendations.append("• Dijkstra is reliable when consistent performance is critical")

    else:
        recommendations.append("\nModerate Scenario (Balanced):")
        recommendations.append("• A* provides best balance of speed and optimality")
        recommendations.append("• Dijkstra is a safe choice when heuristics are uncertain")
        recommendations.append("• Greedy Best-First for speed-critical applications")
        recommendations.append("• BFS for guaranteed shortest path without heuristics")

    # General insights
    recommendations.append("\nGeneral Insights:")
    recommendations.append("• All optimal algorithms (BFS, Dijkstra, A*) should find paths of equal length")
    recommendations.append("• Greedy Best-First trades optimality for speed")
    recommendations.append("• DFS is unpredictable and generally not recommended for pathfinding")
    recommendations.append("• Lower standard deviation indicates more consistent performance")

    return "\n".join(recommendations)

def create_scenario_plot(scenario_name, results_df, save_path=None):
    """
    Create comparison plot for a scenario.

    Args:
        scenario_name: Name of the scenario
        results_df: DataFrame with results
        save_path: Optional path to save figure

    Returns:
        matplotlib Figure object
    """
    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Extract data from results_df
    algorithms = results_df['Algorithm'].tolist()

    # Parse numeric values (handle "N/A" and "FAILED")
    avg_runtimes = []
    avg_nodes = []
    avg_path_lengths = []

    for idx, row in results_df.iterrows():
        try:
            avg_runtimes.append(float(row['Mean Runtime (ms)']))
        except (ValueError, TypeError):
            avg_runtimes.append(0)

        try:
            avg_nodes.append(float(row['Mean Nodes']))
        except (ValueError, TypeError):
            avg_nodes.append(0)

        try:
            avg_path_lengths.append(float(row['Mean Path Length']))
        except (ValueError, TypeError):
            avg_path_lengths.append(0)

    # Define colors for each algorithm
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']

    # Subplot 1: Average Runtime
    bars1 = axes[0].bar(range(len(algorithms)), avg_runtimes, color=colors)
    axes[0].set_xlabel('Algorithm', fontsize=10)
    axes[0].set_ylabel('Mean Runtime (ms)', fontsize=10)
    axes[0].set_title('Runtime Comparison', fontsize=12, fontweight='bold')
    axes[0].set_xticks(range(len(algorithms)))
    axes[0].set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
    axes[0].grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        if height > 0:
            axes[0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}',
                        ha='center', va='bottom', fontsize=8)

    # Subplot 2: Average Nodes Visited
    bars2 = axes[1].bar(range(len(algorithms)), avg_nodes, color=colors)
    axes[1].set_xlabel('Algorithm', fontsize=10)
    axes[1].set_ylabel('Mean Nodes Visited', fontsize=10)
    axes[1].set_title('Search Efficiency', fontsize=12, fontweight='bold')
    axes[1].set_xticks(range(len(algorithms)))
    axes[1].set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
    axes[1].grid(axis='y', alpha=0.3)

    for bar in bars2:
        height = bar.get_height()
        if height > 0:
            axes[1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=8)

    # Subplot 3: Average Path Length
    bars3 = axes[2].bar(range(len(algorithms)), avg_path_lengths, color=colors)
    axes[2].set_xlabel('Algorithm', fontsize=10)
    axes[2].set_ylabel('Mean Path Length', fontsize=10)
    axes[2].set_title('Solution Quality', fontsize=12, fontweight='bold')
    axes[2].set_xticks(range(len(algorithms)))
    axes[2].set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
    axes[2].grid(axis='y', alpha=0.3)

    for bar in bars3:
        height = bar.get_height()
        if height > 0:
            axes[2].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=8)

    # Overall title
    plt.suptitle(f'Benchmark Results: {scenario_name}', fontsize=16, fontweight='bold')
    plt.tight_layout()

    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  Plot saved: {save_path}")

    return fig

def run_comprehensive_benchmark():
    """Run comprehensive benchmark suite with statistical analysis."""

    print("="*70)
    print("COMPREHENSIVE PATHFINDING BENCHMARK SUITE")
    print("="*70)
    print("\nConfiguration:")
    print("  • Warm-up runs: 3 (discarded)")
    print("  • Data runs: 10 (for statistics)")
    print("  • Scenarios: 5 (varying sizes and densities)")
    print("  • Algorithms: 6 (all major pathfinding algorithms)")
    print("="*70)

    # Define scenarios
    scenarios = [
        ("Open Grid", 0.05, 20),
        ("Moderate", 0.20, 20),
        ("Maze", 0.35, 20),
        ("Large Open", 0.05, 40),
        ("Large Maze", 0.35, 40),
    ]

    # Create output directory for results
    os.makedirs("benchmark_results", exist_ok=True)

    all_scenario_results = []

    for scenario_name, obstacle_density, grid_size in scenarios:
        print(f"\n{'='*70}")
        print(f"Running: {scenario_name}")
        print(f"Grid: {grid_size}x{grid_size}, Obstacle Density: {obstacle_density:.0%}")
        print(f"{'='*70}")

        # Create grid
        grid = Grid(
            width=grid_size,
            height=grid_size,
            obstacle_density=obstacle_density,
            random_seed=42
        )

        # Define start and goal
        start = (0, 0)
        goal = (grid_size - 1, grid_size - 1)

        # Generate obstacles
        grid.generate_obstacles(start, goal)
        print(f"Generated {len(grid.obstacles)} obstacles\n")

        # Define all algorithms
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
            print(f"Benchmarking {algo_name}...")

            try:
                # Run with warm-up
                stats = run_with_warmup(
                    algo_func, grid, start, goal,
                    warmup_runs=3,
                    data_runs=10,
                    **algo_kwargs
                )

                # Store results
                scenario_results.append({
                    'Scenario': scenario_name,
                    'Algorithm': algo_name,
                    'Mean Runtime (ms)': f"{stats['runtime']['mean']:.3f}",
                    'Std Runtime (ms)': f"{stats['runtime']['std']:.3f}",
                    'Mean Nodes': f"{stats['nodes_visited']['mean']:.1f}",
                    'Std Nodes': f"{stats['nodes_visited']['std']:.1f}",
                    'Mean Path Length': f"{stats['path_length']['mean']:.1f}" if stats['path_length']['mean'] > 0 else "N/A",
                    'Success Rate': f"{stats['success_count']}/{stats['total_runs']}"
                })

                print(f"  ✓ Complete - Runtime: {stats['runtime']['mean']:.2f} ± {stats['runtime']['std']:.2f} ms")

            except Exception as e:
                print(f"  ✗ Failed: {e}")
                scenario_results.append({
                    'Scenario': scenario_name,
                    'Algorithm': algo_name,
                    'Mean Runtime (ms)': "FAILED",
                    'Std Runtime (ms)': "N/A",
                    'Mean Nodes': "N/A",
                    'Std Nodes': "N/A",
                    'Mean Path Length': "N/A",
                    'Success Rate': "0/10"
                })

        # Create DataFrame
        results_df = pd.DataFrame(scenario_results)

        # Display results
        print(f"\n{'-'*70}")
        print("Results:")
        print(f"{'-'*70}")
        print(results_df.to_string(index=False))

        # Generate recommendations
        recommendations = generate_recommendation(scenario_name, obstacle_density, results_df)
        print(recommendations)

        # Create and save plot
        plot_filename = f"benchmark_results/plot_{scenario_name.lower().replace(' ', '_')}.png"
        fig = create_scenario_plot(scenario_name, results_df, save_path=plot_filename)
        plt.close(fig)  # Close to free memory

        # Export to CSV
        csv_filename = f"benchmark_results/data_{scenario_name.lower().replace(' ', '_')}.csv"
        results_df.to_csv(csv_filename, index=False)
        print(f"  CSV saved: {csv_filename}")

        all_scenario_results.extend(scenario_results)

    # Create overall summary
    print(f"\n{'='*70}")
    print("OVERALL SUMMARY")
    print(f"{'='*70}")

    # Export combined results
    combined_df = pd.DataFrame(all_scenario_results)
    combined_filename = "benchmark_results/all_scenarios_combined.csv"
    combined_df.to_csv(combined_filename, index=False)

    print("\nAll benchmarks completed successfully!")
    print(f"\nResults saved to: benchmark_results/")
    print(f"  • Combined data: {combined_filename}")
    print(f"  • Individual CSV files: data_*.csv")
    print(f"  • Visualization plots: plot_*.png")

    print("\n" + "="*70)
    print("KEY TAKEAWAYS")
    print("="*70)
    print("1. A* consistently provides best balance of speed and optimality")
    print("2. Bidirectional BFS excels on large grids and mazes")
    print("3. Greedy Best-First is fastest but sacrifices path optimality")
    print("4. DFS is unpredictable and generally not recommended")
    print("5. BFS and Dijkstra are reliable when heuristics are unavailable")
    print("="*70)

if __name__ == "__main__":
    run_comprehensive_benchmark()
```

### Key Concepts

- **Warm-up Runs**: Critical for accurate benchmarking. The first few runs are often slower due to JIT compilation, cache effects, and dynamic optimizations. Discarding warm-up runs gives more reliable measurements.

- **Comprehensive Statistics**: Beyond averages, we calculate:
  - **Standard Deviation**: Shows consistency. Low std dev means predictable performance.
  - **Median**: Less affected by outliers than mean.
  - **Min/Max**: Shows best and worst case performance.

- **Professional Visualization**: Three-subplot bar charts make comparisons immediately clear. Color coding and value labels enhance readability.

- **Intelligent Recommendations**: Analyzing grid characteristics (obstacle density, size) and results to provide actionable advice.

- **File Organization**: Creating a dedicated `benchmark_results/` directory keeps outputs organized.

- **Multiple Scenarios**: Testing on both small (20x20) and large (40x40) grids reveals how algorithms scale.

### Testing Advice

1. **Verify Warm-up Works**: Add debug prints to see that warm-up runs are actually being discarded:
   ```python
   print(f"  Warm-up run {i+1} complete")  # During warm-up
   print(f"  Data run {i+1} complete")     # During data collection
   ```

2. **Check Statistical Validity**: Standard deviation should be relatively small (< 10% of mean) for runtime. If it's high, increase the number of data runs.

3. **Verify Plots**: Open the generated PNG files and check:
   - All 6 algorithms appear
   - Bar heights match the DataFrame values
   - Labels are readable
   - Colors distinguish algorithms

4. **Test Recommendations**: Read the recommendations for each scenario and verify they make sense:
   - Open Grid: Should recommend A* or Greedy
   - Maze: Should recommend BFS or Bidirectional
   - Large grids: Should warn about scalability

5. **CSV Export Verification**: Open CSV files in Excel or a text editor to verify:
   - All columns are present
   - Values are properly formatted
   - No missing or corrupted data

6. **Performance Scaling**: Compare the 20x20 and 40x40 results:
   - Runtime should increase significantly (roughly 4x or more)
   - Nodes visited should increase (depends on algorithm)
   - A* advantage should be more pronounced on larger grids

7. **Edge Case Testing**: Try scenarios with very high obstacle density (0.45) to see if any algorithms fail to find paths.

---

## Exercise 4 Solution: Debugging Challenge - Flawed Benchmark

### Bugs Found and Fixes

#### Bug 1: Creating Different Grids for Each Algorithm

**Problem**: Each time `Grid` is created, it generates different random obstacles (even with the same density). This means BFS and A* are solving different problems, making comparison meaningless.

```python
# BUGGY CODE
grid1 = Grid(width=20, height=20, obstacle_density=0.2)
grid1.generate_obstacles((0, 0), (19, 19))

grid2 = Grid(width=20, height=20, obstacle_density=0.2)
grid2.generate_obstacles((0, 0), (19, 19))
```

**Why it's a problem**: Fair comparison requires identical inputs. Different obstacle layouts mean one algorithm might get an easier or harder problem.

**Fix**: Create one grid and use it for both algorithms. Set a random seed for reproducibility.

```python
# FIXED CODE
grid = Grid(width=20, height=20, obstacle_density=0.2, random_seed=42)
grid.generate_obstacles((0, 0), (19, 19))
# Use same grid for both algorithms
```

#### Bug 2: Single Run Per Algorithm (No Statistics)

**Problem**: Running each algorithm only once gives unreliable results. System noise, cache effects, and other factors cause variation.

```python
# BUGGY CODE
result_bfs = bfs(grid, start, goal)  # Only once!
result_astar = astar(grid, start, goal, manhattan_distance)  # Only once!
```

**Why it's a problem**: A single measurement can be misleading. One algorithm might get lucky (or unlucky) with timing.

**Fix**: Run multiple times (at least 5-10) and calculate statistics.

```python
# FIXED CODE
bfs_runtimes = []
bfs_nodes = []
for _ in range(10):
    result = bfs(grid, start, goal)
    bfs_runtimes.append(result.runtime_ms)
    bfs_nodes.append(result.nodes_visited)

avg_bfs_runtime = sum(bfs_runtimes) / len(bfs_runtimes)
std_bfs_runtime = np.std(bfs_runtimes)
```

#### Bug 3: Using Wall Clock Time Instead of result.runtime_ms

**Problem**: Manually timing with `time.time()` includes overhead from Python interpreter, print statements, and other code.

```python
# BUGGY CODE
start_time = time.time()
_ = bfs(grid1, start, goal)
bfs_time = time.time() - start_time
```

**Why it's a problem**: The measurement includes more than just the algorithm execution. Plus, `SearchResult` already provides accurate timing!

**Fix**: Use the `runtime_ms` field from `SearchResult`, which measures only the algorithm execution.

```python
# FIXED CODE
result = bfs(grid, start, goal)
bfs_time = result.runtime_ms  # Already measured internally
```

#### Bug 4: Mixing Time Units (Seconds vs Milliseconds)

**Problem**: `time.time()` returns seconds, but `result.runtime_ms` is milliseconds. Comparing them directly gives wrong results.

```python
# BUGGY CODE
bfs_time = time.time() - start_time  # seconds
print(f"BFS: {bfs_time:.6f} seconds")  # seconds
# Later comparing with milliseconds!
```

**Why it's a problem**: Mixing units leads to incorrect speedup calculations. 0.002 seconds = 2 milliseconds, not 0.002 milliseconds!

**Fix**: Use consistent units (milliseconds) throughout.

```python
# FIXED CODE
print(f"BFS: {result.runtime_ms:.2f} ms")  # Always milliseconds
```

#### Bug 5: Not Checking if Paths Were Found

**Problem**: Accessing `path_length` without checking `success` causes crashes or incorrect results if no path exists.

```python
# BUGGY CODE
print(f"BFS path length: {result_bfs.path_length}")  # What if no path?
```

**Why it's a problem**: If the algorithm fails to find a path, `path_length` will be 0, which is misleading. Or worse, the code might crash.

**Fix**: Always check `result.success` before accessing path-related fields.

```python
# FIXED CODE
if result.success:
    print(f"BFS path length: {result.path_length}")
else:
    print(f"BFS: No path found")
```

#### Bug 6: Integer Division Losing Precision

**Problem**: Using `//` (integer division) instead of `/` (float division) loses precision.

```python
# BUGGY CODE
speedup = bfs_time // astar_time  # Integer division!
print(f"A* is {speedup}x faster")
```

**Why it's a problem**: If BFS takes 2.5 ms and A* takes 1.0 ms, the speedup is 2.5x. But integer division gives 2x, which is inaccurate.

**Fix**: Use float division.

```python
# FIXED CODE
speedup = bfs_time / astar_time  # Float division
print(f"A* is {speedup:.2f}x faster")
```

#### Bug 7: Not Handling Algorithm Failures

**Problem**: No try-except blocks. If an algorithm fails, the entire script crashes.

**Why it's a problem**: Some algorithms (especially DFS) can fail on certain grids. A robust benchmark should handle this gracefully.

**Fix**: Wrap algorithm calls in try-except blocks.

```python
# FIXED CODE
try:
    result = bfs(grid, start, goal)
    bfs_runtimes.append(result.runtime_ms)
except Exception as e:
    print(f"BFS failed: {e}")
    # Handle failure appropriately
```

#### Bug 8: Including Extraneous Operations in Timing

**Problem**: Print statements and sleep calls are included in the timing measurement.

```python
# BUGGY CODE
start_time = time.time()
_ = bfs(grid1, start, goal)
bfs_time = time.time() - start_time

print("Computing speedup...")  # After timing, but...
time.sleep(0.1)  # ...this affects subsequent measurements!
```

**Why it's a problem**: Benchmarks should measure only the algorithm execution, not print statements, file I/O, or other operations.

**Fix**: Use `result.runtime_ms` which only measures the algorithm, or ensure timing excludes extraneous operations.

### Corrected Code

```python
import numpy as np
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def benchmark_algorithms():
    """
    Benchmark BFS vs A* - CORRECTED VERSION

    This version fixes all 8 bugs from the original implementation:
    1. Uses single grid for fair comparison
    2. Runs multiple times for statistical reliability
    3. Uses result.runtime_ms instead of manual timing
    4. Keeps units consistent (all milliseconds)
    5. Checks if paths were found
    6. Uses float division for accurate speedup
    7. Handles algorithm failures gracefully
    8. Excludes print statements from timing
    """

    print("="*60)
    print("CORRECTED BENCHMARK: BFS vs A*")
    print("="*60)

    # FIX 1: Create ONE grid with fixed seed for reproducibility
    print("\nCreating grid...")
    grid = Grid(width=20, height=20, obstacle_density=0.2, random_seed=42)
    start = (0, 0)
    goal = (19, 19)
    grid.generate_obstacles(start, goal)
    print(f"Grid created with {len(grid.obstacles)} obstacles")

    num_runs = 10
    print(f"\nRunning benchmark with {num_runs} runs per algorithm...")

    # FIX 2: Multiple runs for statistical reliability
    # FIX 3: Use result.runtime_ms instead of manual timing
    # FIX 7: Handle failures with try-except

    bfs_runtimes = []
    bfs_nodes = []
    bfs_path_lengths = []
    bfs_success_count = 0

    print("\nRunning BFS...")
    for i in range(num_runs):
        try:
            result = bfs(grid, start, goal)

            # FIX 3: Use result.runtime_ms (already properly timed internally)
            bfs_runtimes.append(result.runtime_ms)
            bfs_nodes.append(result.nodes_visited)

            # FIX 5: Check if path was found before accessing path_length
            if result.success:
                bfs_path_lengths.append(result.path_length)
                bfs_success_count += 1

            print(f"  Run {i+1}: {result.runtime_ms:.2f} ms, "
                  f"{result.nodes_visited} nodes, "
                  f"{'path: ' + str(result.path_length) if result.success else 'NO PATH'}")

        except Exception as e:
            print(f"  Run {i+1}: FAILED - {e}")

    astar_runtimes = []
    astar_nodes = []
    astar_path_lengths = []
    astar_success_count = 0

    print("\nRunning A*...")
    for i in range(num_runs):
        try:
            result = astar(grid, start, goal, manhattan_distance)

            astar_runtimes.append(result.runtime_ms)
            astar_nodes.append(result.nodes_visited)

            if result.success:
                astar_path_lengths.append(result.path_length)
                astar_success_count += 1

            print(f"  Run {i+1}: {result.runtime_ms:.2f} ms, "
                  f"{result.nodes_visited} nodes, "
                  f"{'path: ' + str(result.path_length) if result.success else 'NO PATH'}")

        except Exception as e:
            print(f"  Run {i+1}: FAILED - {e}")

    # FIX 8: All extraneous operations (prints, sleeps) are outside of timing

    # Calculate statistics
    if bfs_runtimes and astar_runtimes:
        bfs_mean = np.mean(bfs_runtimes)
        bfs_std = np.std(bfs_runtimes)
        astar_mean = np.mean(astar_runtimes)
        astar_std = np.std(astar_runtimes)

        bfs_nodes_mean = np.mean(bfs_nodes)
        bfs_nodes_std = np.std(bfs_nodes)
        astar_nodes_mean = np.mean(astar_nodes)
        astar_nodes_std = np.std(astar_nodes)

        # FIX 4: Keep units consistent (all milliseconds)
        print(f"\n{'='*60}")
        print("Results (mean ± std dev):")
        print(f"{'='*60}")
        print(f"BFS:  {bfs_mean:.2f} ± {bfs_std:.2f} ms, "
              f"{bfs_nodes_mean:.0f} ± {bfs_nodes_std:.0f} nodes, "
              f"path length: {np.mean(bfs_path_lengths):.0f}" if bfs_path_lengths else "NO PATH")

        print(f"A*:   {astar_mean:.2f} ± {astar_std:.2f} ms, "
              f"{astar_nodes_mean:.0f} ± {astar_nodes_std:.0f} nodes, "
              f"path length: {np.mean(astar_path_lengths):.0f}" if astar_path_lengths else "NO PATH")

        # FIX 6: Use float division for accurate speedup
        if astar_mean > 0:
            speedup = bfs_mean / astar_mean
            print(f"\nA* is {speedup:.2f}x faster")

            # Calculate statistical significance (simple t-test)
            # If standard deviations don't overlap, difference is likely significant
            if abs(bfs_mean - astar_mean) > (bfs_std + astar_std):
                print("(Statistically significant difference)")
            else:
                print("(Difference may not be statistically significant)")

        if bfs_nodes_mean > 0:
            efficiency = ((bfs_nodes_mean - astar_nodes_mean) / bfs_nodes_mean) * 100
            print(f"A* visited {efficiency:.1f}% fewer nodes")

        # Path quality comparison
        if bfs_path_lengths and astar_path_lengths:
            bfs_avg_path = np.mean(bfs_path_lengths)
            astar_avg_path = np.mean(astar_path_lengths)

            if abs(bfs_avg_path - astar_avg_path) < 0.1:
                print("Both algorithms found optimal paths")
            else:
                print(f"Path quality differs: BFS={bfs_avg_path:.1f}, A*={astar_avg_path:.1f}")

        print(f"\nSuccess rates:")
        print(f"  BFS: {bfs_success_count}/{num_runs}")
        print(f"  A*: {astar_success_count}/{num_runs}")

        print("="*60)

    else:
        print("\n✗ Insufficient data for comparison (both algorithms failed)")

if __name__ == "__main__":
    benchmark_algorithms()
```

### What You Should Understand

**Key Learning Outcomes**:

1. **Fair Comparison Principles**:
   - Use identical inputs for all algorithms
   - Set random seeds for reproducibility
   - Keep environment consistent

2. **Statistical Reliability**:
   - Single measurements are unreliable due to system noise
   - Multiple runs (10+) provide statistical validity
   - Report mean ± standard deviation
   - Check if differences are statistically significant

3. **Measurement Accuracy**:
   - Use built-in timing mechanisms (`result.runtime_ms`) when available
   - Avoid including extraneous operations in measurements
   - Be aware of measurement overhead for fast operations

4. **Unit Consistency**:
   - Keep all measurements in the same units
   - Document units clearly (milliseconds vs seconds)
   - Convert units consistently when necessary

5. **Robust Error Handling**:
   - Always check `result.success` before accessing path data
   - Use try-except for algorithm execution
   - Handle failures gracefully without crashing
   - Report success rates

6. **Precision in Calculations**:
   - Use float division (`/`) not integer division (`//`)
   - Format output appropriately (e.g., `:.2f` for 2 decimal places)
   - Be careful with percentage calculations

7. **Common Benchmarking Pitfalls**:
   - **Different inputs**: Comparing algorithms on different data
   - **Single runs**: Trusting one measurement
   - **Mixed units**: Comparing seconds to milliseconds
   - **Ignoring failures**: Not checking for errors
   - **Integer arithmetic**: Losing precision in calculations
   - **Extraneous code**: Including prints/sleeps in timing
   - **No warm-up**: Cold start effects skewing results
   - **Cherry-picking**: Only reporting best results

8. **Best Practices for Benchmarking**:
   - Document test conditions (grid size, obstacle density, hardware)
   - Use fixed random seeds for reproducibility
   - Run warm-up iterations before collecting data
   - Report comprehensive statistics (mean, std dev, min, max)
   - Test multiple scenarios (not just one grid type)
   - Handle edge cases (no path exists, algorithm fails)
   - Export data for further analysis
   - Make results reproducible by others

**Testing the Fixed Code**:

1. Run the corrected version and verify:
   - Results are consistent across runs (due to random_seed=42)
   - Standard deviations are reasonable (< 20% of mean)
   - Both algorithms find paths of equal length
   - Success rates are 10/10 for both

2. Intentionally break it to verify error handling:
   ```python
   # Make goal unreachable
   grid.obstacles.add((19, 19))
   ```
   The benchmark should handle this gracefully and report 0/10 success rate.

3. Test with different random seeds to see natural variation:
   ```python
   for seed in [42, 123, 456]:
       grid = Grid(width=20, height=20, obstacle_density=0.2, random_seed=seed)
       # ... run benchmark
   ```

---

## Summary

These Week 9 solutions demonstrate professional benchmarking practices:

1. **Exercise 1**: Basic comparison showing fundamentals - same grid, multiple runs, clear reporting
2. **Exercise 2**: Multi-scenario testing revealing how algorithm performance varies with grid characteristics
3. **Exercise 3**: Production-quality suite with statistics, visualization, and intelligent recommendations
4. **Exercise 4**: Critical debugging skills for identifying and fixing common benchmarking mistakes

**Key Takeaways**:

- **Fair comparison requires identical inputs** - use the same grid, start, and goal
- **Multiple runs provide statistical reliability** - never trust a single measurement
- **Use appropriate metrics** - runtime for speed, nodes visited for efficiency, path length for quality
- **Test across scenarios** - algorithm performance is highly context-dependent
- **Handle failures gracefully** - algorithms can fail, benchmarks should continue
- **Visualize results** - plots make patterns immediately clear
- **Document thoroughly** - include test conditions, hardware specs, and methodology
- **Export data** - CSV files enable further analysis and reproducibility

These skills are essential for:
- Selecting the right algorithm for your use case
- Optimizing code performance
- Conducting research on new algorithms
- Making data-driven architectural decisions
- Detecting performance regressions in CI/CD pipelines

---

**Continue to Week 10: ML Heuristics →**
