# Week 5: A* Search Algorithm

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 4](week_04_dijkstra.md)** | **📝 [Week 5 Exercises](../exercises/week_05.md)** | **✅ [Week 5 Solutions](../solutions/week_05_solutions.md)** | **🔬 [Notebook](../notebooks/03_dijkstra_astar.ipynb)** | **➡️ [Next: Week 6](week_06_heuristics.md)**

---

## 📋 Before You Start

> **🧭 Pipeline:** This week adds **box 5** to the [end-to-end pipeline](END_TO_END_PIPELINE.md) — A* and Greedy, adding heuristic-guided search.

**What you should already know** (each links to where to learn or revisit it):

- Dijkstra and priority queues — [Week 4](week_04_dijkstra.md).
- `heapq` and `float('inf')` — [Week 0 §8](week_00_python_prerequisites.md#prereq-deque-heapq-inf).
- Reading `Callable[[Position, Position], float]` (a heuristic is a *function*) — [Week 0 §7](week_00_python_prerequisites.md#prereq-typehints).
- Tuples & dicts for tracking costs — [Week 0 §1–§2](week_00_python_prerequisites.md#prereq-tuples).

---

## Learning Goals

By the end of this week, you will:
- Understand how A* combines Dijkstra's with heuristics
- Implement and use different heuristic functions
- Learn what makes a heuristic "admissible" and "consistent"
- Understand why A* is faster than Dijkstra's
- Master the f(n) = g(n) + h(n) formula

## Theory

### The Problem with Dijkstra's

**Dijkstra's is optimal but blind**: It explores in all directions equally, visiting many nodes that are clearly moving away from the goal.

**Example**: Finding path from (0,0) to (10,10)
- Dijkstra's explores nodes at (0,5) even though they're perpendicular to the goal
- This wastes time on unpromising paths

**Solution**: Use a **heuristic** to guide the search toward the goal!

### Introducing A* Search

**A* Search** extends Dijkstra's by using a heuristic function to estimate the remaining distance to the goal. It's the most popular pathfinding algorithm in games, robotics, and GPS navigation.

**Key Formula**:
```
f(n) = g(n) + h(n)

where:
- g(n) = actual cost from start to node n
- h(n) = estimated cost from node n to goal (heuristic)
- f(n) = estimated total cost of path through n
```

**Key Characteristics**:
- Uses priority queue ordered by f(n) = g(n) + h(n)
- Explores nodes that appear closest to goal first
- **Guarantees optimal path** (with admissible heuristic)
- Much faster than Dijkstra's on average

### How A* Works

**Algorithm Steps**:
1. Start with priority queue containing start at f = h(start)
2. Pop node with lowest f-cost
3. If goal, reconstruct and return path
4. For each neighbor:
   - Calculate g = current_g + edge_cost
   - Calculate h = heuristic(neighbor, goal)
   - Calculate f = g + h
   - If better path, update and add to queue

**Why It's Faster**:
A* focuses exploration toward the goal, visiting fewer nodes than Dijkstra's while still guaranteeing optimality.

### Heuristic Functions

**Manhattan Distance** (L1):
```python
def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
```
- Best for 4-directional movement
- Admissible: never overestimates

**Euclidean Distance** (L2):
```python
import math
def euclidean(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx*dx + dy*dy)
```
- Best for straight-line distance
- Admissible: never overestimates

**Chebyshev Distance** (L∞):
```python
def chebyshev(pos1, pos2):
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))
```
- Best for 8-directional movement with equal diagonal cost
- Admissible when diagonals cost same as orthogonal

**Octile Distance**:
```python
def octile(pos1, pos2):
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
```
- Best for 8-directional with proper diagonal costs
- Admissible: accounts for diagonal cost of √2

### Admissible Heuristics

**Definition**: A heuristic h(n) is **admissible** if it never overestimates the true cost to the goal.

**Mathematical**:
```
h(n) ≤ h*(n)  for all n

where h*(n) is the true optimal cost from n to goal
```

**Why It Matters**: A* with an admissible heuristic **guarantees** finding the optimal path.

**Examples**:
- ✅ Manhattan on 4-directional grid: admissible
- ✅ Euclidean on any grid: admissible (straight line is shortest)
- ❌ 2 × Manhattan: NOT admissible (overestimates)
- ❌ Random values: NOT admissible

### Consistent Heuristics

**Definition**: A heuristic is **consistent** (monotone) if:
```
h(n) ≤ cost(n, n') + h(n')

For all neighbors n' of n
```

**Triangle Inequality**: The heuristic respects the triangle inequality.

**Why It Matters**: Consistent heuristics are admissible AND prevent reopening nodes, making A* more efficient.

**All standard heuristics are consistent**: Manhattan, Euclidean, Chebyshev, Octile.

### A* vs Dijkstra's vs Greedy Best-First

| Feature | Dijkstra's | A* | Greedy Best-First |
|---------|------------|----|--------------------|
| **Priority** | g(n) | g(n) + h(n) | h(n) |
| **Optimal** | ✅ Yes | ✅ Yes (if h admissible) | ❌ No |
| **Nodes Visited** | Many | Fewer | Fewest |
| **Use Heuristic** | ❌ No | ✅ Yes | ✅ Yes |
| **Speed** | Slow | Fast | Fastest (but not optimal) |

**Key Insight**: A* is Dijkstra's guided by a heuristic!

## Build the Intuition: Why `f = g + h` Orders Exploration Sensibly

Trace A* **by hand** on the simplest possible map: three cells in a line, 4-directional, every
move costs 1.

```text
[S]---[M]---[G]
(0,0) (0,1) (0,2)
```

Use **Manhattan distance** to the goal as the heuristic `h`:

- `h(S) = |0-0| + |0-2| = 2`
- `h(M) = 1`
- `h(G) = 0`

Remember the three quantities: `g` = real cost from the start, `h` = *estimated* remaining cost
to the goal, and `f = g + h` = estimated total cost of a path going through this cell. A* always
expands the smallest `f` first.

| Step | Pop (lowest `f`) | `g` | `h` | `f = g + h` | Push neighbors |
| --- | --- | --- | --- | --- | --- |
| 1 | `S` | 0 | 2 | **2** | `M`: g=1, h=1, f=2 |
| 2 | `M` | 1 | 1 | **2** | `G`: g=2, h=0, f=2 |
| 3 | `G` | 2 | 0 | **2** | goal reached, cost 2 |

Notice `f` stays **2** the whole way down the optimal path. That is the point: `g` rises by 1 at
each step while `h` falls by 1, so their sum tracks the *true* total cost of the best route. Now
imagine a detour cell `U = (1,0)` hanging off the line. It has `g(U) = 1` but
`h(U) = |1-0| + |0-2| = 3`, giving `f(U) = 4`. Because `4 > 2`, A* explores `U` **last** — the
heuristic correctly tells A* that `U` leads away from the goal. Dijkstra, using only `g`, would
have treated `U` and `M` as equally promising (both `g = 1`).

### True Cost `h*` and Admissibility

Define **`h*(n)`** as the *true* optimal remaining cost from `n` to the goal. On our line,
`h*(S) = 2` and `h*(M) = 1` — here Manhattan equals `h*` exactly.

A heuristic is **admissible** when it **never overestimates**: `h(n) ≤ h*(n)` for every cell.
Admissibility is what guarantees A* returns an optimal path.

**A concrete over-estimate that breaks optimality.** Suppose we cheated and set `h(M) = 10`
(way above its true cost of 1). Then `f(M) = g + h = 1 + 10 = 11`. A* would now treat the one
cell on the only optimal path as terrible and avoid it, expanding every *other* cell first. If
any longer route happened to have a smaller `f`, A* would return that longer route — a
**sub-optimal** answer. This is exactly why heuristics like Manhattan (which underestimate or
match `h*`) are safe, while inflated heuristics are not. Keep this trace in mind as you read the
implementation below.

## Code Walkthrough

### A* Implementation (`src/pathfinding_lab/algorithms/astar.py`)

#### 1. Initialization

```python
import heapq

# Initial f-cost: g(start) = 0, h(start) = heuristic(start, goal)
h_start = heuristic(start, goal)
pq = [(h_start, 0.0, start)]  # (f_cost, g_cost, position)

g_cost = {start: 0.0}  # Best known g-cost
parent = {}
closed_set = set()  # Already processed nodes
```

**Key Points**:
- Priority queue stores `(f, g, position)` tuples
- Include g to break ties (prefer nodes closer to start)
- Track g_cost separately for path reconstruction

#### 2. Main A* Loop

```python
while pq:
    f, current_g, current = heapq.heappop(pq)

    # Skip if already processed
    if current in closed_set:
        continue

    closed_set.add(current)
    visited_order.append(current)

    if current == goal:
        return reconstruct_path(...)

    # Explore neighbors
    for neighbor in grid.get_neighbors(current):
        if neighbor in closed_set:
            continue

        # Calculate costs
        move_cost = grid.get_movement_cost(current, neighbor)
        tentative_g = current_g + move_cost

        # Update if better path
        if tentative_g < g_cost.get(neighbor, float('inf')):
            g_cost[neighbor] = tentative_g
            h = heuristic(neighbor, goal)
            f_cost = tentative_g + h
            parent[neighbor] = current
            heapq.heappush(pq, (f_cost, tentative_g, neighbor))
```

**Process**:
1. Pop lowest f-cost node
2. Skip if already in closed set
3. Check for goal
4. For each neighbor: calculate g, h, f and update if improved

#### 3. Choosing the Right Heuristic

**For 4-directional grids**:
```python
from pathfinding_lab.heuristics.manhattan import manhattan_distance
result = astar(grid, start, goal, manhattan_distance)
```

**For 8-directional grids**:
```python
from pathfinding_lab.heuristics.octile import octile_distance
result = astar(grid, start, goal, octile_distance)
```

**For any grid (always works)**:
```python
from pathfinding_lab.heuristics.euclidean import euclidean_distance
result = astar(grid, start, goal, euclidean_distance)
```

## Common Mistakes

### 1. Using Non-Admissible Heuristic

**Problem**: Overestimating the cost breaks optimality guarantee
```python
# WRONG - overestimates!
def bad_heuristic(pos, goal):
    return 10 * manhattan_distance(pos, goal)  # 10x too large!
```

**Solution**: Always underestimate or be exact
```python
# CORRECT
def good_heuristic(pos, goal):
    return manhattan_distance(pos, goal)  # Never overestimates
```

### 2. Forgetting to Calculate h for Each Neighbor

**Problem**: Reusing old h values
```python
# WRONG
h = heuristic(current, goal)  # Calculate once
for neighbor in grid.get_neighbors(current):
    f = g + h  # Using current's h for neighbor!
```

**Solution**: Calculate h for each neighbor
```python
# CORRECT
for neighbor in grid.get_neighbors(current):
    h = heuristic(neighbor, goal)  # Calculate for each neighbor
    f = g + h
```

### 3. Wrong Heuristic for Movement Mode

**Problem**: Using Manhattan on 8-directional grid underestimates diagonals
```python
# SUBOPTIMAL - Manhattan underestimates on 8-directional
grid = Grid(10, 10, 0.1, MovementMode.EIGHT_DIRECTIONAL)
result = astar(grid, start, goal, manhattan_distance)
# Still optimal but explores more nodes than necessary
```

**Solution**: Match heuristic to movement mode
```python
# BETTER
result = astar(grid, start, goal, octile_distance)  # Octile for 8-dir
```

### 4. Not Skipping Closed Nodes

**Problem**: Revisiting already-processed nodes
```python
# INEFFICIENT
for neighbor in grid.get_neighbors(current):
    # No check, might re-add closed nodes
    heappush(pq, (f, g, neighbor))
```

**Solution**: Skip closed nodes
```python
# EFFICIENT
for neighbor in grid.get_neighbors(current):
    if neighbor in closed_set:
        continue  # Skip already-processed nodes
    heappush(pq, (f, g, neighbor))
```

### 5. Confusing g and f Costs

**Problem**: Using f-cost instead of g-cost for path reconstruction
```python
# WRONG - f is estimate, not actual cost
return SearchResult(path_cost=f_cost[goal])  # Includes heuristic!
```

**Solution**: Use g-cost for actual path cost
```python
# CORRECT
return SearchResult(path_cost=g_cost[goal])  # Actual cost
```

## Mini Project Task

### Task: Compare A* with Different Heuristics

Implement a comparison tool that runs A* with Manhattan, Euclidean, and Octile heuristics, analyzing performance differences.

**Requirements**:
1. Run A* with 3 different heuristics on same grid
2. Compare nodes visited and runtime
3. Verify all find optimal paths
4. Analyze which is fastest for different movement modes

**Starter Code**:
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.heuristics.euclidean import euclidean_distance
from pathfinding_lab.heuristics.octile import octile_distance

# Create test grid
grid = Grid(30, 30, 0.15, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (29, 29)
grid.generate_obstacles(start, goal)

# Test each heuristic
heuristics = {
    "Manhattan": manhattan_distance,
    "Euclidean": euclidean_distance,
    "Octile": octile_distance
}

print("=== A* Heuristic Comparison ===\n")
for name, heuristic in heuristics.items():
    result = astar(grid, start, goal, heuristic)

    print(f"{name} Heuristic:")
    print(f"  Path length: {result.path_length}")
    print(f"  Path cost: {result.path_cost:.2f}")
    print(f"  Nodes visited: {result.nodes_visited}")
    print(f"  Runtime: {result.runtime_ms:.2f}ms")
    print()
```

### Success Criteria

- ✅ All heuristics find paths with same cost (optimal)
- ✅ Octile visits fewest nodes on 8-directional
- ✅ Manhattan works but less efficient on 8-directional
- ✅ Understand trade-offs between heuristics

## Reflection Questions

1. **Why does A* with an admissible heuristic guarantee optimal paths?**
   - Hint: Think about when nodes are expanded

2. **What's the difference between admissible and consistent heuristics?**
   - Consider: Can a heuristic be admissible but not consistent?

3. **When would you use Dijkstra's instead of A*?**
   - Think about: Cost of computing heuristic, multiple goals

4. **Why does A* visit fewer nodes than Dijkstra's?**
   - Consider: How the heuristic guides the search

5. **What happens if you use h(n) = 0 for all n in A*?**
   - Think about: What algorithm does this become?

## Practical Applications

### Real-World Uses of A*

1. **Video Games**: NPC pathfinding (most popular choice)
2. **GPS Navigation**: Route planning with traffic estimates
3. **Robotics**: Mobile robot navigation
4. **Puzzle Solving**: Solving sliding puzzles, Rubik's cube

### When A* Excels

- Single source, single goal pathfinding
- Good heuristic available
- Optimal path required
- Moderate graph size

### When to Use Alternatives

- **No good heuristic**: Use Dijkstra's
- **Many goals**: Use Dijkstra's or Bidirectional search
- **Huge graphs**: Consider Hierarchical pathfinding
- **Dynamic environments**: Use D* Lite or Anytime algorithms

## Additional Resources

- [Red Blob Games - A* Introduction](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [A* Visualization](https://qiao.github.io/PathFinding.js/visual/)
- [Understanding Heuristics](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html)
- [A* Variants and Optimizations](https://en.wikipedia.org/wiki/A*_search_algorithm)

## Next Week Preview

Next week, we'll dive deep into **Heuristic Functions**, learning:
- How to design custom heuristics
- Weighted heuristics for speed vs optimality trade-offs
- Tie-breaking strategies
- When and how to combine heuristics

**Preparation**: Make sure you understand:
- How A* uses f(n) = g(n) + h(n)
- What makes a heuristic admissible
- Why the heuristic choice affects performance

---

**Continue to Week 6: Heuristic Functions →**

---

## End-to-End Pipeline Connection

A* turns the pathfinding product from exhaustive weighted search into guided search:

```text
Grid + start + goal + heuristic → A* → SearchResult → visualization + comparison metrics
```

The grid still provides legal movement and real costs. The heuristic adds an estimate of how far a candidate cell is from the goal.

### Understanding g, h, and f in the Pipeline

A* chooses what to explore using three values:

- `g`: real cost from start to the current cell
- `h`: estimated cost from the current cell to the goal
- `f`: combined priority, usually `g + h`

Dijkstra only uses `g`. Greedy Best-First mostly trusts `h`. A* balances both.

### What the UI Should Help You See

When A* works well, the visited region usually points toward the goal instead of expanding evenly in all directions. When the heuristic is weak, A* behaves more like Dijkstra. When the heuristic is too aggressive, it may become faster but risk path quality depending on the variant.

Visualization is therefore not decoration; it is the easiest way to understand heuristic quality.

### Step-by-Step Debugging

For a small grid, trace A* manually:

1. Put the start in the open set.
2. Compute its heuristic to the goal.
3. Pop the cell with the lowest `f` value.
4. Add valid neighbors from the grid.
5. Update a neighbor only if the new `g` cost is better.
6. Stop when the goal is popped or no candidates remain.
7. Reconstruct the path from parent links.

If your output is wrong, check whether the bug is in real costs, heuristic values, priority ordering, or path reconstruction.

### Week 5 Build Checkpoint

You are ready for Week 6 when you can run A* with a heuristic, explain why it visits fewer cells than Dijkstra on many maps, and identify which part of the result proves that improvement.
