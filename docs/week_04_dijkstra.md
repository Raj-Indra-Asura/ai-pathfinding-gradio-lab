# Week 4: Dijkstra's Algorithm

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 3](week_03_bfs_dfs.md)** | **📝 [Week 4 Exercises](../exercises/week_04.md)** | **✅ [Week 4 Solutions](../solutions/week_04_solutions.md)** | **🔬 [Notebook](../notebooks/03_dijkstra_astar.ipynb)** | **➡️ [Next: Week 5](week_05_astar.md)**

---

## 📋 Before You Start

> **🧭 Pipeline:** This week adds **box 4** to the [end-to-end pipeline](END_TO_END_PIPELINE.md) — Dijkstra, adding movement-cost awareness.

**What you should already know** (each links to where to learn or revisit it):

- BFS/DFS from last week — [Week 3](week_03_bfs_dfs.md).
- `heapq` (priority queue) and `float('inf')` — [Week 0 §8](week_00_python_prerequisites.md#prereq-deque-heapq-inf).
- Dicts for `cost_so_far`, tuples as keys — [Week 0 §1–§2](week_00_python_prerequisites.md#prereq-tuples).
- Why a priority queue needs ordering (`__lt__`) — [Week 0 §5](week_00_python_prerequisites.md#prereq-dunder).

---

## Learning Goals

By the end of this week, you will:
- Understand weighted pathfinding and why BFS isn't enough
- Implement Dijkstra's algorithm with a priority queue
- Learn when Dijkstra's algorithm is optimal
- Understand the difference between BFS and Dijkstra's
- Use heapq for efficient priority queue operations

## Theory

### Why BFS Isn't Always Enough

**Problem with BFS**: BFS finds the shortest path in terms of *number of steps*, but what if different moves have different costs?

**Example Scenario**:
- Moving through grass: cost = 1
- Moving through swamp: cost = 5
- Moving through road: cost = 0.5

BFS treats all moves equally, but in the real world, we care about *total cost*, not just *number of steps*.

### Introducing Dijkstra's Algorithm

**Dijkstra's Algorithm** finds the shortest path considering edge weights (movement costs). It's the gold standard for single-source shortest path on graphs with non-negative weights.

**Key Idea**: Explore nodes in order of increasing cost from the start. Always expand the lowest-cost unexplored node next.

**Key Characteristics**:
- Uses a **priority queue** (min-heap)
- Explores in order of cost from start
- **Guarantees optimal path** (with non-negative weights)
- More general than BFS (BFS is Dijkstra's with all weights = 1)

### How It Works

**Algorithm Steps**:
1. Start with priority queue containing start position at cost 0
2. Track the best known cost to reach each position
3. While priority queue is not empty:
   - Pop the position with lowest cost
   - If it's the goal, we found the optimal path!
   - For each neighbor:
     - Calculate new cost: current cost + edge cost
     - If new cost is better than known cost, update and add to queue
     - Track parent for path reconstruction

**Why It's Optimal**:
Because we always expand the lowest-cost node first, when we reach the goal, we know we've found the cheapest path. Any other path would have required expanding a more expensive node.

### Dijkstra's vs BFS

| Feature | BFS | Dijkstra's |
|---------|-----|-----------|
| **Data Structure** | Queue (FIFO) | Priority Queue (min-heap) |
| **Expansion Order** | Distance from start | Cost from start |
| **Edge Weights** | Unweighted (all = 1) | Weighted (any ≥ 0) |
| **Shortest Path** | ✅ By steps | ✅ By cost |
| **Time Complexity** | O(V + E) | O((V + E) log V) |
| **Use Cases** | Equal-cost moves | Different movement costs |

**Key Insight**: BFS is Dijkstra's algorithm where all edges have weight 1!

### Priority Queue (Heap)

**What is a Priority Queue?**
A data structure where elements are removed in order of priority (lowest cost first).

**Python's heapq**:
- `heappush(heap, item)`: Add item (O(log n))
- `heappop(heap)`: Remove and return smallest item (O(log n))
- Stores tuples: `(priority, data)`

**Why It Matters**:
- Regular queue (BFS): Explores by distance
- Priority queue (Dijkstra's): Explores by cost
- This difference makes Dijkstra's optimal for weighted graphs

## Build the Intuition: Why a Node Lands in the Heap Twice

Before reading the code, trace a tiny example **by hand**. Forget grids for a moment and use
four nodes **S, A, B, G** with these one-way move costs:

```text
S → A = 4
S → B = 1
B → A = 1
A → G = 1
```

We track `cost_so_far` (best cost known to reach each node). Every node starts at
**`float('inf')`**, which simply means **"not reached yet"** — any real cost is smaller, so the
first real path always wins the comparison `new_cost < cost_so_far[node]`.

| Step | Pop from heap | Action | Heap afterwards | `cost_so_far` |
| --- | --- | --- | --- | --- |
| 1 | — (start) | push `(0, S)` | `[(0,S)]` | `S:0` |
| 2 | `(0, S)` | S→A: `0+4=4` push `(4, A)`; S→B: `0+1=1` push `(1, B)` | `[(1,B), (4,A)]` | `S:0, A:4, B:1` |
| 3 | `(1, B)` | B→A: `1+1=2` **< 4**, so update A and push `(2, A)` | `[(2,A), (4,A)]` | `S:0, A:2, B:1` |
| 4 | `(2, A)` | A→G: `2+1=3` push `(3, G)` | `[(3,G), (4,A)]` | `…, A:2, G:3` |
| 5 | `(3, G)` | G is the goal → done (cost 3) | `[(4,A)]` | — |

Look at step 3: **A is now in the heap twice — once at cost 4, once at cost 2.** That is normal.
Dijkstra never edits or deletes old heap entries (that would be slow); it just pushes a new,
cheaper one. The cheaper copy `(2, A)` sits *above* the stale `(4, A)` because the heap always
keeps the smallest on top.

**Why the skip-check is correct.** Because the heap pops smallest-first, we always pop the
*cheapest* copy `(2, A)` before the stale `(4, A)`. By the time the stale `(4, A)` would be
popped, `cost_so_far[A]` is already `2`, so:

```python
if current_cost > cost_so_far.get(current, float('inf')):
    continue   # 4 > 2  → skip this stale entry, we already did better
```

The skip-check throws away outdated entries safely. It can never skip a *useful* entry, because
the first time we pop a node it carries that node's best possible cost (that is the heart of why
Dijkstra is optimal). Keep this trace in mind while reading the real code below.

## Code Walkthrough

### Dijkstra's Implementation (`src/pathfinding_lab/algorithms/dijkstra.py`)

Let's examine the key parts:

#### 1. Initialization

```python
import heapq

# Priority queue: (cost, position)
pq = [(0.0, start)]
cost_so_far = {start: 0.0}  # Best known cost to each position
parent = {}                  # For path reconstruction
visited_order = []           # Track exploration order
```

**Key Points**:
- Priority queue stores `(cost, position)` tuples
- `cost_so_far` tracks the best cost found to reach each position
- Costs are floats to handle fractional movement costs

#### 2. Main Dijkstra Loop

```python
while pq:
    current_cost, current = heapq.heappop(pq)  # Get lowest-cost node

    # Skip if we've already found a better path to this node
    if current_cost > cost_so_far.get(current, float('inf')):
        continue

    visited_order.append(current)

    # Goal check
    if current == goal:
        path = _reconstruct_path(parent, start, goal)
        return SearchResult(...)

    # Explore neighbors
    for neighbor in grid.get_neighbors(current):
        # Calculate cost via current node
        move_cost = grid.get_movement_cost(current, neighbor)
        new_cost = current_cost + move_cost

        # If this path is better, update
        if new_cost < cost_so_far.get(neighbor, float('inf')):
            cost_so_far[neighbor] = new_cost
            parent[neighbor] = current
            heapq.heappush(pq, (new_cost, neighbor))
```

**Process**:
1. **Pop lowest-cost node**: `heappop` gives us the cheapest unexplored option
2. **Skip if outdated**: Due to duplicates in heap, check if we've found better path
3. **Goal check**: When we reach goal, we have the optimal path!
4. **Update neighbors**: If we found a cheaper path, update cost and add to queue

#### 3. Why Skip Outdated Nodes?

**Problem**: We can add the same position to the priority queue multiple times with different costs.

**Example**:
```python
# First path to (1,1): cost = 10
heappush(pq, (10, (1,1)))

# Later, better path to (1,1): cost = 5
heappush(pq, (5, (1,1)))

# Both entries exist in the queue!
# We want to skip the outdated (10, (1,1)) entry
```

**Solution**:
```python
if current_cost > cost_so_far.get(current, float('inf')):
    continue  # Skip outdated entry
```

#### 4. Movement Cost Calculation

```python
move_cost = grid.get_movement_cost(current, neighbor)
```

**What affects movement cost?**
- Base movement (1.0 for orthogonal, √2 for diagonal)
- Terrain type (if implemented)
- Grid-specific weights

For basic grids:
- 4-directional: all moves cost 1.0
- 8-directional: orthogonal = 1.0, diagonal = √2 ≈ 1.414

## Common Mistakes

### 1. Using a Regular List Instead of Heapq

**Problem**: Manually sorting is slow!
```python
# WRONG - O(n log n) every iteration
queue = [(0, start)]
while queue:
    queue.sort()  # Expensive!
    cost, current = queue.pop(0)
```

**Solution**: Use `heapq` for O(log n) operations
```python
# CORRECT
import heapq
pq = [(0, start)]
while pq:
    cost, current = heapq.heappop(pq)  # O(log n)
```

### 2. Forgetting the Outdated Node Check

**Problem**: Processing the same node multiple times wastes time
```python
# WRONG - no duplicate check
while pq:
    current_cost, current = heapq.heappop(pq)
    # Process node even if we found a better path already
```

**Solution**: Skip outdated entries
```python
# CORRECT
while pq:
    current_cost, current = heapq.heappop(pq)
    if current_cost > cost_so_far.get(current, float('inf')):
        continue  # Skip outdated entry
```

### 3. Not Updating cost_so_far Before Adding to Queue

**Problem**: Infinite loops or incorrect results
```python
# WRONG - check happens before update
if new_cost < cost_so_far.get(neighbor, float('inf')):
    heapq.heappush(pq, (new_cost, neighbor))
    cost_so_far[neighbor] = new_cost  # Too late!
```

**Solution**: Update `cost_so_far` immediately
```python
# CORRECT
if new_cost < cost_so_far.get(neighbor, float('inf')):
    cost_so_far[neighbor] = new_cost  # Update first
    parent[neighbor] = current
    heapq.heappush(pq, (new_cost, neighbor))
```

### 4. Using Dijkstra's with Negative Weights

**Problem**: Dijkstra's algorithm **does not work** with negative edge weights!

**Why**: Once a node is popped from the priority queue, Dijkstra's assumes we've found the optimal path to it. Negative weights can invalidate this assumption.

**Example**:
```
Start -> A: cost = 5
Start -> B -> A: cost = 10 + (-8) = 2  # Better, but found later!
```

**Solution**: Use **Bellman-Ford** algorithm for graphs with negative weights (not covered in this course).

### 5. Comparing Dijkstra's to BFS on Unweighted Graphs

**Problem**: Using Dijkstra's when BFS would work

**When all weights are equal (or weight = 1)**:
- BFS: O(V + E)
- Dijkstra's: O((V + E) log V)

**Solution**: Use BFS for unweighted graphs—it's faster and simpler!

## Mini Project Task

### Task: Implement Weighted Grid Movement

Create a grid where different terrain types have different movement costs, then compare how BFS and Dijkstra's perform.

**Requirements**:
1. Create a 20x20 grid with three terrain types:
   - **Grass** (70%): cost = 1.0
   - **Swamp** (20%): cost = 3.0
   - **Road** (10%): cost = 0.5
2. Run BFS and Dijkstra's from (0,0) to (19,19)
3. Compare:
   - Path lengths (number of steps)
   - Path costs (total movement cost)
   - Which finds the cheaper path?

**Starter Code**:
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dijkstra import dijkstra
import random

# Create weighted grid (you'll need to extend Grid class or track terrain separately)
grid = Grid(20, 20, 0.0, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (19, 19)

# For this exercise, assume equal weights (all = 1.0)
# In a real implementation, you'd modify Grid to support terrain types

# Run both algorithms
bfs_result = bfs(grid, start, goal)
dijkstra_result = dijkstra(grid, start, goal)

print("BFS Results:")
print(f"  Path length: {bfs_result.path_length} steps")
print(f"  Path cost: {bfs_result.path_cost:.2f}")
print(f"  Nodes visited: {bfs_result.nodes_visited}")

print("\nDijkstra's Results:")
print(f"  Path length: {dijkstra_result.path_length} steps")
print(f"  Path cost: {dijkstra_result.path_cost:.2f}")
print(f"  Nodes visited: {dijkstra_result.nodes_visited}")

print("\nComparison:")
print(f"  Same path? {bfs_result.path == dijkstra_result.path}")
print(f"  Cost difference: {abs(bfs_result.path_cost - dijkstra_result.path_cost):.2f}")
```

### Success Criteria

- ✅ Both algorithms find a path
- ✅ With equal weights, both find the same cost
- ✅ Understand why Dijkstra's is needed for weighted graphs
- ✅ Can explain the difference in exploration order

### Challenge Extension

Modify the grid to have actual terrain weights and observe how Dijkstra's finds cheaper paths than BFS by avoiding expensive terrain!

## Reflection Questions

1. **Why does Dijkstra's algorithm guarantee the optimal path?**
   - Hint: Think about the order in which nodes are explored

2. **When would you use BFS instead of Dijkstra's?**
   - Consider: Performance, simplicity, problem requirements

3. **What happens if you use Dijkstra's on a graph with negative weights?**
   - Think about: The optimality assumption, when can it break?

4. **How is the priority queue critical to Dijkstra's correctness?**
   - Consider: What if we used a regular queue or stack?

5. **Why do we need the "skip outdated nodes" check?**
   - Think about: Duplicate entries in the priority queue

## Practical Applications

### Real-World Uses of Dijkstra's

1. **GPS Navigation**: Finding shortest routes with different road speeds
2. **Network Routing**: Finding optimal packet routes (OSPF protocol)
3. **Robotics**: Path planning with varied terrain costs
4. **Game AI**: NPC pathfinding in games with movement penalties

### When Dijkstra's Falls Short

- **Large graphs**: Can be slow; consider A* with heuristics (next week!)
- **Negative weights**: Use Bellman-Ford instead
- **Changing graphs**: Need dynamic algorithms (D* Lite)

## Additional Resources

- [Red Blob Games - Dijkstra's Implementation](https://www.redblobgames.com/pathfinding/a-star/introduction.html#dijkstra)
- [Visualizing Dijkstra's Algorithm](https://visualgo.net/en/sssp)
- [Priority Queue Data Structure](https://docs.python.org/3/library/heapq.html)
- [Dijkstra's Algorithm Proof of Correctness](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/)

## Next Week Preview

Next week, we'll learn **A* Algorithm**, which combines Dijkstra's with heuristics for even faster pathfinding. You'll learn:
- How heuristics guide the search
- Manhattan and Euclidean distance heuristics
- Why A* is faster than Dijkstra's
- Admissible and consistent heuristics

**Preparation**: Make sure you understand:
- How Dijkstra's uses a priority queue
- Why Dijkstra's explores in order of cost
- Path reconstruction with parent pointers

---

**Continue to Week 5: A* Algorithm →**

---

## End-to-End Pipeline Connection

Dijkstra adds cost awareness to the project pipeline:

```text
Grid movement costs → priority queue → lowest-cost path → SearchResult.path_cost → UI metrics
```

Before this week, "best path" usually meant fewest steps. After this week, "best path" means lowest total cost.

### Cost Tracking Through the Product

The algorithm maintains a cost for each reached position. That cost eventually becomes part of the result and can be displayed in the UI or compared in benchmarks.

This is why path length and path cost must be treated as different metrics:

- Path length answers: "How many cells are in the route?"
- Path cost answers: "How expensive is the route according to movement rules?"

A longer route can be better if it avoids expensive cells.

### From BFS to Dijkstra to A*

Dijkstra is the bridge between uninformed and informed weighted search:

```text
BFS: queue ordered by discovery time
Dijkstra: priority queue ordered by real cost so far
A*: priority queue ordered by real cost + estimated remaining cost
```

Understanding this progression makes Week 5 much easier. A* is not magic; it is Dijkstra with a goal-directed estimate added to the priority.

### Movement Costs in Practice

Movement cost rules belong in the grid layer, not inside Dijkstra. That separation keeps the algorithm reusable. The same Dijkstra code can work with simple 4-directional movement, diagonal movement, or future terrain costs.

When debugging cost behavior, ask:

1. What cost does the grid report for this move?
2. Did Dijkstra update the position only when the new cost is lower?
3. Does the final `path_cost` equal the sum of the movement costs?

### Comparison Mindset

On an unweighted grid, BFS and Dijkstra should often agree on path length. On a weighted grid, Dijkstra should be trusted for optimal cost while BFS may still minimize only step count.

### Week 4 Build Checkpoint

You are ready for Week 5 when you can explain priority queues, cost-so-far tracking, and why Dijkstra may visit many cells even though it is optimal.
