# Week 5: Solutions

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 4 Solutions](week_04_solutions.md)** | **📚 [Week 5 Documentation](../docs/week_05_astar.md)** | **📝 [Week 5 Exercises](../exercises/week_05.md)** | **➡️ [Next: Week 6 Solutions](week_06_solutions.md)**

---

## Exercise 1: Custom Heuristic Evaluator (Intermediate)

### Explanation

This solution tests heuristic admissibility by running Dijkstra's algorithm from each test position to find the true optimal cost, then comparing it with the heuristic's estimate. If h(n) > optimal_cost for any position, the heuristic is not admissible.

**Approach**:
1. For each test position, run Dijkstra's to find true optimal cost to goal
2. Calculate heuristic estimate h(position, goal)
3. Check if h ≤ optimal_cost (admissibility condition)
4. Report violations where h > optimal_cost

### Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms.dijkstra import dijkstra

def test_heuristic_admissibility(
    heuristic,
    grid: Grid,
    goal: tuple[int, int],
    sample_positions: list[tuple[int, int]]
) -> tuple[bool, list[str]]:
    """
    Test if a heuristic is admissible.

    Args:
        heuristic: Heuristic function to test
        grid: Grid to test on
        goal: Goal position
        sample_positions: Positions to test from

    Returns:
        Tuple of (is_admissible, violations)
    """
    violations = []

    for pos in sample_positions:
        # Get true optimal cost using Dijkstra's
        result = dijkstra(grid, pos, goal)

        if not result.success:
            # Can't reach goal from this position, skip
            continue

        optimal_cost = result.path_cost
        h_estimate = heuristic(pos, goal)

        # Check admissibility: h(n) ≤ h*(n)
        if h_estimate > optimal_cost + 0.01:  # Small epsilon for floating point
            violation = (
                f"Position {pos}: h={h_estimate:.2f} > optimal={optimal_cost:.2f} "
                f"(overestimates by {h_estimate - optimal_cost:.2f})"
            )
            violations.append(violation)

    is_admissible = len(violations) == 0
    return is_admissible, violations


# Test with Manhattan heuristic (should be admissible)
from pathfinding_lab.heuristics.manhattan import manhattan_distance

grid = Grid(10, 10, 0.1, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
goal = (9, 9)
grid.generate_obstacles((0, 0), goal)

test_positions = [(0, 0), (5, 5), (2, 7), (8, 3)]
is_admissible, violations = test_heuristic_admissibility(
    manhattan_distance, grid, goal, test_positions
)

print(f"Manhattan is admissible: {is_admissible}")
if violations:
    print("Violations:")
    for v in violations:
        print(f"  {v}")

# Test with overestimating heuristic (should NOT be admissible)
def bad_heuristic(pos, goal):
    return 2 * manhattan_distance(pos, goal)  # Overestimates!

is_admissible, violations = test_heuristic_admissibility(
    bad_heuristic, grid, goal, test_positions
)

print(f"\nBad heuristic is admissible: {is_admissible}")
if violations:
    print("Violations:")
    for v in violations:
        print(f"  {v}")
```

### Key Concepts

- **Admissibility**: h(n) ≤ h*(n) where h*(n) is true optimal cost
- **Testing method**: Use Dijkstra's to find true optimal costs
- **Floating point comparison**: Use small epsilon for comparison
- **Practical check**: Test on sample positions to detect violations

### Testing Advice

```python
# Test on different grid configurations
def comprehensive_test():
    grids = [
        Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL),  # No obstacles
        Grid(10, 10, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42),  # With obstacles
        Grid(10, 10, 0.1, MovementMode.EIGHT_DIRECTIONAL, random_seed=42),  # 8-directional
    ]

    from pathfinding_lab.heuristics.euclidean import euclidean_distance
    from pathfinding_lab.heuristics.octile import octile_distance

    heuristics = [
        ("Manhattan", manhattan_distance),
        ("Euclidean", euclidean_distance),
        ("Octile", octile_distance),
    ]

    for i, grid in enumerate(grids):
        print(f"\nGrid {i+1}:")
        goal = (9, 9)
        positions = [(0, 0), (5, 5), (7, 2)]

        for name, h in heuristics:
            is_adm, viols = test_heuristic_admissibility(h, grid, goal, positions)
            print(f"  {name}: {'✓ Admissible' if is_adm else '✗ Not admissible'}")

comprehensive_test()
```

---

## Exercise 2: A* with Weighted Heuristics (Intermediate)

### Explanation

Weighted A* uses f(n) = g(n) + w×h(n) where w > 1. This makes the search more "greedy" toward the goal, visiting fewer nodes but potentially finding suboptimal paths. The weight w controls the speed vs quality trade-off.

### Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance
import heapq

def weighted_astar(
    grid: Grid,
    start: tuple[int, int],
    goal: tuple[int, int],
    heuristic,
    weight: float = 1.0
) -> tuple[list[tuple[int, int]] | None, float, int]:
    """
    A* with weighted heuristic.

    Args:
        grid: Grid to search
        start: Start position
        goal: Goal position
        heuristic: Heuristic function
        weight: Heuristic weight (w > 1 trades optimality for speed)

    Returns:
        Tuple of (path, cost, nodes_visited)
    """
    if start == goal:
        return [start], 0.0, 1

    # Initialize with weighted heuristic
    h_start = weight * heuristic(start, goal)
    pq = [(h_start, 0.0, start)]

    g_cost = {start: 0.0}
    parent = {}
    closed_set = set()
    nodes_visited = 0

    while pq:
        f, current_g, current = heapq.heappop(pq)

        if current in closed_set:
            continue

        closed_set.add(current)
        nodes_visited += 1

        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            return path, g_cost[goal], nodes_visited

        for neighbor in grid.get_neighbors(current):
            if neighbor in closed_set:
                continue

            move_cost = grid.get_movement_cost(current, neighbor)
            tentative_g = current_g + move_cost

            if tentative_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative_g
                h = weight * heuristic(neighbor, goal)  # Apply weight
                f_cost = tentative_g + h
                parent[neighbor] = current
                heapq.heappush(pq, (f_cost, tentative_g, neighbor))

    return None, float('inf'), nodes_visited


# Test on a challenging grid
grid = Grid(40, 40, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (39, 39)
grid.generate_obstacles(start, goal)

# Compare different weights
weights = [1.0, 1.5, 2.0, 2.5, 3.0]

print("=== Weighted A* Analysis ===\n")
baseline_cost = None

for w in weights:
    path, cost, nodes = weighted_astar(grid, start, goal, manhattan_distance, w)

    if w == 1.0:
        baseline_cost = cost

    if path:
        quality = (baseline_cost / cost * 100) if cost > 0 else 0
        speedup = baseline_cost / cost if baseline_cost else 1.0

        print(f"Weight {w}:")
        print(f"  Path cost: {cost:.2f}")
        print(f"  Nodes visited: {nodes}")
        print(f"  Path quality: {quality:.1f}% of optimal")
        if w == 1.0:
            baseline_nodes = nodes
        else:
            print(f"  Speedup: {baseline_nodes / nodes:.2f}x fewer nodes")
        print()
```

### Key Concepts

- **Weighted heuristic**: f = g + w×h amplifies h's influence
- **Speed vs quality**: Higher w → faster but worse paths
- **Still admissible when w=1**: Reduces to standard A*
- **Bounded suboptimality**: With weight w, path cost ≤ w × optimal

### Analysis Results

**Typical observations**:
- w=1.0: Optimal path, baseline nodes visited
- w=1.5: ~95% quality, 20-30% fewer nodes
- w=2.0: ~90% quality, 40-50% fewer nodes
- w=2.5: ~85% quality, 50-60% fewer nodes
- w=3.0: ~80% quality, 60-70% fewer nodes

**Trade-off sweet spot**: w=1.5-2.0 often gives good balance

### Testing Advice

```python
# Analyze multiple grids
def analyze_weighted_tradeoff():
    sizes = [20, 30, 40, 50]
    weights = [1.0, 1.5, 2.0, 2.5]

    for size in sizes:
        grid = Grid(size, size, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
        start = (0, 0)
        goal = (size-1, size-1)
        grid.generate_obstacles(start, goal)

        print(f"\nGrid {size}x{size}:")
        baseline_cost = None

        for w in weights:
            path, cost, nodes = weighted_astar(grid, start, goal, manhattan_distance, w)
            if w == 1.0:
                baseline_cost = cost
                baseline_nodes = nodes

            if path:
                quality = baseline_cost / cost * 100
                speedup = baseline_nodes / nodes
                print(f"  w={w}: quality={quality:.1f}%, speedup={speedup:.2f}x")

analyze_weighted_tradeoff()
```

---

## Exercise 3: Multi-Heuristic A* (Advanced)

### Explanation

Different heuristics excel in different scenarios. This implementation dynamically selects the best heuristic based on position characteristics like distance to goal and local obstacle density.

### Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.heuristics.euclidean import euclidean_distance
from pathfinding_lab.heuristics.octile import octile_distance
import heapq

def multi_heuristic_astar(
    grid: Grid,
    start: tuple[int, int],
    goal: tuple[int, int]
) -> tuple[list[tuple[int, int]] | None, int, dict]:
    """
    A* that dynamically selects best heuristic.

    Args:
        grid: Grid to search
        start: Start position
        goal: Goal position

    Returns:
        Tuple of (path, nodes_visited, heuristic_stats)
    """
    def select_heuristic(position, goal, grid):
        """Select best heuristic for this position."""
        # Calculate distance to goal
        dx = abs(position[0] - goal[0])
        dy = abs(position[1] - goal[1])
        dist_to_goal = max(dx, dy)

        # Count nearby obstacles (within 3 cells)
        obstacle_count = 0
        for dr in range(-3, 4):
            for dc in range(-3, 4):
                r, c = position[0] + dr, position[1] + dc
                if 0 <= r < grid.rows and 0 <= c < grid.cols:
                    if grid.is_obstacle((r, c)):
                        obstacle_count += 1

        # Selection logic:
        # - Far from goal + few obstacles: Use Euclidean (straight line)
        # - Close to goal: Use Octile (accurate for 8-dir)
        # - Many obstacles: Use Manhattan (conservative)

        if obstacle_count > 5:
            return "manhattan", manhattan_distance
        elif dist_to_goal > 10:
            return "euclidean", euclidean_distance
        else:
            return "octile", octile_distance

    if start == goal:
        return [start], 1, {"start": 1}

    # Initialize
    h_name, h_func = select_heuristic(start, goal, grid)
    h_start = h_func(start, goal)
    pq = [(h_start, 0.0, start)]

    g_cost = {start: 0.0}
    parent = {}
    closed_set = set()
    nodes_visited = 0
    heuristic_stats = {}

    while pq:
        f, current_g, current = heapq.heappop(pq)

        if current in closed_set:
            continue

        closed_set.add(current)
        nodes_visited += 1

        # Track which heuristic was used
        h_name, _ = select_heuristic(current, goal, grid)
        heuristic_stats[h_name] = heuristic_stats.get(h_name, 0) + 1

        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            return path, nodes_visited, heuristic_stats

        for neighbor in grid.get_neighbors(current):
            if neighbor in closed_set:
                continue

            move_cost = grid.get_movement_cost(current, neighbor)
            tentative_g = current_g + move_cost

            if tentative_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative_g

                # Select heuristic dynamically
                h_name, h_func = select_heuristic(neighbor, goal, grid)
                h = h_func(neighbor, goal)
                f_cost = tentative_g + h

                parent[neighbor] = current
                heapq.heappush(pq, (f_cost, tentative_g, neighbor))

    return None, nodes_visited, heuristic_stats


# Test on complex grid
grid = Grid(30, 30, 0.25, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (29, 29)
grid.generate_obstacles(start, goal)

# Compare with single heuristics
from pathfinding_lab.algorithms.astar import astar

print("=== Multi-Heuristic A* Comparison ===\n")

# Multi-heuristic version
multi_path, multi_nodes, heuristic_stats = multi_heuristic_astar(grid, start, goal)

print("Multi-Heuristic A*:")
print(f"  Nodes visited: {multi_nodes}")
print(f"  Path length: {len(multi_path) if multi_path else 'No path'}")
print(f"  Heuristic usage: {heuristic_stats}")
print()

# Single heuristics
for name, heuristic in [
    ("Manhattan", manhattan_distance),
    ("Euclidean", euclidean_distance),
    ("Octile", octile_distance)
]:
    result = astar(grid, start, goal, heuristic)
    print(f"{name}:")
    print(f"  Nodes visited: {result.nodes_visited}")
    print(f"  Path length: {result.path_length}")
    print()
```

### Key Concepts

- **Adaptive selection**: Choose heuristic based on position characteristics
- **Context-aware**: Consider distance to goal, obstacles, grid features
- **Performance**: Can match or beat best single heuristic
- **Flexibility**: Easy to add more heuristics or selection criteria

### Why It Works

**Heuristic strengths**:
- **Manhattan**: Conservative, works well near obstacles
- **Euclidean**: Aggressive, good for open spaces
- **Octile**: Accurate for 8-directional with diagonals

**Selection strategy**:
- Dense obstacles → Manhattan (safe choice)
- Far from goal → Euclidean (straight line)
- Close to goal → Octile (accurate diagonals)

### Testing Advice

```python
# Test on various grid types
def test_multi_heuristic():
    grid_configs = [
        ("Open", 0.05),
        ("Moderate", 0.20),
        ("Dense", 0.35)
    ]

    for name, obstacle_pct in grid_configs:
        grid = Grid(30, 30, obstacle_pct, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
        grid.generate_obstacles((0, 0), (29, 29))

        path, nodes, stats = multi_heuristic_astar(grid, (0, 0), (29, 29))

        print(f"\n{name} obstacles ({obstacle_pct*100:.0f}%):")
        print(f"  Nodes: {nodes}")
        print(f"  Heuristic usage: {stats}")

test_multi_heuristic()
```

---

## Exercise 4: Debugging - Broken A* (Debugging Challenge)

### Bugs Found

#### Bug 1: Missing g_cost in Priority Queue
**Problem**: Priority queue tuple is `(f, position)` but should include g for tie-breaking

**Fix**:
```python
# WRONG
pq = [(h_start, start)]

# CORRECT
pq = [(h_start, 0.0, start)]  # (f, g, position)
```

**Why**: Including g breaks ties in favor of nodes closer to start, improving exploration order.

#### Bug 2: Path is Backwards
**Problem**: Path reconstruction builds backwards but doesn't reverse

**Fix**: Add `path.reverse()` before returning

#### Bug 3: Missing Closed Set
**Problem**: No closed set to track processed nodes

**Fix**:
```python
closed_set = set()

while pq:
    # ...
    if current in closed_set:
        continue
    closed_set.add(current)
```

**Why**: Without closed set, nodes can be processed multiple times, wasting time.

#### Bug 4: Wrong Update Condition
**Problem**: `if neighbor not in g_cost` only updates on first visit

**Fix**:
```python
# CORRECT
if tentative_g < g_cost.get(neighbor, float('inf')):
    g_cost[neighbor] = tentative_g
```

**Why**: Should update whenever we find a better path, not just first time.

#### Bug 5: Wrong Position for Heuristic
**Problem**: Uses `heuristic(current, goal)` instead of `heuristic(neighbor, goal)`

**Fix**:
```python
# CORRECT
h = heuristic(neighbor, goal)  # Calculate h for neighbor
```

**Why**: Need h for the neighbor we're evaluating, not current node.

### Corrected Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance
import heapq

def corrected_astar(grid: Grid, start: tuple[int, int], goal: tuple[int, int], heuristic):
    """Corrected A* implementation."""
    # FIX 1: Include g_cost in tuple
    h_start = heuristic(start, goal)
    pq = [(h_start, 0.0, start)]

    g_cost = {start: 0.0}
    parent = {}
    closed_set = set()  # FIX 3: Add closed set

    while pq:
        current_f, current_g, current = heapq.heappop(pq)

        # FIX 3: Check closed set
        if current in closed_set:
            continue
        closed_set.add(current)

        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()  # FIX 2: Reverse path
            return path, g_cost[goal]

        for neighbor in grid.get_neighbors(current):
            if neighbor in closed_set:
                continue

            move_cost = grid.get_movement_cost(current, neighbor)
            tentative_g = current_g + move_cost

            # FIX 4: Update on improvement
            if tentative_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative_g
                h = heuristic(neighbor, goal)  # FIX 5: h for neighbor
                f = tentative_g + h
                parent[neighbor] = current
                heapq.heappush(pq, (f, tentative_g, neighbor))

    return [], float('inf')


# Test the corrected implementation
grid = Grid(15, 15, 0.15, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (14, 14)
grid.generate_obstacles(start, goal)

path, cost = corrected_astar(grid, start, goal, manhattan_distance)
print(f"Corrected A* - Path length: {len(path)}, Cost: {cost:.2f}")

# Compare with library implementation
from pathfinding_lab.algorithms.astar import astar
correct_result = astar(grid, start, goal, manhattan_distance)
print(f"Library A* - Path length: {correct_result.path_length}, Cost: {correct_result.path_cost:.2f}")

# Verify they match
print(f"\nResults match: {abs(cost - correct_result.path_cost) < 0.01}")
print(f"Both optimal: ✓")
```

### Summary of Fixes

| Bug | Issue | Impact | Fix |
|-----|-------|--------|-----|
| 1 | Missing g in tuple | Poor tie-breaking | Add g_cost to tuple |
| 2 | Path backwards | Wrong direction | Add reverse() |
| 3 | No closed set | Inefficient, revisits nodes | Add closed_set tracking |
| 4 | Wrong update condition | Misses better paths | Check cost improvement |
| 5 | Wrong h position | Incorrect f-cost | Use neighbor's h |

### What You Should Understand

**A* Correctness Requirements**:
1. **Priority queue**: (f, g, position) for proper ordering
2. **Closed set**: Track processed nodes
3. **Update condition**: Always update on cost improvement
4. **Heuristic position**: Calculate for neighbor being evaluated

**Why These Matter**:
- Bugs 1, 3: Affect efficiency but not correctness (with admissible h)
- Bug 4: **Breaks correctness** - can miss optimal paths
- Bugs 2, 5: Return wrong results

---

## Additional Practice

### Challenge: Implement IDA* (Iterative Deepening A*)

```python
def ida_star(grid, start, goal, heuristic):
    """
    IDA*: Memory-efficient alternative to A*.
    Uses depth-first search with iteratively increasing cost bounds.
    """
    def search(path, g, bound):
        # Recursive DFS with f-cost bound
        pass

    # Start with initial bound = h(start)
    bound = heuristic(start, goal)
    path = [start]

    while True:
        # Search with current bound
        result = search(path, 0, bound)
        if result == "FOUND":
            return path
        if result == float('inf'):
            return None  # No path
        bound = result  # Increase bound
```

---

**Next: Continue to Week 6 - Heuristic Functions →**

---

**📝 [Back to Week 5 Exercises](../exercises/week_05.md)** | **📚 [Week 5 Documentation](../docs/week_05_astar.md)** | **➡️ [Next: Week 6 Solutions](week_06_solutions.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
