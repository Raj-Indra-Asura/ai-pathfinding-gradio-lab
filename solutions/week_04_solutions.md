# Week 4 Solutions: Dijkstra's Algorithm

## Exercise 1: Priority Queue Cost Tracker (Beginner)

### Explanation

This solution implements Dijkstra's algorithm to track the minimum cost to reach each cell. The key is using a priority queue (heapq) to always explore the lowest-cost node next, ensuring we find optimal costs.

**Approach**:
1. Initialize priority queue with start at cost 0.0
2. Track best known cost to each position in a dictionary
3. Pop lowest-cost node, explore neighbors
4. Update costs if we found a cheaper path
5. Continue until queue is empty

### Code

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
    # Priority queue: (cost, position)
    pq = [(0.0, start)]
    costs = {start: 0.0}

    while pq:
        current_cost, current = heapq.heappop(pq)

        # Skip if we've already found a better path
        if current_cost > costs.get(current, float('inf')):
            continue

        # Explore neighbors
        for neighbor in grid.get_neighbors(current):
            # Calculate cost via current node
            move_cost = grid.get_movement_cost(current, neighbor)
            new_cost = current_cost + move_cost

            # Update if this is a better path
            if new_cost < costs.get(neighbor, float('inf')):
                costs[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))

    return costs


# Test implementation
grid = Grid(8, 8, 0.2, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
start = (0, 0)
grid.generate_obstacles(start, (7, 7))

costs = dijkstra_cost_tracker(grid, start)

# Print results
print(f"Cost to reach (3, 3): {costs.get((3, 3), 'unreachable'):.2f}")
print(f"Cost to reach (7, 7): {costs.get((7, 7), 'unreachable'):.2f}")
print(f"Total reachable cells: {len(costs)}")

# Analyze cost distribution
cost_ranges = {
    "0-2": 0, "2-5": 0, "5-10": 0, "10-15": 0, "15+": 0
}
for cost in costs.values():
    if cost < 2:
        cost_ranges["0-2"] += 1
    elif cost < 5:
        cost_ranges["2-5"] += 1
    elif cost < 10:
        cost_ranges["5-10"] += 1
    elif cost < 15:
        cost_ranges["10-15"] += 1
    else:
        cost_ranges["15+"] += 1

print("\nCost distribution:")
for range_name, count in cost_ranges.items():
    print(f"  {range_name}: {count} cells")
```

### Key Concepts

- **Priority queue with costs**: `(cost, position)` tuples in heapq
- **Optimal substructure**: Best cost to a node comes from best cost to its parent
- **Greedy exploration**: Always expand lowest-cost node first
- **Cost comparison**: Use `float('inf')` for unvisited nodes
- **Movement costs**: Diagonal moves cost √2 ≈ 1.414, orthogonal cost 1.0

### Testing Advice

**Test Case 1: Compare with BFS on 4-directional**
```python
# On 4-directional grid, costs should equal BFS step counts
grid_4dir = Grid(10, 10, 0.1, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
grid_4dir.generate_obstacles((0, 0), (9, 9))

costs = dijkstra_cost_tracker(grid_4dir, (0, 0))
# Verify: cost to adjacent cells should be 1.0
```

**Test Case 2: Verify diagonal costs**
```python
# On 8-directional, diagonals cost more
grid_8dir = Grid(5, 5, 0.0, MovementMode.EIGHT_DIRECTIONAL)
costs = dijkstra_cost_tracker(grid_8dir, (0, 0))

assert abs(costs[(1, 1)] - 1.414) < 0.01  # Diagonal
assert abs(costs[(1, 0)] - 1.0) < 0.01     # Orthogonal
```

---

## Exercise 2: Heap Operations Validator (Intermediate)

### Explanation

This validator wraps heapq operations to verify Dijkstra's correctness. It ensures costs are popped in non-decreasing order, which is fundamental to Dijkstra's optimality guarantee.

### Code

```python
import heapq

class HeapValidator:
    """Validate heap operations for Dijkstra's algorithm."""

    def __init__(self):
        self.heap = []
        self.pop_history = []  # Track popped costs
        self.violations = []
        self.last_popped_cost = None

    def push(self, cost: float, item: any):
        """Push item with cost onto heap."""
        heapq.heappush(self.heap, (cost, item))

    def pop(self) -> tuple[float, any]:
        """Pop minimum cost item from heap."""
        if not self.heap:
            raise IndexError("Pop from empty heap")

        cost, item = heapq.heappop(self.heap)
        self.pop_history.append(cost)

        # Validate: costs should be non-decreasing
        if self.last_popped_cost is not None:
            if cost < self.last_popped_cost:
                violation = (
                    f"Cost decreased: {self.last_popped_cost:.2f} -> {cost:.2f} "
                    f"(item: {item})"
                )
                self.violations.append(violation)

        self.last_popped_cost = cost
        return cost, item

    def get_violations(self) -> list[str]:
        """Return list of detected violations."""
        return self.violations

    def is_valid(self) -> bool:
        """Check if all operations were valid."""
        return len(self.violations) == 0


# Test the validator
validator = HeapValidator()

# Simulate correct Dijkstra's operations
validator.push(0.0, (0, 0))
validator.push(1.0, (0, 1))
validator.push(1.0, (1, 0))

cost1, pos1 = validator.pop()  # 0.0
cost2, pos2 = validator.pop()  # 1.0

# Add more items
validator.push(5.0, (2, 2))
validator.push(2.0, (1, 1))  # Should come out before (2,2)

cost3, pos3 = validator.pop()  # 1.0
cost4, pos4 = validator.pop()  # 2.0
cost5, pos5 = validator.pop()  # 5.0

print("Violations:", validator.get_violations())
print("Pop sequence:", [f"{c:.1f}" for c in validator.pop_history])
print(f"Valid: {validator.is_valid()}")

# Test with violation
print("\n--- Testing with violation ---")
validator2 = HeapValidator()
validator2.push(0.0, "start")
validator2.push(5.0, "expensive")

validator2.pop()  # 0.0
# Manually insert violation (in real code, this shouldn't happen)
validator2.heap = [(3.0, "cheap")]  # Lower than what we just popped? No, 3.0 > 0.0
validator2.pop()  # 3.0 - this is fine

print("Violations:", validator2.get_violations())
```

### Key Concepts

- **Heap invariant**: Min-heap ensures smallest element is always at top
- **Non-decreasing pop sequence**: Critical for Dijkstra's correctness
- **Validation pattern**: Wrap operations to add checks
- **Debugging tool**: Helps identify incorrect heap usage

### Testing Advice

```python
def test_validator():
    """Test the heap validator."""
    v = HeapValidator()

    # Add items in random order
    v.push(5.0, "e")
    v.push(1.0, "a")
    v.push(3.0, "c")
    v.push(2.0, "b")
    v.push(4.0, "d")

    # Pop all - should come out sorted
    costs = []
    while v.heap:
        cost, _ = v.pop()
        costs.append(cost)

    assert costs == [1.0, 2.0, 3.0, 4.0, 5.0], "Costs not in order!"
    assert v.is_valid(), "Validation failed!"
    print("✓ Heap validator working correctly")

test_validator()
```

---

## Exercise 3: Compare Dijkstra vs BFS Performance (Advanced)

### Explanation

This comprehensive comparison tool reveals when Dijkstra's and BFS differ. On 4-directional grids, they're identical. On 8-directional grids, Dijkstra's finds cheaper paths by properly accounting for diagonal costs.

### Code

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
    results = []

    for trial in range(num_trials):
        # Create grid with unique seed
        grid = Grid(
            grid_size, grid_size, obstacle_pct,
            movement_mode, random_seed=42 + trial
        )
        start = (0, 0)
        goal = (grid_size - 1, grid_size - 1)
        grid.generate_obstacles(start, goal)

        # Run both algorithms
        bfs_result = bfs(grid, start, goal)
        dijkstra_result = dijkstra(grid, start, goal)

        # Only compare if both found paths
        if bfs_result.success and dijkstra_result.success:
            costs_match = abs(bfs_result.path_cost - dijkstra_result.path_cost) < 0.01
            paths_match = bfs_result.path == dijkstra_result.path

            result = ComparisonResult(
                grid_size=grid_size,
                movement_mode=movement_mode,
                bfs_path_length=bfs_result.path_length,
                bfs_path_cost=bfs_result.path_cost,
                bfs_nodes_visited=bfs_result.nodes_visited,
                dijkstra_path_length=dijkstra_result.path_length,
                dijkstra_path_cost=dijkstra_result.path_cost,
                dijkstra_nodes_visited=dijkstra_result.nodes_visited,
                costs_match=costs_match,
                paths_match=paths_match
            )
            results.append(result)

    return results

# Test on 4-directional (should be identical)
print("=== 4-Directional Movement ===")
results_4dir = compare_algorithms(15, 0.2, MovementMode.FOUR_DIRECTIONAL, 5)

for i, r in enumerate(results_4dir):
    print(f"Trial {i+1}:")
    print(f"  Costs match: {r.costs_match}")
    print(f"  Paths match: {r.paths_match}")
    print(f"  BFS cost: {r.bfs_path_cost:.2f}, Dijkstra cost: {r.dijkstra_path_cost:.2f}")

# Test on 8-directional (may differ)
print("\n=== 8-Directional Movement ===")
results_8dir = compare_algorithms(15, 0.2, MovementMode.EIGHT_DIRECTIONAL, 5)

cost_differences = []
for i, r in enumerate(results_8dir):
    diff = r.bfs_path_cost - r.dijkstra_path_cost
    cost_differences.append(diff)
    print(f"Trial {i+1}:")
    print(f"  Costs match: {r.costs_match}")
    print(f"  BFS cost: {r.bfs_path_cost:.2f}")
    print(f"  Dijkstra cost: {r.dijkstra_path_cost:.2f}")
    print(f"  Difference: {diff:.2f} (Dijkstra saves {diff:.1%} of BFS cost)")

# Summary statistics
if cost_differences:
    avg_savings = sum(cost_differences) / len(cost_differences)
    max_savings = max(cost_differences)
    print(f"\nSummary:")
    print(f"  Average cost savings: {avg_savings:.2f}")
    print(f"  Maximum cost savings: {max_savings:.2f}")
    print(f"  Dijkstra found cheaper paths in {sum(1 for d in cost_differences if d > 0.01)}/{len(cost_differences)} cases")
```

### Key Concepts

- **Movement mode matters**: 4-dir vs 8-dir affects whether BFS and Dijkstra differ
- **Cost vs steps**: BFS optimizes steps, Dijkstra optimizes cost
- **Statistical analysis**: Multiple trials reveal typical behavior
- **Performance trade-off**: Dijkstra finds cheaper paths but visits more nodes

### Why They Differ on 8-Directional

**Example Path**:
```
Start (0,0) -> Goal (3,3)

BFS path: (0,0) -> (1,1) -> (2,2) -> (3,3)
  - 3 diagonal moves
  - Cost: 3 × 1.414 = 4.24

Dijkstra path: (0,0) -> (1,0) -> (2,0) -> (3,0) -> (3,1) -> (3,2) -> (3,3)
  - 6 orthogonal moves
  - Cost: 6 × 1.0 = 6.0

Wait! In this case BFS is actually cheaper! So Dijkstra would choose the diagonal path too.
Let me reconsider...

Actually, with proper costs:
- Both should find the same optimal path: diagonals (cost 4.24)
- The difference comes when obstacles force detours
```

### Testing Advice

```python
# Create specific test case
def test_specific_case():
    """Test case where BFS and Dijkstra must differ."""
    # On 8-directional with equal costs, they should match
    grid = Grid(10, 10, 0.15, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
    grid.generate_obstacles((0, 0), (9, 9))

    bfs_result = bfs(grid, (0, 0), (9, 9))
    dijk_result = dijkstra(grid, (0, 0), (9, 9))

    print(f"BFS: {bfs_result.path_length} steps, cost {bfs_result.path_cost:.2f}")
    print(f"Dijkstra: {dijk_result.path_length} steps, cost {dijk_result.path_cost:.2f}")

test_specific_case()
```

---

## Exercise 4: Debugging - Broken Dijkstra (Debugging Challenge)

### Bugs Found

#### Bug 1: Start Cost Should Be 0.0, Not 1.0
**Problem**: Starting with cost 1.0 instead of 0.0
```python
# WRONG
pq = [(1.0, start)]
cost_so_far = {start: 1.0}
```

**Why it's wrong**: The cost to reach the start from the start is 0, not 1. This adds 1.0 to all path costs.

**Fix**:
```python
# CORRECT
pq = [(0.0, start)]
cost_so_far = {start: 0.0}
```

#### Bug 2: Missing Outdated Node Check
**Problem**: No check for outdated entries after popping

**Why it's wrong**: The same node can be in the priority queue multiple times with different costs. We should skip if we've already processed this node with a better cost.

**Fix**: Add this check after popping:
```python
if current_cost > cost_so_far.get(current, float('inf')):
    continue
```

#### Bug 3: Path is Backwards
**Problem**: Path reconstruction builds backwards but doesn't reverse

**Why it's wrong**: We build the path from goal to start, but need to return start to goal.

**Fix**: Add `path.reverse()` before returning:
```python
path.reverse()
return path, cost_so_far[goal]
```

#### Bug 4: Only Updates When Node Not Visited
**Problem**: Condition `if neighbor not in cost_so_far`

**Why it's wrong**: We should update if we found a *cheaper* path, not just if we've never seen the node. This prevents finding optimal paths.

**Fix**:
```python
# CORRECT
if new_cost < cost_so_far.get(neighbor, float('inf')):
    cost_so_far[neighbor] = new_cost
    parent[neighbor] = current
    heapq.heappush(pq, (new_cost, neighbor))
```

### Corrected Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
import heapq

def corrected_dijkstra(
    grid: Grid,
    start: tuple[int, int],
    goal: tuple[int, int]
) -> tuple[list, float]:
    """Corrected Dijkstra implementation."""
    # FIX 1: Start with cost 0.0
    pq = [(0.0, start)]
    cost_so_far = {start: 0.0}
    parent = {}

    while pq:
        current_cost, current = heapq.heappop(pq)

        # FIX 2: Skip outdated entries
        if current_cost > cost_so_far.get(current, float('inf')):
            continue

        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()  # FIX 3: Reverse the path
            return path, cost_so_far[goal]

        # Explore neighbors
        for neighbor in grid.get_neighbors(current):
            move_cost = grid.get_movement_cost(current, neighbor)
            new_cost = current_cost + move_cost

            # FIX 4: Update if cost improved
            if new_cost < cost_so_far.get(neighbor, float('inf')):
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return [], float('inf')


# Test the corrected implementation
grid = Grid(10, 10, 0.15, MovementMode.EIGHT_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (9, 9)
grid.generate_obstacles(start, goal)

path, cost = corrected_dijkstra(grid, start, goal)
print(f"Corrected - Path length: {len(path)}, Cost: {cost:.2f}")

# Compare with library implementation
from pathfinding_lab.algorithms.dijkstra import dijkstra
correct_result = dijkstra(grid, start, goal)
print(f"Library - Path length: {correct_result.path_length}, Cost: {correct_result.path_cost:.2f}")

# Verify they match
cost_match = abs(cost - correct_result.path_cost) < 0.01
print(f"\nCosts match: {cost_match}")
print(f"Path correct: {path[0] == start and path[-1] == goal}")
```

### Summary of Fixes

| Bug | Issue | Impact | Fix |
|-----|-------|--------|-----|
| 1 | Start cost = 1.0 | All costs off by 1.0 | Use 0.0 |
| 2 | No outdated check | Wastes time, may revisit nodes | Add cost comparison |
| 3 | Path backwards | Wrong order | Add reverse() |
| 4 | Wrong update condition | Misses better paths | Check cost improvement |

### What You Should Understand

**Dijkstra's Invariants**:
1. **Cost to start is 0**: Starting point costs nothing to reach
2. **Once popped, optimal**: When a node is popped with cost C, we've found the optimal path to it
3. **Always update on improvement**: If we find a cheaper path, always update
4. **Outdated entries exist**: The heap can have multiple entries for the same node

**Why These Bugs Break Dijkstra**:
- **Bug 1**: Makes all paths appear more expensive than they are
- **Bug 2**: Reduces efficiency but doesn't break correctness
- **Bug 3**: Returns unusable path (wrong direction)
- **Bug 4**: **Breaks correctness** - can miss optimal paths entirely

**Testing Strategy**:
```python
# Always test these aspects
def validate_dijkstra(impl):
    grid = Grid(5, 5, 0.0, MovementMode.EIGHT_DIRECTIONAL)
    path, cost = impl(grid, (0, 0), (4, 4))

    # Check 1: Start cost is 0
    # (Implicit in returned cost)

    # Check 2: Path starts at start
    assert path[0] == (0, 0), "Path doesn't start at start!"

    # Check 3: Path ends at goal
    assert path[-1] == (4, 4), "Path doesn't end at goal!"

    # Check 4: Cost is optimal
    # (Compare with known-good implementation)

    print("✓ All validations passed")
```

---

## Additional Practice

### Challenge: Implement Dijkstra Variants

```python
# 1. Lazy Dijkstra (no outdated check)
def lazy_dijkstra(grid, start, goal):
    """Version without outdated node check - less efficient."""
    # Same as standard but remove the "continue" check
    pass

# 2. Early-exit Dijkstra (stop when goal added to queue)
def early_exit_dijkstra(grid, start, goal):
    """Is this safe? Why or why not?"""
    # Add goal check when adding to queue instead of when popping
    # This is WRONG - goal might be in queue with non-optimal cost!
    pass
```

---

**Next: Continue to Week 5 - A* Algorithm →**
