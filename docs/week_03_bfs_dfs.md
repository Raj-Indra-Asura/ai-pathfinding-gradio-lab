# Week 3: BFS and DFS

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 2](week_02_grid_model.md)** | **📝 [Week 3 Exercises](../exercises/week_03.md)** | **✅ [Week 3 Solutions](../solutions/week_03_solutions.md)** | **🔬 [Notebook](../notebooks/02_bfs_dfs.ipynb)** | **➡️ [Next: Week 4](week_04_dijkstra.md)**

---

## Learning Goals

By the end of this week, you will:
- Understand Breadth-First Search (BFS) and Depth-First Search (DFS)
- Implement queue-based and stack-based exploration
- Learn when to use each algorithm
- Understand why BFS finds shortest paths
- Compare algorithm behavior on different grids

## Theory

### Introduction to Search Algorithms

**Search algorithms** systematically explore a grid to find a path from start to goal. The two fundamental uninformed search algorithms are:

1. **Breadth-First Search (BFS)**: Explores layer by layer
2. **Depth-First Search (DFS)**: Explores as deep as possible first

### Breadth-First Search (BFS)

BFS explores nodes level by level, like ripples expanding from a stone thrown in water.

**Key Characteristics**:
- Uses a **queue** (FIFO: First In, First Out)
- Explores all nodes at distance `k` before distance `k+1`
- **Guarantees shortest path** (in terms of number of steps)
- Optimal for unweighted grids

**Algorithm Steps**:
1. Start with a queue containing the start position
2. Mark start as visited
3. While queue is not empty:
   - Remove the front node (dequeue)
   - If it's the goal, reconstruct and return the path
   - Add all unvisited neighbors to the back of the queue
   - Mark them as visited

**Why BFS Finds Shortest Paths**:
Because BFS explores in order of distance from start, when it first reaches the goal, it has taken the minimum number of steps.

### Depth-First Search (DFS)

DFS explores as far as possible along each branch before backtracking.

**Key Characteristics**:
- Uses a **stack** (LIFO: Last In, First Out)
- Goes deep quickly, then backtracks
- **Does NOT guarantee shortest path**
- Uses less memory than BFS in some cases
- Good for maze generation, cycle detection

**Algorithm Steps**:
1. Start with a stack containing the start position
2. While stack is not empty:
   - Pop the top node
   - If already visited, skip it
   - Mark as visited
   - If it's the goal, reconstruct path
   - Push all unvisited neighbors onto the stack

**Why DFS Doesn't Find Shortest Paths**:
DFS might explore a long winding path to the goal before discovering a shorter direct path.

### Comparison

| Feature | BFS | DFS |
|---------|-----|-----|
| **Data Structure** | Queue | Stack |
| **Exploration** | Level by level | Depth first |
| **Shortest Path** | ✅ Yes | ❌ No |
| **Memory** | O(width) | O(depth) |
| **Use Cases** | Finding shortest path | Maze generation, topological sort |

## Code Walkthrough

### BFS Implementation (`src/pathfinding_lab/algorithms/bfs.py`)

Let's examine the key parts:

#### 1. Initialization

```python
from collections import deque

queue = deque([start])  # Queue for BFS
visited = {start}       # Track visited nodes
parent = {}             # Track parent for path reconstruction
visited_order = [start] # Track exploration order
```

**Key Points**:
- `deque` provides O(1) append and popleft operations
- `visited` is a set for O(1) lookup
- `parent` dictionary enables path reconstruction

#### 2. Main BFS Loop

```python
while queue:
    current = queue.popleft()  # FIFO: remove from front

    # Goal check
    if current == goal:
        path = _reconstruct_path(parent, start, goal)
        return SearchResult(...)

    # Explore neighbors
    for neighbor in grid.get_neighbors(current):
        if neighbor not in visited:
            visited.add(neighbor)
            parent[neighbor] = current
            queue.append(neighbor)  # Add to back
            visited_order.append(neighbor)
```

**Process**:
1. Remove from **front** of queue (oldest node)
2. Check if it's the goal
3. Add unvisited neighbors to **back** of queue (newer nodes)
4. This ensures level-by-level exploration

#### 3. Path Reconstruction

```python
def _reconstruct_path(parent, start, goal):
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path
```

**How it Works**:
- Start from goal, follow parent pointers back to start
- Build path backwards, then reverse it

### DFS Implementation (`src/pathfinding_lab/algorithms/dfs.py`)

#### Main Differences from BFS

```python
stack = [start]  # List used as stack
visited = set()  # Don't add start yet
parent = {}

while stack:
    current = stack.pop()  # LIFO: remove from end

    if current in visited:
        continue  # Skip if already visited

    visited.add(current)
    visited_order.append(current)

    # Goal check AFTER marking visited
    if current == goal:
        path = _reconstruct_path(parent, start, goal)
        return SearchResult(...)

    # Explore neighbors (reversed for left-to-right priority)
    neighbors = grid.get_neighbors(current)
    for neighbor in reversed(neighbors):
        if neighbor not in visited:
            if neighbor not in parent:
                parent[neighbor] = current
            stack.append(neighbor)
```

**Key Differences**:
1. Uses `pop()` not `popleft()` → LIFO behavior
2. Checks if visited BEFORE processing (DFS visits when popping)
3. Goal check after marking visited
4. Reverses neighbors for consistent exploration order

## Common Mistakes

### 1. Forgetting to Mark Nodes as Visited

**Problem**: Infinite loops or visiting same node multiple times
```python
# WRONG - no visited tracking
while queue:
    current = queue.popleft()
    for neighbor in grid.get_neighbors(current):
        queue.append(neighbor)  # Will revisit nodes!
```

**Solution**: Always track visited nodes
```python
# CORRECT
visited = {start}
while queue:
    current = queue.popleft()
    for neighbor in grid.get_neighbors(current):
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
```

### 2. Using List pop(0) for BFS

**Problem**: `list.pop(0)` is O(n) - very slow!
```python
# WRONG - inefficient
queue = [start]
current = queue.pop(0)  # O(n) operation
```

**Solution**: Use `collections.deque`
```python
# CORRECT - O(1) operation
from collections import deque
queue = deque([start])
current = queue.popleft()  # O(1) operation
```

### 3. Checking Goal Before Dequeue (BFS)

**Problem**: Can miss the goal if checked too early
```python
# WRONG
if current == goal:  # Before adding to queue
    queue.append(current)
```

**Solution**: Check after dequeuing
```python
# CORRECT
current = queue.popleft()
if current == goal:  # After dequeuing
    return path
```

### 4. Expecting DFS to Find Shortest Path

**Problem**: DFS explores deeply first and might miss shorter paths
```python
# DFS result: path length = 20
# BFS result: path length = 12
```

**Solution**: Use BFS when you need the shortest path!

## Mini Project Task

### Task: Visualize BFS vs DFS Exploration

Create a function that runs both BFS and DFS on the same grid and compares their exploration patterns.

**Requirements**:
1. Create a 15x15 grid with 15% obstacles
2. Run BFS from (0,0) to (14,14)
3. Run DFS from (0,0) to (14,14)
4. Compare:
   - Path lengths
   - Number of nodes visited
   - Runtime
   - Exploration patterns

**Starter Code**:
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dfs import dfs
from pathfinding_lab.visualization.grid_plot import create_grid_plot
import matplotlib.pyplot as plt

def compare_bfs_dfs():
    # Create grid
    grid = Grid(15, 15, 0.15, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
    start = (0, 0)
    goal = (14, 14)
    grid.generate_obstacles(start, goal)

    # Run both algorithms
    bfs_result = bfs(grid, start, goal)
    dfs_result = dfs(grid, start, goal)

    # Print comparison
    print("BFS Results:")
    print(f"  Path length: {bfs_result.path_length}")
    print(f"  Nodes visited: {bfs_result.nodes_visited}")
    print(f"  Runtime: {bfs_result.runtime_ms:.2f}ms")

    print("\nDFS Results:")
    print(f"  Path length: {dfs_result.path_length}")
    print(f"  Nodes visited: {dfs_result.nodes_visited}")
    print(f"  Runtime: {dfs_result.runtime_ms:.2f}ms")

    # Visualize both
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # TODO: Create visualizations

    plt.show()

compare_bfs_dfs()
```

### Success Criteria
- ✅ Both algorithms find a path (if one exists)
- ✅ BFS path is shorter or equal to DFS path
- ✅ Can visualize different exploration patterns
- ✅ Understand why they behave differently

## Reflection Questions

1. **Why does BFS guarantee the shortest path but DFS doesn't?**
   - Hint: Think about the order in which nodes are explored

2. **When might you prefer DFS over BFS?**
   - Consider: Memory usage, specific problem types

3. **What happens if there's no path to the goal?**
   - How does each algorithm handle this case?

4. **How would you modify BFS to work on weighted graphs?**
   - Preview: This leads to Dijkstra's algorithm next week!

5. **Why do we reverse the neighbors list in DFS?**
   - Think about: Stack order and exploration direction

## Additional Resources

- [Red Blob Games - Breadth First Search](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Visualizing BFS and DFS](https://visualgo.net/en/dfsbfs)
- [BFS vs DFS - When to Use Each](https://medium.com/basecs/breaking-down-breadth-first-search-cebe696709d9)
- [Queue vs Stack Data Structures](https://www.geeksforgeeks.org/difference-between-bfs-and-dfs/)

## Next Week Preview

Next week, we'll learn **Dijkstra's Algorithm**, which extends BFS to handle weighted graphs. You'll learn:
- How to handle different movement costs
- Priority queues for efficient exploration
- Why Dijkstra is optimal for weighted graphs
- When to use Dijkstra vs BFS

**Preparation**: Make sure you understand:
- How BFS uses a queue
- Path reconstruction with parent pointers
- Why exploring in order of distance matters

---

## 📚 Week 3 Resources

- **📝 [Week 3 Exercises](../exercises/week_03.md)** - Practice problems
- **✅ [Week 3 Solutions](../solutions/week_03_solutions.md)** - Detailed solutions
- **🔬 [BFS & DFS Notebook](../notebooks/02_bfs_dfs.ipynb)** - Interactive exploration
- **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)** - Full 12-week guide

**➡️ [Continue to Week 4: Dijkstra's Algorithm](week_04_dijkstra.md)** | **⬅️ [Back to Week 2](week_02_grid_model.md)** | **📖 [Back to Roadmap](../LEARNING_ROADMAP.md)**

---

## End-to-End Pipeline Connection

Week 3 introduces the first complete search loop:

```text
Grid → BFS/DFS → SearchResult → path + visited order → visualization and metrics
```

BFS and DFS are the simplest algorithms in the product, so they are the best place to understand the contract every later algorithm should follow.

### The SearchResult Handoff

The UI and visualization layers should not need to know whether a path came from BFS, DFS, Dijkstra, or A*. They should receive a consistent result containing the final path, visited cells, path length, runtime, and success state.

This matters because Week 7 can draw any algorithm result if the result shape is consistent, and Week 9 can benchmark every algorithm with the same metric fields.

### What BFS Teaches the Product

BFS proves that the grid and path reconstruction logic work on unweighted maps. If BFS cannot find the expected path on a simple grid, fix the grid or reconstruction before moving to harder algorithms.

BFS is also the baseline for correctness: on unweighted 4-directional grids, it should find a shortest path by number of steps.

### What DFS Teaches the Product

DFS shows that a valid path is different from an optimal path. In the Gradio app, this distinction becomes visible: DFS may reach the goal, but it can explore deeply in an inefficient direction or return a longer route.

That visual difference prepares you for Week 9 comparisons.

### Debugging Search Behavior

When a search result looks wrong, inspect these values in order:

1. `visited`: prevents repeated work and infinite loops.
2. `came_from` or parent tracking: controls path reconstruction.
3. neighbor order: influences DFS path shape and BFS tie-breaking.
4. success/no-path handling: keeps the UI from crashing.

### Week 3 Build Checkpoint

You are ready for Week 4 when you can explain why BFS finds shortest unweighted paths, why DFS does not guarantee shortest paths, and how visited nodes become a teaching visualization.
