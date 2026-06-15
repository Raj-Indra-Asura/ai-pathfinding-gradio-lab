# Week 9: Benchmarking and Performance Analysis

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 8](week_08_gradio_ui.md)** | **📝 [Week 9 Exercises](../exercises/week_09.md)** | **✅ [Week 9 Solutions](../solutions/week_09_solutions.md)** | **🔬 [Notebook](../notebooks/05_algorithm_comparison.ipynb)** | **➡️ [Next: Week 10](week_10_ml_heuristic.md)**

---

## 📋 Before You Start

> **🧭 Pipeline:** This week adds **box 9** to the [end-to-end pipeline](END_TO_END_PIPELINE.md) — benchmarking that compares algorithms fairly.

**What you should already know** (each links to where to learn or revisit it):

- `SearchResult` metric fields (a dataclass) — [Week 0 §4](week_00_python_prerequisites.md#prereq-dataclasses).
- pandas DataFrame basics — [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html).
- Random seeds for reproducible grids — [Week 2](week_02_grid_model.md).
- Dicts/lists for aggregating runs — [Week 0 §2](week_00_python_prerequisites.md#prereq-collections).

---

## Learning Goals

By the end of this week, you will understand:
- How to systematically measure algorithm performance
- Key performance metrics and what they reveal
- Statistical methods for reliable benchmarking
- How to compare algorithms fairly across different scenarios
- Visualization techniques for performance analysis
- Common pitfalls in benchmarking and how to avoid them

## Theory

### What is Benchmarking?

**Benchmarking** is the systematic measurement and comparison of algorithm performance. In pathfinding, we need to understand not just whether an algorithm finds a path, but how efficiently it does so across different scenarios.

### Why Benchmark?

1. **Algorithm Selection**: Choose the right algorithm for your use case
2. **Performance Optimization**: Identify bottlenecks and improvement opportunities
3. **Regression Detection**: Ensure code changes don't degrade performance
4. **Documentation**: Provide performance characteristics to users
5. **Research**: Compare new approaches against established baselines

### Key Performance Metrics

#### 1. **Runtime (Execution Time)**

The time taken to complete the search from start to finish.

- **Units**: Milliseconds (ms) or microseconds (μs)
- **What it measures**: Computational efficiency
- **Use case**: Critical for real-time applications like games or robotics

**Important**: Runtime can vary based on:
- Hardware (CPU speed, memory)
- System load (other processes)
- Implementation details (language, optimizations)
- Input characteristics (grid size, obstacle density)

#### 2. **Nodes Visited (Search Space Explored)**

The number of nodes examined during the search.

- **Units**: Count of nodes
- **What it measures**: Search efficiency and space complexity
- **Use case**: Independent of hardware, good for comparing algorithm logic

**Key insight**: Fewer nodes visited generally means better performance, but not always:
- A* visits fewer nodes than BFS but has higher per-node cost
- Bidirectional search may visit more nodes but find paths faster

#### 3. **Path Length**

The number of steps in the final path.

- **Units**: Number of nodes
- **What it measures**: Solution quality
- **Use case**: Important when path optimality matters

#### 4. **Path Cost**

The total cost of traversing the path (considering edge weights).

- **Units**: Cost units (depends on grid definition)
- **What it measures**: Solution quality for weighted graphs
- **Use case**: Critical when movement costs vary (terrain, traffic)

#### 5. **Memory Usage**

The amount of memory consumed during search.

- **Units**: Bytes or number of stored nodes
- **What it measures**: Space complexity
- **Use case**: Important for memory-constrained systems

### Statistical Benchmarking

Running an algorithm once is not enough! Performance can vary due to:
- System noise (other processes, context switching)
- Cache effects (first run vs subsequent runs)
- Random factors (hash table collisions, garbage collection)

#### Multiple Runs

Run each benchmark multiple times and report:

- **Mean (Average)**: Central tendency of performance
- **Median**: Middle value, less affected by outliers
- **Standard Deviation**: Measure of variability
- **Min/Max**: Range of performance

```python
# Example: 10 runs of A* on the same grid
runtimes = [12.3, 11.8, 12.5, 11.9, 12.1, 12.4, 12.0, 12.2, 11.7, 12.6]

mean = sum(runtimes) / len(runtimes)  # 12.15 ms
median = sorted(runtimes)[len(runtimes)//2]  # 12.15 ms
std_dev = calculate_std_dev(runtimes)  # ~0.3 ms
```

#### Warm-up Runs

The first few runs may be slower due to:
- JIT compilation (for languages like Python, Java)
- Cache warming
- Dynamic optimization

**Best practice**: Run a few warm-up iterations and discard them before collecting real data.

### Fair Comparison

To compare algorithms fairly:

1. **Same Input**: Use identical grids, start/goal positions
2. **Same Environment**: Run on the same hardware, similar system load
3. **Multiple Scenarios**: Test on diverse inputs (open grids, mazes, various sizes)
4. **Controlled Variables**: Change one factor at a time
5. **Statistical Significance**: Use enough samples to detect real differences

### Benchmarking Scenarios

#### Scenario 1: Open Grid (Low Obstacle Density < 10%)

**Characteristics**:
- Many possible paths
- Heuristics are very effective
- Path length matters

**Expected performance**:
- A* and Greedy: Excellent (heuristic guides search)
- BFS/Dijkstra: Good but explore more nodes
- DFS: Poor (explores irrelevant areas)

#### Scenario 2: Maze (High Obstacle Density > 30%)

**Characteristics**:
- Limited path options
- Many dead ends
- Heuristic can be misleading

**Expected performance**:
- BFS: Excellent (systematic exploration)
- Bidirectional BFS: Best (meets in middle)
- A*: Good (but less advantage)
- Greedy: Can be poor (follows heuristic into dead ends)

#### Scenario 3: Large Grid (> 50x50)

**Characteristics**:
- Huge search space
- Long paths
- Performance differences amplified

**Expected performance**:
- Bidirectional search: Excellent (reduces search space exponentially)
- A* with good heuristic: Good
- BFS/DFS: Poor (too much exploration)

#### Scenario 4: Variable Edge Costs

**Characteristics**:
- Different terrain types
- Cost-optimal path needed
- Simple path length insufficient

**Expected performance**:
- Dijkstra: Always optimal
- A* with admissible heuristic: Optimal and fast
- BFS: Finds shortest path, not lowest cost
- Greedy: Fast but not optimal

## Code Walkthrough

### Benchmark Module (`src/pathfinding_lab/metrics/benchmark.py`)

#### 1. `benchmark_algorithm()` Function

This function runs an algorithm multiple times and collects statistics:

```python
def benchmark_algorithm(
    algorithm_func: Callable,
    grid: Grid,
    start: Position,
    goal: Position,
    num_runs: int = 1
) -> Dict[str, float]:
    """
    Benchmark an algorithm over multiple runs.

    Returns average, min, max runtime and nodes visited.
    """
    runtimes = []
    nodes_visited_list = []

    for _ in range(num_runs):
        result = algorithm_func(grid, start, goal)
        runtimes.append(result.runtime_ms)
        nodes_visited_list.append(result.nodes_visited)

    return {
        'avg_runtime_ms': sum(runtimes) / len(runtimes),
        'min_runtime_ms': min(runtimes),
        'max_runtime_ms': max(runtimes),
        'avg_nodes_visited': sum(nodes_visited_list) / len(nodes_visited_list),
    }
```

**Key points**:
- Takes algorithm as a function parameter (higher-order function)
- Runs multiple times to get reliable statistics
- Collects both runtime and nodes visited
- Returns dictionary with statistical summaries

#### 2. `run_comparison()` Function

Compares multiple algorithms on the same grid:

```python
def run_comparison(
    algorithms: List[tuple],
    grid: Grid,
    start: Position,
    goal: Position
) -> List[SearchResult]:
    """
    Run multiple algorithms and collect results.

    algorithms: List of (name, function, kwargs) tuples
    """
    results = []

    for name, func, kwargs in algorithms:
        try:
            result = func(grid, start, goal, **kwargs)
            results.append(result)
        except Exception as e:
            # Handle failures gracefully
            results.append(SearchResult(
                algorithm_name=name,
                success=False,
                message=f"Error: {str(e)}"
            ))

    return results
```

**Key points**:
- Accepts algorithms as (name, function, kwargs) tuples
- Handles exceptions gracefully (some algorithms may fail)
- Returns uniform list of SearchResult objects
- Allows passing algorithm-specific parameters via kwargs

### Comparison Visualization (`src/pathfinding_lab/visualization/comparison_plot.py`)

#### 1. `create_comparison_table()` Function

Creates a pandas DataFrame for easy comparison:

```python
def create_comparison_table(results: List[SearchResult]) -> pd.DataFrame:
    """Create a comparison table for multiple algorithm results."""
    data = []
    for result in results:
        data.append({
            'Algorithm': result.algorithm_name,
            'Success': '✓' if result.success else '✗',
            'Path Length': result.path_length if result.success else 'N/A',
            'Path Cost': f"{result.path_cost:.2f}" if result.success else 'N/A',
            'Nodes Visited': result.nodes_visited,
            'Runtime (ms)': f"{result.runtime_ms:.2f}",
        })
    return pd.DataFrame(data)
```

**Key points**:
- Uses pandas for structured data representation
- Handles failed searches gracefully (shows N/A)
- Formats numbers for readability
- Easy to export to CSV, display in Gradio, or print

#### 2. `create_comparison_plot()` Function

Creates side-by-side bar charts:

```python
def create_comparison_plot(results: List[SearchResult], figsize: tuple = (12, 6)) -> plt.Figure:
    """Create bar charts comparing algorithm performance."""
    fig, axes = plt.subplots(1, 3, figsize=figsize)

    algorithms = [r.algorithm_name for r in results]
    nodes_visited = [r.nodes_visited for r in results]
    runtime_ms = [r.runtime_ms for r in results]
    path_costs = [r.path_cost if r.success else 0 for r in results]

    # Three subplots: nodes visited, runtime, path cost
    axes[0].bar(range(len(algorithms)), nodes_visited, color='skyblue')
    axes[1].bar(range(len(algorithms)), runtime_ms, color='lightcoral')
    axes[2].bar(range(len(algorithms)), path_costs, color='lightgreen')

    # ... set titles, labels, formatting ...
```

**Key points**:
- Three metrics visualized side-by-side
- Color-coded for easy interpretation
- Rotated x-axis labels for readability
- Tight layout prevents label overlap

## Common Mistakes

### 1. **Single-Run Benchmarks**

**Problem**: Running each algorithm once gives unreliable results due to system noise and variation.

```python
# BAD: Single run
result = astar(grid, start, goal, manhattan_distance)
print(f"A* took {result.runtime_ms:.2f} ms")
```

**Solution**: Run multiple times and report statistics.

```python
# GOOD: Multiple runs with statistics
runtimes = []
for _ in range(10):
    result = astar(grid, start, goal, manhattan_distance)
    runtimes.append(result.runtime_ms)

avg = sum(runtimes) / len(runtimes)
std = calculate_std_dev(runtimes)
print(f"A* took {avg:.2f} ± {std:.2f} ms (n=10)")
```

### 2. **Comparing Apples to Oranges**

**Problem**: Comparing algorithms on different grids or with different parameters.

```python
# BAD: Different grids
result1 = bfs(grid1, start1, goal1)
result2 = astar(grid2, start2, goal2, manhattan_distance)
# Can't meaningfully compare!
```

**Solution**: Use the same grid, start, and goal for all algorithms.

```python
# GOOD: Same inputs
algorithms = [
    ("BFS", bfs, {}),
    ("A*", astar, {"heuristic": manhattan_distance}),
]

results = run_comparison(algorithms, grid, start, goal)
```

### 3. **Ignoring Cold Start Effects**

**Problem**: First run is often slower due to cache warming, compilation, etc.

**Solution**: Run warm-up iterations before collecting data.

```python
# Warm-up: run 3 times without recording
for _ in range(3):
    _ = astar(grid, start, goal, manhattan_distance)

# Now collect real data
runtimes = []
for _ in range(10):
    result = astar(grid, start, goal, manhattan_distance)
    runtimes.append(result.runtime_ms)
```

### 4. **Not Testing Diverse Scenarios**

**Problem**: Only testing on one type of grid (e.g., open grids).

**Solution**: Test across multiple scenarios:

```python
scenarios = [
    ("Open Grid", 0.05),
    ("Moderate", 0.20),
    ("Maze", 0.35),
]

for scenario_name, obstacle_density in scenarios:
    grid = Grid(width=30, height=30, obstacle_density=obstacle_density)
    # ... run benchmarks ...
```

### 5. **Comparing Runtime Across Different Machines**

**Problem**: Reporting absolute runtime values (e.g., "A* takes 12.5 ms") without hardware context.

**Solution**:
- Report relative performance (e.g., "A* is 2.3x faster than BFS")
- Report nodes visited (hardware-independent)
- Document hardware specifications

### 6. **Not Accounting for Measurement Overhead**

**Problem**: Timer overhead can dominate measurement for very fast operations.

```python
# BAD: Measuring too-fast operations
start = time.perf_counter()
x = 1 + 1  # Too fast!
end = time.perf_counter()
# Overhead is larger than operation itself
```

**Solution**:
- Use appropriate time resolution (microseconds for fast ops)
- Ensure operations take at least several milliseconds
- Or run operation many times in a loop and divide by count

### 7. **Cherry-Picking Results**

**Problem**: Only reporting the best run or most favorable scenario.

**Solution**: Report all scenarios honestly, including worst-case performance.

## Mini Project Task

### This Week's Challenge: Build a Comprehensive Benchmarking Suite

Create a benchmarking suite that:
1. Runs all 6 algorithms on multiple grid types
2. Collects statistical data (mean, std dev, min, max)
3. Generates comparison visualizations
4. Exports results to CSV for further analysis
5. Provides performance recommendations

### Steps

1. **Create benchmark scenarios**: Define 5 different grid scenarios (open, moderate, maze, large, corridors)

2. **Set up algorithms**: Prepare all 6 algorithms with appropriate parameters

3. **Run benchmarks**: Execute each algorithm on each scenario with multiple runs

4. **Collect data**: Store results in a structured format (DataFrame)

5. **Visualize results**: Create comparison plots for each scenario

6. **Export data**: Save results to CSV files

7. **Generate report**: Create a summary showing which algorithms perform best in each scenario

### Success Criteria

- ✅ All 6 algorithms benchmarked on 5+ scenarios
- ✅ At least 5 runs per algorithm per scenario for statistical reliability
- ✅ Comparison tables showing all key metrics
- ✅ Visualization plots for each scenario
- ✅ CSV export with complete benchmark data
- ✅ Summary report with performance recommendations
- ✅ Code handles algorithm failures gracefully

### Example Output

```
Benchmark Results: Open Grid (20x20, 5% obstacles)
=======================================================
Algorithm           Runtime (ms)    Nodes Visited    Path Length
-----------------------------------------------------------------
BFS                 2.34 ± 0.12     156 ± 3          28
DFS                 3.87 ± 0.45     298 ± 67         45
Dijkstra            2.41 ± 0.09     159 ± 2          28
Greedy Best-First   0.89 ± 0.05     34 ± 1           29
A*                  0.92 ± 0.06     38 ± 2           28
Bidirectional BFS   1.67 ± 0.11     98 ± 4           28

Recommendation: A* provides optimal paths with excellent performance.
Greedy Best-First is fastest but path is slightly longer.
```

## Reflection Questions

1. **Why is it important to run benchmarks multiple times rather than relying on a single run?**
   - Consider: system noise, caching, garbage collection, statistical validity

2. **What are the trade-offs between runtime and nodes visited as performance metrics?**
   - Consider: hardware independence, implementation details, what each reveals

3. **Why might A* visit fewer nodes than BFS but have similar or longer runtime?**
   - Consider: per-node computation cost, heuristic evaluation, priority queue operations

4. **How do different grid characteristics affect which algorithm performs best?**
   - Consider: obstacle density, grid size, path tortuosity, branching factor

5. **What factors should you consider when choosing between Dijkstra and A* for a real application?**
   - Consider: availability of heuristics, optimality requirements, performance needs

6. **Why is reporting relative performance (e.g., "2x faster") often better than absolute values?**
   - Consider: hardware differences, reproducibility, clarity of comparison

7. **How would you benchmark an algorithm for a real-time system with strict latency requirements?**
   - Consider: worst-case vs average-case, tail latencies, deadline guarantees

## Additional Resources

### Performance Analysis
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/) - Complexity of common algorithms
- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [Algorithmic Complexity Analysis](https://www.geeksforgeeks.org/analysis-of-algorithms-set-1-asymptotic-analysis/)

### Statistical Methods
- [Introduction to Statistics for Data Analysis](https://www.khanacademy.org/math/statistics-probability)
- [Understanding Standard Deviation](https://www.mathsisfun.com/data/standard-deviation.html)

### Benchmarking Best Practices
- [How to Benchmark Code](https://pythonspeed.com/articles/consistent-benchmarking/)
- [Benchmarking Pitfalls](https://stackoverflow.blog/2021/10/18/best-practices-for-writing-code-comments/)

### Pathfinding Benchmarks
- [Moving AI Lab Benchmarks](https://movingai.com/benchmarks/) - Standard pathfinding benchmarks
- [Pathfinding Complexity Analysis](https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html)

## Next Week Preview

Next week, we'll explore **Machine Learning Heuristics** - using learned patterns to create better heuristic functions for A* and other informed search algorithms. You'll learn how to:

- Train ML models on pathfinding data
- Use learned heuristics to guide search
- Combine traditional and ML approaches
- Evaluate heuristic quality

This combines classical pathfinding with modern ML techniques!

---

**Continue to Week 10: ML Heuristics →**

---

## End-to-End Pipeline Connection

Benchmarking turns individual pathfinding runs into evidence:

```text
scenario definitions → repeated algorithm runs → collected SearchResults → tables/charts → algorithm recommendations
```

The goal is not just to find which algorithm is fastest once. The goal is to understand which algorithm is reliable for a class of maps.

### Benchmark Data Pipeline

A benchmark should record enough information to explain the result later:

- grid size
- obstacle density
- movement mode
- random seed or scenario name
- algorithm name
- heuristic name when relevant
- success or failure
- path length and path cost
- nodes visited
- runtime

With those fields, you can export results, compare regressions, and justify algorithm choices.

### Fair Comparison Rules

For fair benchmarks:

1. Run algorithms on the same grid.
2. Use the same start and goal.
3. Use fixed seeds for random obstacles.
4. Repeat runs when timing noise matters.
5. Separate correctness metrics from speed metrics.

A fast algorithm that fails to find a path is not better than a slower algorithm that succeeds.

### How Benchmarks Feed the Product

Benchmark results can guide UI explanations. For example, after running all algorithms, the app can explain that BFS is strong on unweighted grids, Dijkstra is reliable for weighted costs, and A* often reduces visited nodes when paired with a suitable heuristic.

### Regression Thinking

As you polish the project, benchmark outputs become guardrails. If a refactor makes A* visit twice as many nodes on the same scenario, investigate before accepting the change.

### Week 9 Build Checkpoint

You are ready for Week 10 when you can design a repeatable scenario, run multiple algorithms on it, and explain the result using both plots and metrics.
