# Week 6: Heuristic Functions Deep Dive

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 5](week_05_astar.md)** | **📝 [Week 6 Exercises](../exercises/week_06.md)** | **✅ [Week 6 Solutions](../solutions/week_06_solutions.md)** | **🔬 [Notebook](../notebooks/04_heuristics.ipynb)** | **➡️ [Next: Week 7](week_07_visualization.md)**

---

## 📋 Before You Start

> **🧭 Pipeline:** This week adds **box 6** to the [end-to-end pipeline](END_TO_END_PIPELINE.md) — the heuristic library A* chooses from.

**What you should already know** (each links to where to learn or revisit it):

- A* and the `f = g + h` idea — [Week 5](week_05_astar.md).
- Heuristics are plain functions over positions — [Week 0 §7](week_00_python_prerequisites.md#prereq-typehints).
- Tuples & unpacking — [Week 0 §1](week_00_python_prerequisites.md#prereq-tuples).
- Basic math: `abs`, `sqrt`, `min`/`max` — [Python math module](https://docs.python.org/3/library/math.html).

---

## Learning Goals

By the end of this week, you will understand:
- The mathematical foundations of heuristic functions
- Manhattan, Euclidean, Chebyshev, and Octile distance metrics
- Admissibility and consistency properties in depth
- How to choose the right heuristic for different grid configurations
- The impact of heuristic accuracy on A* performance
- Weighted heuristics and the speed-optimality tradeoff

## Theory

### What Are Heuristic Functions?

A **heuristic function** `h(n)` estimates the cost from node `n` to the goal. In A* search, the heuristic guides the algorithm toward the goal by prioritizing nodes that appear closer to the target.

**Key equation**: `f(n) = g(n) + h(n)`
- `g(n)`: Actual cost from start to node `n`
- `h(n)`: Estimated cost from node `n` to goal (heuristic)
- `f(n)`: Total estimated cost through node `n`

### Admissibility: Never Overestimate

A heuristic is **admissible** if it never overestimates the actual cost to reach the goal:

```
h(n) ≤ h*(n)  for all nodes n
```

Where `h*(n)` is the true optimal cost from `n` to the goal.

**Why it matters**: An admissible heuristic guarantees that A* finds the optimal path. If you overestimate, A* may overlook the true shortest path.

**Example**:
- True distance from `n` to goal: 10 units
- Manhattan distance estimate: 8 units ✅ (admissible)
- Euclidean distance estimate: 7 units ✅ (admissible)
- Random overestimate: 12 units ❌ (not admissible)

### Consistency (Monotonicity): The Triangle Inequality

A heuristic is **consistent** (or monotonic) if for every node `n` and successor `n'`:

```
h(n) ≤ cost(n, n') + h(n')
```

This means the estimated cost from `n` to the goal should not be greater than the cost to move to successor `n'` plus the estimate from `n'` to the goal. It's essentially the triangle inequality.

**Why it matters**: Consistency is stronger than admissibility and ensures A* never reopens closed nodes, making the algorithm more efficient. Every consistent heuristic is admissible, but not vice versa.

### The Four Classic Distance Metrics

#### 1. Manhattan Distance (L1 Norm)

```
h(n) = |x₁ - x₂| + |y₁ - y₂|
```

**Use case**: 4-directional grids (up, down, left, right)
**Properties**: Admissible and consistent for 4-directional movement
**Analogy**: Like navigating city blocks where you can only move along streets

**When to use**:
- Grid-based games with 4-directional movement
- Manhattan world environments
- When diagonal movement is not allowed

#### 2. Euclidean Distance (L2 Norm)

```
h(n) = √[(x₁ - x₂)² + (y₁ - y₂)²]
```

**Use case**: 8-directional grids, continuous spaces
**Properties**: Admissible for 8-directional movement, but may not be consistent depending on grid cost configuration
**Analogy**: Straight-line "as the crow flies" distance

**When to use**:
- Open spaces with free movement
- 8-directional grids where diagonal cost equals cardinal cost
- Real-world navigation where paths can be diagonal

**Caveat**: On grids where diagonal moves cost √2 and cardinal moves cost 1, Euclidean distance might slightly underestimate in certain configurations. Use Octile distance instead for perfect accuracy.

#### 3. Chebyshev Distance (L∞ Norm)

```
h(n) = max(|x₁ - x₂|, |y₁ - y₂|)
```

**Use case**: 8-directional grids where diagonal and cardinal moves have equal cost
**Properties**: Admissible and consistent when all moves cost the same
**Analogy**: Like a king moving on a chessboard (any direction, 1 square = 1 cost)

**When to use**:
- Chess-like movement patterns
- 8-directional grids with uniform cost (all moves cost 1)
- When you want maximum speed with minimal computation

#### 4. Octile Distance (Optimal for 8-directional)

```
h(n) = D × (dx + dy) + (D₂ - 2D) × min(dx, dy)
```

Where:
- `D = 1.0` (cost of cardinal moves)
- `D₂ = √2 ≈ 1.414` (cost of diagonal moves)
- `dx = |x₁ - x₂|`, `dy = |y₁ - y₂|`

**Use case**: 8-directional grids with realistic diagonal costs (√2 for diagonal, 1 for cardinal)
**Properties**: Admissible and consistent for standard 8-directional grids
**Analogy**: The true minimum cost when you can move diagonally at cost √2

**When to use**:
- Standard 8-directional pathfinding (most common case)
- Games with realistic movement costs
- When you want optimal A* performance on 8-directional grids

### Heuristic Accuracy and Performance

**The accuracy spectrum**:

1. **h(n) = 0** (Zero heuristic)
   - Always admissible (never overestimates)
   - A* degenerates into Dijkstra's algorithm
   - Explores many unnecessary nodes
   - Slowest, but guaranteed optimal

2. **h(n) < h*(n)** (Underestimate)
   - Admissible ✅
   - Explores more nodes than necessary
   - Slower, but still optimal
   - Example: Manhattan on an 8-directional grid

3. **h(n) = h*(n)** (Perfect heuristic)
   - Admissible ✅
   - A* follows the optimal path directly
   - Fastest possible while maintaining optimality
   - Impossible in practice (requires knowing the answer)

4. **h(n) > h*(n)** (Overestimate)
   - Not admissible ❌
   - May find suboptimal paths
   - Can be faster but loses optimality guarantee
   - Example: Weighted heuristics with weight > 1

**Rule of thumb**: The closer `h(n)` is to `h*(n)` without exceeding it, the fewer nodes A* explores.

### Weighted Heuristics: Trading Optimality for Speed

Sometimes you want faster results and don't need the absolute optimal path. **Weighted heuristics** multiply the heuristic by a weight `w`:

```
f(n) = g(n) + w × h(n)
```

**Effects**:
- `w = 1.0`: Standard A*, optimal paths
- `w > 1.0`: Greedier search, faster but suboptimal (e.g., `w = 1.5`)
- `w < 1.0`: More conservative, may explore even more nodes than standard A*

**Bounded suboptimality**: With weight `w`, the path cost is at most `w` times the optimal cost. For `w = 1.5`, you might get a path up to 50% longer than optimal, but much faster.

**When to use**:
- Real-time games where speed matters more than perfection
- Large maps where optimal search is too slow
- Initial pathfinding passes (use weighted A*, then refine)

## Code Walkthrough

### Manhattan Distance Implementation

File: `src/pathfinding_lab/heuristics/manhattan.py`

```python
def manhattan_distance(pos1: Position, pos2: Position) -> float:
    row1, col1 = pos1
    row2, col2 = pos2
    return abs(row1 - row2) + abs(col1 - col2)
```

**Key points**:
- Simple sum of absolute differences
- No square roots → fast computation
- Perfect for 4-directional grids
- Returns a float for consistency with other heuristics

**Computational complexity**: O(1), extremely fast

### Euclidean Distance Implementation

File: `src/pathfinding_lab/heuristics/euclidean.py`

```python
import math

def euclidean_distance(pos1: Position, pos2: Position) -> float:
    row1, col1 = pos1
    row2, col2 = pos2
    return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)
```

**Key points**:
- Requires `math.sqrt()` → slightly slower than Manhattan
- Returns straight-line distance
- Good for 8-directional grids
- More accurate than Manhattan for diagonal-heavy paths

**Computational complexity**: O(1), but ~5-10x slower than Manhattan due to square root

### Octile Distance Implementation

File: `src/pathfinding_lab/heuristics/octile.py`

```python
import math

def octile_distance(pos1: Position, pos2: Position) -> float:
    row1, col1 = pos1
    row2, col2 = pos2

    dx = abs(row1 - row2)
    dy = abs(col1 - col2)

    D = 1.0  # Cardinal movement cost
    D2 = math.sqrt(2)  # Diagonal movement cost

    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
```

**Key points**:
- Perfectly models 8-directional movement with realistic costs
- Formula breakdown:
  - `D * (dx + dy)`: Total cost if moving only cardinally
  - `(D2 - 2 * D) * min(dx, dy)`: Adjustment for diagonal moves
  - `min(dx, dy)`: Maximum diagonals you can take
- Most accurate admissible heuristic for standard 8-directional grids

**Why this formula works**:
- You can move diagonally `min(dx, dy)` times (cost: `√2` each)
- Remaining distance is cardinal-only: `|dx - dy|` moves (cost: 1 each)
- Total: `√2 × min(dx, dy) + 1 × |dx - dy|`
- Simplified: `dx + dy + (√2 - 2) × min(dx, dy)`

### Weighted Heuristic Implementation

File: `src/pathfinding_lab/heuristics/weighted.py`

```python
def weighted_manhattan_distance(pos1: Position, pos2: Position, weight: float = 1.0) -> float:
    row1, col1 = pos1
    row2, col2 = pos2
    manhattan = abs(row1 - row2) + abs(col1 - col2)
    return weight * manhattan
```

**Key points**:
- Simple multiplication by weight factor
- `weight = 1.0`: Standard admissible heuristic
- `weight > 1.0`: Trades optimality for speed
- Can be applied to any base heuristic (Manhattan, Euclidean, etc.)

### Using Heuristics with A*

From `src/pathfinding_lab/algorithms/astar.py`:

```python
def astar(
    grid: Grid,
    start: Position,
    goal: Position,
    heuristic: Callable[[Position, Position], float]
) -> SearchResult:
    # Initial heuristic estimate
    h_start = heuristic(start, goal)
    pq = [(h_start, 0.0, start)]

    while pq:
        f, current_g, current = heapq.heappop(pq)

        # ... process current node ...

        for neighbor in grid.get_neighbors(current):
            tentative_g = current_g + move_cost

            if tentative_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative_g
                h = heuristic(neighbor, goal)  # Evaluate heuristic
                f_cost = tentative_g + h
                heapq.heappush(pq, (f_cost, tentative_g, neighbor))
```

**Key points**:
- Heuristic is a function passed as a parameter
- Called once per node expansion: `h = heuristic(neighbor, goal)`
- Combined with actual cost: `f_cost = g + h`
- Flexibility: swap heuristics without changing A* code

## Common Mistakes

### 1. Using Manhattan Distance on 8-Directional Grids

**Problem**: Manhattan distance underestimates significantly when diagonal movement is allowed. While still admissible, it causes A* to explore many unnecessary nodes.

**Example**:
- Goal is 10 cells diagonally away
- Manhattan says: `|10-0| + |10-0| = 20` moves
- Actual cost with diagonals: `10 × √2 ≈ 14.14` moves
- A* explores ~40% more nodes than necessary

**Solution**: Use Octile distance for 8-directional grids with realistic costs, or Chebyshev if all moves cost the same.

### 2. Forgetting to Handle Zero Division or Edge Cases

**Problem**: Some heuristic implementations might have edge cases where the start and goal are the same, or involve division.

**Example**:
```python
# Bad: doesn't handle start == goal
def bad_heuristic(pos1, pos2):
    return (pos2[0] - pos1[0]) / (pos2[1] - pos1[1])  # Division by zero!
```

**Solution**: Always test with start == goal, and avoid division in heuristic calculations. Return 0 when positions are equal.

```python
def safe_heuristic(pos1, pos2):
    if pos1 == pos2:
        return 0.0
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
```

### 3. Overestimating with Custom Heuristics

**Problem**: Creating a custom heuristic that occasionally overestimates, breaking admissibility and causing suboptimal paths.

**Example**:
```python
# Bad: overestimates when obstacles are present
def bad_heuristic(pos1, pos2):
    return manhattan_distance(pos1, pos2) * 1.1  # 10% overestimate
```

**Solution**: Always ensure `h(n) ≤ h*(n)`. Test against Dijkstra's algorithm (which finds true optimal costs) to verify admissibility:

```python
def verify_admissibility(grid, start, goal, heuristic):
    # Run Dijkstra to get true costs
    dijkstra_result = dijkstra(grid, start, goal)
    true_cost = dijkstra_result.path_cost

    # Check heuristic estimate
    h_estimate = heuristic(start, goal)

    assert h_estimate <= true_cost, f"Heuristic overestimates: {h_estimate} > {true_cost}"
```

### 4. Confusing Euclidean with Octile

**Problem**: Using Euclidean distance on standard 8-directional grids thinking it's the most accurate, but Octile is actually more precise.

**Why**:
- Euclidean assumes continuous movement at any angle
- Octile models discrete 8-directional grid movement exactly
- Euclidean: `√(dx² + dy²)`
- Octile: `max(dx, dy) + (√2 - 1) × min(dx, dy)`

**Example** (10 cells diagonal):
- Euclidean: `√(100 + 100) ≈ 14.14`
- Octile: `10 × √2 ≈ 14.14`
- Same result in this case, but Octile is always accurate

**Solution**: Use Octile for 8-directional grids with standard costs (diagonal = √2, cardinal = 1).

### 5. Not Considering Heuristic Computation Cost

**Problem**: Using an expensive heuristic (like complex geometric calculations) that makes A* slower than Dijkstra.

**Example**:
```python
# Bad: extremely expensive heuristic
def expensive_heuristic(pos1, pos2):
    # Simulating complex terrain analysis
    cost = 0
    for i in range(1000):
        cost += math.sin(pos1[0] + i) * math.cos(pos2[1] + i)
    return abs(cost)
```

**Solution**: Keep heuristics simple. The heuristic is called many times per search, so it should be O(1) and fast. If your heuristic takes longer than processing a node, use a simpler one.

**Benchmark**:
- Manhattan: ~10 nanoseconds
- Euclidean: ~50 nanoseconds (due to sqrt)
- Complex calculations: microseconds or worse ❌

## Mini Project Task

### This Week's Challenge: Heuristic Comparison Framework

Build a comprehensive comparison tool that evaluates different heuristics on the same pathfinding problem. Your tool should measure:
- Nodes explored
- Path cost found
- Runtime
- Path optimality (compared to Dijkstra)

### Steps

1. **Create a test scenario generator**
   - Generate grids with various configurations (open, maze-like, weighted terrain)
   - Define start/goal pairs at different distances

2. **Run A* with multiple heuristics**
   - Manhattan, Euclidean, Chebyshev, Octile
   - Weighted variants (w = 1.0, 1.3, 1.5, 2.0)
   - Zero heuristic (equivalent to Dijkstra)

3. **Collect and compare metrics**
   - Nodes visited: fewer is better (efficiency)
   - Path cost: should match Dijkstra for admissible heuristics
   - Runtime: measure in milliseconds
   - Path length: number of steps in the path

4. **Analyze the results**
   - Which heuristic explores the fewest nodes?
   - How does heuristic accuracy affect performance?
   - What's the speed-optimality tradeoff for weighted heuristics?

### Success Criteria

- ✅ Framework runs A* with at least 5 different heuristics
- ✅ Outputs clear comparison metrics (nodes, cost, time)
- ✅ Verifies path optimality for admissible heuristics
- ✅ Includes at least one weighted heuristic test
- ✅ Generates a summary table or visualization of results

### Example Output

```
Heuristic Comparison on 50x50 grid (Start: (5,5), Goal: (45,45))
================================================================
Heuristic          | Nodes Visited | Path Cost | Runtime (ms) | Optimal
-------------------|---------------|-----------|--------------|--------
Zero (Dijkstra)    |          2487 |     56.57 |        12.34 |   Yes
Manhattan          |           876 |     56.57 |         4.82 |   Yes
Euclidean          |           654 |     56.57 |         5.23 |   Yes
Octile             |           548 |     56.57 |         3.91 |   Yes
Chebyshev          |           712 |     56.57 |         4.15 |   Yes
Weighted (1.3)     |           432 |     58.12 |         3.02 |   No
Weighted (1.5)     |           287 |     61.23 |         2.34 |   No
```

## Reflection Questions

1. **Why is admissibility crucial for A* optimality?**
   - What happens when you use a non-admissible heuristic?
   - Can you construct an example where overestimating by just 1 unit causes a suboptimal path?

2. **What's the relationship between heuristic accuracy and nodes explored?**
   - If Manhattan explores 1000 nodes and Octile explores 600, what does this tell you?
   - Why doesn't a more accurate heuristic always mean faster runtime?

3. **When would you choose a weighted heuristic over an admissible one?**
   - What types of applications prioritize speed over optimality?
   - How would you decide what weight value to use?

4. **How does grid configuration affect heuristic choice?**
   - What heuristic would you use for a 4-directional grid? 8-directional?
   - What if diagonal moves cost 1.5 instead of √2?

5. **Can you design a heuristic that's admissible but not consistent?**
   - What properties would it need?
   - Why is consistency desirable even though admissibility is sufficient for optimality?

## Additional Resources

- **AI: A Modern Approach** (Russell & Norvig) - Chapter 3.5 on Informed Search
- **Red Blob Games: A* Tutorial** - Excellent visual explanations: https://www.redblobgames.com/pathfinding/a-star/introduction.html
- **Distance Metrics in Machine Learning** - Understanding L1, L2, L∞ norms
- **Weighted A* and Bounded Suboptimality** - Research on speed-optimality tradeoffs
- **Heuristic Functions in Game AI** - Practical applications in game development

## Next Week Preview

Next week, we'll explore **visualization techniques** for pathfinding algorithms. You'll learn how to:
- Animate search progression step by step
- Visualize the difference between visited nodes and the final path
- Display heuristic heat maps showing estimated distances
- Create interactive debugging tools to understand algorithm behavior
- Build intuition for why algorithms make certain decisions

Visualization is key to understanding and debugging pathfinding algorithms!

---

**Continue to Week 7: Visualization Techniques →**

---

## End-to-End Pipeline Connection

Heuristics are plug-in decision helpers for informed algorithms:

```text
movement mode + goal position → heuristic function → A*/Greedy priority → visited nodes and runtime
```

A good heuristic improves the search pipeline without changing the grid, visualization, UI, or result format.

### Choosing the Right Heuristic

Use the movement rules to choose the heuristic:

- 4-directional movement: Manhattan is usually the clearest match.
- 8-directional movement with diagonal cost near 1: Chebyshev can be useful.
- 8-directional movement with diagonal cost around sqrt(2): Octile is usually a strong fit.
- Open geometric spaces: Euclidean is intuitive and easy to explain.
- Speed-over-optimality experiments: weighted heuristics show the trade-off clearly.

The key question is: "Does this estimate match what movement is actually allowed to do?"

### Heuristic Impact on the Product

Changing a heuristic can change:

- how many cells A* visits
- how quickly the search finishes
- how direct the visible search pattern looks
- whether weighted variants trade optimality for speed
- how learners interpret algorithm behavior in the UI

That means heuristics affect both performance and education.

### Custom Heuristic Checklist

Before using a custom heuristic in the product:

1. It should accept the same position inputs as the existing heuristics.
2. It should return a numeric estimate.
3. It should be fast enough to call many times.
4. It should not read or mutate UI state.
5. If optimality matters, verify that it does not overestimate the true remaining cost.

### Integration Example in Words

The UI dropdown chooses a heuristic name. The app maps that name to a function. A* receives that function and calls it whenever it evaluates a neighbor. The returned estimate affects priority queue order. The final result records how much work the algorithm did, and visualization makes that work visible.

### Week 6 Build Checkpoint

You are ready for Week 7 when you can choose a heuristic for a movement mode and predict whether it will make A* focused, broad, fast, or risky.
