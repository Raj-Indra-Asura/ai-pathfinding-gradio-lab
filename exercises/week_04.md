# Week 4: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 3 Exercises](week_03.md)** | **📚 [Week 4 Documentation](../docs/week_04_dijkstra.md)** | **✅ [Week 4 Solutions](../solutions/week_04_solutions.md)** | **➡️ [Next: Week 5 Exercises](week_05.md)**

---

## Overview

These exercises will help you master Dijkstra's algorithm for weighted pathfinding. You'll implement priority queue operations, understand cost-based exploration, and debug common issues.

## Exercise 1: Priority Queue Cost Tracker (Beginner)

**Goal**: Implement a simple cost tracker that uses Dijkstra's approach to find minimum costs.

**Description**: Create a function that tracks the minimum cost to reach each cell using Dijkstra's algorithm, similar to BFS step counter but with weighted edges.

**Requirements**:
- Use `heapq` for the priority queue
- Track minimum cost to each reachable position
- Handle diagonal movement costs (orthogonal = 1.0, diagonal = √2)
- Return dictionary mapping positions to minimum costs

**Starter Code**:
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
import heapq

def dijkstra_cost_tracker(grid: Grid, start: tuple[int, int]) -> dict[tuple[int, int], float]:
    """
    Track minimum cost to reach each cell using Dijkstra's algorithm.

    Args:
        grid: The grid to explore
        start: Starting position (row, col)

    Returns:
        Dictionary mapping positions to minimum cost from start
    """
    # TODO: Implement this function
    pass

# Test your implementation
grid = Grid(8, 8, 0.2, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
start = (0, 0)
grid.generate_obstacles(start, (7, 7))

costs = dijkstra_cost_tracker(grid, start)

# Print results
print(f"Cost to reach (3, 3): {costs.get((3, 3), 'unreachable'):.2f}")
print(f"Cost to reach (7, 7): {costs.get((7, 7), 'unreachable'):.2f}")
print(f"Total reachable cells: {len(costs)}")
```

**Expected Behavior**:
- `(0, 0)` should have cost 0.0
- Adjacent orthogonal cells: cost 1.0
- Adjacent diagonal cells: cost ~1.414
- Costs represent optimal paths

**Testing Tips**:
- Compare with BFS step counter on 4-directional grid
- Verify diagonal moves cost more than orthogonal
- Check that costs increase along paths

---

## Exercise 2: Heap Operations Validator (Intermediate)

**Goal**: Validate correct usage of Python's heapq module in Dijkstra's context.

**Description**: Create a tool that tracks heap operations and verifies they follow Dijkstra's algorithm correctly.

**Requirements**:
- Monitor `heappush` and `heappop` operations
- Verify items are popped in cost order
- Detect if costs are non-decreasing when popped
- Report any violations

**Starter Code**:
```python
import heapq

class HeapValidator:
    """Validate heap operations for Dijkstra's algorithm."""

    def __init__(self):
        self.heap = []
        self.pop_history = []  # Track popped costs
        self.violations = []

    def push(self, cost: float, item: any):
        """Push item with cost onto heap."""
        # TODO: Implement
        pass

    def pop(self) -> tuple[float, any]:
        """Pop minimum cost item from heap."""
        # TODO: Implement and validate
        pass

    def get_violations(self) -> list[str]:
        """Return list of detected violations."""
        return self.violations

# Test the validator
validator = HeapValidator()

# Simulate Dijkstra's operations
validator.push(0.0, (0, 0))
validator.push(1.0, (0, 1))
validator.push(1.0, (1, 0))

cost1, pos1 = validator.pop()  # Should be 0.0
cost2, pos2 = validator.pop()  # Should be 1.0

# Add some out-of-order operations
validator.push(5.0, (2, 2))
validator.push(2.0, (1, 1))  # Should come out before (2,2)

cost3, pos3 = validator.pop()  # Should be 1.0
cost4, pos4 = validator.pop()  # Should be 2.0

print("Violations:", validator.get_violations())
print("Pop sequence:", validator.pop_history)
```

**Expected Behavior**:
- Costs should be non-decreasing when popped
- Violations should be detected and reported
- Helps understand heap invariant

---

## Exercise 3: Compare Dijkstra vs BFS Performance (Advanced)

**Goal**: Implement a comprehensive comparison tool for BFS and Dijkstra's algorithm.

**Description**: Create a tool that runs both algorithms on various grids and analyzes their behavior, especially on 8-directional grids where they differ.

**Requirements**:
- Run on multiple grid configurations
- Track path length, path cost, nodes visited
- Identify when results differ
- Analyze performance characteristics

**Starter Code**:
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dijkstra import dijkstra
from dataclasses import dataclass

@dataclass
class ComparisonResult:
    """Results from comparing BFS and Dijkstra's."""
    grid_size: int
    movement_mode: MovementMode
    bfs_path_length: int
    bfs_path_cost: float
    bfs_nodes_visited: int
    dijkstra_path_length: int
    dijkstra_path_cost: float
    dijkstra_nodes_visited: int
    costs_match: bool
    paths_match: bool

def compare_algorithms(
    grid_size: int,
    obstacle_pct: float,
    movement_mode: MovementMode,
    num_trials: int = 10
) -> list[ComparisonResult]:
    """
    Compare BFS and Dijkstra's on multiple random grids.

    Args:
        grid_size: Size of square grid
        obstacle_pct: Obstacle percentage
        movement_mode: Movement mode to test
        num_trials: Number of random grids to test

    Returns:
        List of comparison results
    """
    # TODO: Implement comparison
    pass

# Test on 4-directional (should be identical)
results_4dir = compare_algorithms(15, 0.2, MovementMode.FOUR_DIRECTIONAL, 5)

print("4-Directional Results:")
for i, r in enumerate(results_4dir):
    print(f"  Trial {i+1}: Costs match={r.costs_match}, Paths match={r.paths_match}")

# Test on 8-directional (may differ)
results_8dir = compare_algorithms(15, 0.2, MovementMode.EIGHT_DIRECTIONAL, 5)

print("\n8-Directional Results:")
for i, r in enumerate(results_8dir):
    print(f"  Trial {i+1}: Costs match={r.costs_match}")
    print(f"    BFS cost: {r.bfs_path_cost:.2f}, Dijkstra cost: {r.dijkstra_path_cost:.2f}")
```

**Expected Behavior**:
- 4-directional: BFS and Dijkstra's should match
- 8-directional: Dijkstra's may find cheaper paths
- Analysis shows when diagonal movements matter

---

## Exercise 4: Debugging - Broken Dijkstra (Debugging Challenge)

**Goal**: Find and fix bugs in a broken Dijkstra's implementation.

**Description**: The following implementation has several subtle bugs that break Dijkstra's correctness or efficiency.

**Buggy Code**:
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
import heapq

def buggy_dijkstra(grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> tuple[list, float]:
    """Buggy Dijkstra implementation - find and fix the bugs!"""
    # Bug 1: Wrong initial cost?
    pq = [(1.0, start)]
    cost_so_far = {start: 1.0}
    parent = {}

    while pq:
        current_cost, current = heapq.heappop(pq)

        # Bug 2: Missing something important here?
        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            # Bug 3: Path direction?
            return path, cost_so_far[goal]

        # Explore neighbors
        for neighbor in grid.get_neighbors(current):
            move_cost = grid.get_movement_cost(current, neighbor)
            new_cost = current_cost + move_cost

            # Bug 4: Condition for updating?
            if neighbor not in cost_so_far:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return [], float('inf')

# Test the buggy implementation
grid = Grid(10, 10, 0.15, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (9, 9)
grid.generate_obstacles(start, goal)

path, cost = buggy_dijkstra(grid, start, goal)
print(f"Path length: {len(path)}")
print(f"Path cost: {cost:.2f}")

# Compare with correct implementation
from pathfinding_lab.algorithms.dijkstra import dijkstra
correct_result = dijkstra(grid, start, goal)
print(f"\nCorrect path length: {correct_result.path_length}")
print(f"Correct path cost: {correct_result.path_cost:.2f}")
print(f"Cost difference: {abs(cost - correct_result.path_cost):.2f}")
```

**Bugs to Find**:
There are 4 bugs in this code. Can you find them all?

**Questions to Consider**:
1. What should the initial cost be?
2. Is there a check missing after popping from the queue?
3. Is the path in the correct order?
4. When should we update costs?

**Testing**:
- Run on multiple grids to see different failure modes
- Compare results with correct implementation
- Check if paths are optimal

**Hints**:
- Bug 1: Start cost should be different
- Bug 2: Efficiency issue with duplicate processing
- Bug 3: Path reconstruction direction
- Bug 4: Only update when cost improves

---

## Success Criteria

### Exercise 1 (Cost Tracker)
- ✅ Returns correct minimum costs for all reachable cells
- ✅ Start position has cost 0.0
- ✅ Handles diagonal costs correctly (~1.414)
- ✅ Uses heapq properly

### Exercise 2 (Heap Validator)
- ✅ Correctly tracks heap operations
- ✅ Detects cost ordering violations
- ✅ Reports clear violation messages
- ✅ Helps understand heap invariant

### Exercise 3 (Algorithm Comparison)
- ✅ Runs comprehensive comparisons
- ✅ Identifies differences between BFS and Dijkstra's
- ✅ Shows when diagonal costs matter
- ✅ Provides statistical analysis

### Exercise 4 (Debugging)
- ✅ Identifies all 4 bugs
- ✅ Understands why each bug is problematic
- ✅ Fixes produce optimal results
- ✅ Can explain Dijkstra's invariants

---

## Bonus Challenges

### Challenge 1: Lazy Dijkstra
Implement "lazy" Dijkstra's that doesn't check for outdated nodes and compare performance with standard version.

### Challenge 2: Dijkstra with Early Exit
Add early termination when goal is reached but not yet popped from queue. Is this safe? Why or why not?

### Challenge 3: Bidirectional Dijkstra
Extend bidirectional BFS to work with Dijkstra's algorithm for weighted graphs.

### Challenge 4: Dijkstra Visualization
Create a visualization showing how the "frontier" of explored costs expands from the start node.

---

## Additional Resources

- [Priority Queue Visualization](https://visualgo.net/en/heap)
- [Dijkstra's Algorithm Animation](https://qiao.github.io/PathFinding.js/visual/)
- [Python heapq Documentation](https://docs.python.org/3/library/heapq.html)
- [Understanding Dijkstra's Correctness](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/04GreedyAlgorithmsI.pdf)

---

---

**✅ [See Solutions](../solutions/week_04_solutions.md)** | **📚 [Back to Week 4 Docs](../docs/week_04_dijkstra.md)** | **➡️ [Next: Week 5 Exercises](week_05.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
