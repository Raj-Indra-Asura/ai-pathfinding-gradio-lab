# Week 3 Solutions: BFS and DFS

## Exercise 1: BFS Step Counter (Beginner)

### Explanation

This exercise implements a BFS that tracks the minimum number of steps to reach each cell. The key insight is that BFS explores nodes level-by-level, so the first time we reach a cell is always via the shortest path.

**Approach**:
1. Use a queue starting with the start position at step 0
2. For each position, store the step count in a dictionary
3. When exploring neighbors, assign them step_count + 1
4. Only process unvisited cells to ensure minimum steps

### Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from collections import deque

def bfs_step_counter(grid: Grid, start: tuple[int, int]) -> dict[tuple[int, int], int]:
    """
    Count minimum steps from start to each reachable cell using BFS.

    Args:
        grid: The grid to explore
        start: Starting position (row, col)

    Returns:
        Dictionary mapping positions to minimum steps from start
    """
    # Initialize queue with (position, step_count)
    queue = deque([(start, 0)])
    steps = {start: 0}  # Track minimum steps to each position

    while queue:
        current, current_steps = queue.popleft()

        # Explore all neighbors
        for neighbor in grid.get_neighbors(current):
            # Only visit if not already visited
            if neighbor not in steps:
                steps[neighbor] = current_steps + 1
                queue.append((neighbor, current_steps + 1))

    return steps


# Test implementation
grid = Grid(8, 8, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
grid.generate_obstacles(start, (7, 7))

steps = bfs_step_counter(grid, start)

# Print results
print(f"Steps to reach (3, 3): {steps.get((3, 3), 'unreachable')}")
print(f"Steps to reach (7, 7): {steps.get((7, 7), 'unreachable')}")
print(f"Total reachable cells: {len(steps)}")

# Visualize step distribution
step_counts = {}
for pos, step in steps.items():
    step_counts[step] = step_counts.get(step, 0) + 1

print("\nStep distribution:")
for step in sorted(step_counts.keys())[:10]:  # First 10 steps
    print(f"  Step {step}: {step_counts[step]} cells")
```

### Key Concepts

- **BFS guarantees minimum steps**: First time reaching a cell is always shortest
- **Queue with metadata**: Store `(position, step_count)` tuples
- **Visited tracking**: Use dictionary to track both visited status and step count
- **Level-by-level exploration**: All cells at step `k` are explored before step `k+1`

### Testing Advice

**Test Case 1: Empty Grid**
```python
grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
steps = bfs_step_counter(grid, (0, 0))
assert steps[(0, 0)] == 0
assert steps[(0, 1)] == 1
assert steps[(1, 1)] == 2  # Diagonal in 4-directional
```

**Test Case 2: With Obstacles**
```python
grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
grid.add_obstacle((1, 1))
grid.add_obstacle((1, 2))
steps = bfs_step_counter(grid, (0, 0))
# Check that obstacles force longer paths
```

**Test Case 3: Unreachable Cells**
```python
# Create a grid with isolated regions
grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
for col in range(5):
    grid.add_obstacle((2, col))  # Wall across middle
steps = bfs_step_counter(grid, (0, 0))
assert (4, 4) not in steps  # Bottom right is unreachable
```

---

## Exercise 2: DFS Path Validator (Intermediate)

### Explanation

Path validation ensures that a path found by any algorithm is actually valid. This is crucial for debugging and verifying pathfinding implementations.

**Validation Steps**:
1. Check path is not empty
2. Verify start and goal positions
3. Ensure consecutive positions are neighbors
4. Check for loops (no repeated positions)
5. Verify no obstacles in path

### Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

def validate_path(
    grid: Grid,
    path: list[tuple[int, int]],
    start: tuple[int, int],
    goal: tuple[int, int]
) -> tuple[bool, str]:
    """
    Validate a path found by a search algorithm.

    Args:
        grid: The grid the path is on
        path: List of positions forming the path
        start: Expected start position
        goal: Expected goal position

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check 1: Path must not be empty
    if not path:
        return False, "Path is empty"

    # Check 2: Path must start at start position
    if path[0] != start:
        return False, f"Path starts at {path[0]}, expected {start}"

    # Check 3: Path must end at goal position
    if path[-1] != goal:
        return False, f"Path ends at {path[-1]}, expected {goal}"

    # Check 4: No position should repeat (no loops)
    seen = set()
    for i, pos in enumerate(path):
        if pos in seen:
            return False, f"Position {pos} appears multiple times (loop detected at index {i})"
        seen.add(pos)

    # Check 5: Each consecutive pair must be neighbors
    for i in range(len(path) - 1):
        current = path[i]
        next_pos = path[i + 1]

        neighbors = grid.get_neighbors(current)
        if next_pos not in neighbors:
            return False, f"Position {next_pos} is not a neighbor of {current} (at index {i})"

    # Check 6: No obstacles in path
    for i, pos in enumerate(path):
        if grid.is_obstacle(pos):
            return False, f"Position {pos} is an obstacle (at index {i})"

    # All checks passed
    return True, ""


# Test with valid path
grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
start = (0, 0)
goal = (2, 2)

valid_path = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
is_valid, error = validate_path(grid, valid_path, start, goal)
print(f"Valid path: {is_valid}, Error: '{error}'")

# Test with invalid paths
test_cases = [
    ([], "Empty path"),
    ([(1, 1), (2, 2)], "Wrong start"),
    ([(0, 0), (1, 1)], "Wrong goal"),
    ([(0, 0), (0, 1), (1, 1), (0, 1), (2, 1), (2, 2)], "Has loop"),
    ([(0, 0), (2, 2)], "Non-adjacent positions"),
]

for test_path, description in test_cases:
    is_valid, error = validate_path(grid, test_path, start, goal)
    print(f"{description}: valid={is_valid}, error='{error}'")

# Test with obstacle in path
grid.add_obstacle((1, 1))
invalid_path = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
is_valid, error = validate_path(grid, invalid_path, start, goal)
print(f"Path through obstacle: valid={is_valid}, error='{error}'")
```

### Key Concepts

- **Multiple validation checks**: Each catches different types of errors
- **Early return**: Stop validation as soon as an error is found
- **Descriptive errors**: Help users understand what went wrong
- **Set for loop detection**: O(1) lookup for repeated positions
- **Neighbor verification**: Use grid's `get_neighbors()` for consistency

### Testing Advice

Create a comprehensive test suite:

```python
def test_path_validator():
    """Comprehensive path validation tests."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    # Test valid path
    valid = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
    assert validate_path(grid, valid, start, goal)[0]

    # Test each error condition
    assert not validate_path(grid, [], start, goal)[0]  # Empty
    assert not validate_path(grid, [(1, 0)], start, goal)[0]  # Wrong start
    assert not validate_path(grid, [(0, 0)], start, goal)[0]  # Wrong goal
    assert not validate_path(grid, [(0, 0), (0, 1), (0, 0)], start, goal)[0]  # Loop

    print("All validation tests passed!")

test_path_validator()
```

---

## Exercise 3: Bidirectional BFS (Advanced)

### Explanation

Bidirectional BFS searches from both start and goal simultaneously, meeting in the middle. This can be up to 2x faster than regular BFS because it explores roughly half the search space.

**Key Idea**: Instead of exploring a circle of radius `d` from start, we explore two circles of radius `d/2` from start and goal. The area explored is roughly halved: `π(d/2)² + π(d/2)² = πd²/2` vs `πd²`.

### Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from collections import deque

def bidirectional_bfs(
    grid: Grid,
    start: tuple[int, int],
    goal: tuple[int, int]
) -> tuple[list[tuple[int, int]] | None, int]:
    """
    Find path using bidirectional BFS.

    Args:
        grid: The grid to search
        start: Start position
        goal: Goal position

    Returns:
        Tuple of (path, nodes_visited)
    """
    # Handle trivial case
    if start == goal:
        return [start], 1

    # Initialize forward search (from start)
    forward_queue = deque([start])
    forward_visited = {start}
    forward_parent = {start: None}

    # Initialize backward search (from goal)
    backward_queue = deque([goal])
    backward_visited = {goal}
    backward_parent = {goal: None}

    nodes_visited = 0

    # Search until queues are empty or paths meet
    while forward_queue or backward_queue:
        # Expand from forward direction
        if forward_queue:
            current = forward_queue.popleft()
            nodes_visited += 1

            # Check if we've met the backward search
            if current in backward_visited:
                # Found meeting point! Reconstruct path
                path = _reconstruct_bidirectional_path(
                    forward_parent, backward_parent, current
                )
                return path, nodes_visited

            # Explore neighbors
            for neighbor in grid.get_neighbors(current):
                if neighbor not in forward_visited:
                    forward_visited.add(neighbor)
                    forward_parent[neighbor] = current
                    forward_queue.append(neighbor)

        # Expand from backward direction
        if backward_queue:
            current = backward_queue.popleft()
            nodes_visited += 1

            # Check if we've met the forward search
            if current in forward_visited:
                # Found meeting point! Reconstruct path
                path = _reconstruct_bidirectional_path(
                    forward_parent, backward_parent, current
                )
                return path, nodes_visited

            # Explore neighbors
            for neighbor in grid.get_neighbors(current):
                if neighbor not in backward_visited:
                    backward_visited.add(neighbor)
                    backward_parent[neighbor] = current
                    backward_queue.append(neighbor)

    # No path found
    return None, nodes_visited


def _reconstruct_bidirectional_path(
    forward_parent: dict,
    backward_parent: dict,
    meeting_point: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    Reconstruct path from bidirectional search.

    Args:
        forward_parent: Parent pointers from start
        backward_parent: Parent pointers from goal
        meeting_point: Where the two searches met

    Returns:
        Complete path from start to goal
    """
    # Build path from start to meeting point
    forward_path = []
    current = meeting_point
    while current is not None:
        forward_path.append(current)
        current = forward_parent[current]
    forward_path.reverse()

    # Build path from meeting point to goal
    backward_path = []
    current = backward_parent[meeting_point]  # Skip meeting point (already in forward)
    while current is not None:
        backward_path.append(current)
        current = backward_parent[current]

    # Combine paths
    return forward_path + backward_path


# Test implementation
grid = Grid(30, 30, 0.15, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (29, 29)
grid.generate_obstacles(start, goal)

# Compare with regular BFS
from pathfinding_lab.algorithms.bfs import bfs

bi_path, bi_nodes = bidirectional_bfs(grid, start, goal)
regular_result = bfs(grid, start, goal)

print(f"Bidirectional BFS:")
print(f"  Path length: {len(bi_path) if bi_path else 'No path'}")
print(f"  Nodes visited: {bi_nodes}")

print(f"\nRegular BFS:")
print(f"  Path length: {regular_result.path_length}")
print(f"  Nodes visited: {regular_result.nodes_visited}")

if bi_path:
    print(f"\nSpeed improvement: {regular_result.nodes_visited / bi_nodes:.2f}x")
    print(f"Path lengths match: {len(bi_path) == regular_result.path_length}")
```

### Key Concepts

- **Two simultaneous searches**: Forward from start, backward from goal
- **Meeting point**: First intersection of visited sets
- **Path reconstruction**: Combine forward and backward paths
- **Space efficiency**: Both searches stop when they meet
- **Performance gain**: Most effective on large open grids

### Why It's Faster

**Mathematical Analysis**:
- Regular BFS explores a circle of radius `d`: Area ≈ `πd²`
- Bidirectional explores two circles of radius `d/2`: Area ≈ `2π(d/2)² = πd²/2`
- **Result**: Roughly 2x faster!

**Practical Considerations**:
- Best on large grids with clear paths
- Less effective on highly constrained mazes
- Slight overhead from managing two searches

### Testing Advice

```python
# Test on various grid sizes
for size in [10, 20, 30, 40, 50]:
    grid = Grid(size, size, 0.15, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
    start = (0, 0)
    goal = (size-1, size-1)
    grid.generate_obstacles(start, goal)

    bi_path, bi_nodes = bidirectional_bfs(grid, start, goal)
    regular_result = bfs(grid, start, goal)

    if bi_path:
        speedup = regular_result.nodes_visited / bi_nodes
        print(f"Size {size}x{size}: {speedup:.2f}x speedup")
```

---

## Exercise 4: Debugging - Broken DFS (Debugging Challenge)

### Bugs Found

#### Bug 1: Start is Marked as Visited Too Early
**Problem**: In DFS, we should mark nodes as visited when we pop them from the stack, not when we push them.

**Location**: `visited = {start}`

**Why it's wrong**: The start node should be processed like any other node. Marking it visited before the loop causes inconsistency.

**Fix**: Initialize `visited = set()` (empty set)

#### Bug 2: Missing Visited Check After Pop
**Problem**: The code doesn't check if the node was already visited after popping.

**Location**: After `current = stack.pop()`

**Why it's wrong**: Multiple paths can lead to the same node, causing it to be added to the stack multiple times. We need to skip already-visited nodes.

**Fix**: Add this check:
```python
if current in visited:
    continue
visited.add(current)
```

#### Bug 3: Path is Reversed
**Problem**: Path reconstruction builds the path backwards but doesn't reverse it.

**Location**: Return statement in path reconstruction

**Why it's wrong**: The path starts at goal and follows parents back to start, but we need start→goal order.

**Fix**: Add `path.reverse()` before returning, or build it correctly from the start.

#### Bug 4: Neighbors Not Marked as Visited When Added
**Problem**: Nodes are added to stack but not marked as visited immediately.

**Location**: In the neighbor exploration loop

**Why it's wrong**: Wait, this is actually intentional in DFS! Nodes are marked visited when popped, not when pushed. So this isn't a bug if Bug 2 is fixed.

**Actually**: The real Bug 4 is that we check the goal BEFORE marking as visited, which means we try to reconstruct the path but the current node might not be in the parent dictionary properly.

### Corrected Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

def corrected_dfs(
    grid: Grid,
    start: tuple[int, int],
    goal: tuple[int, int]
) -> list[tuple[int, int]]:
    """Corrected DFS implementation."""
    stack = [start]
    visited = set()  # FIX 1: Empty set, mark when popping
    parent = {}

    while stack:
        current = stack.pop()

        # FIX 2: Skip if already visited
        if current in visited:
            continue

        # FIX 2: Mark as visited when processing
        visited.add(current)

        # Goal check AFTER marking visited
        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()  # FIX 3: Reverse the path
            return path

        # Explore neighbors
        neighbors = grid.get_neighbors(current)
        for neighbor in reversed(neighbors):  # Reversed for consistent order
            if neighbor not in visited:
                if neighbor not in parent:  # Only set parent once
                    parent[neighbor] = current
                stack.append(neighbor)

    return []  # No path found


# Test the corrected DFS
grid = Grid(8, 8, 0.1, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (7, 7)
grid.generate_obstacles(start, goal)

path = corrected_dfs(grid, start, goal)
print(f"Path found: {path}")
print(f"Path length: {len(path)}")

if len(path) > 0:
    print(f"Starts at {path[0]} (expected {start}): {path[0] == start}")
    print(f"Ends at {path[-1]} (expected {goal}): {path[-1] == goal}")

    # Validate the path
    from pathfinding_lab.algorithms.dfs import dfs

    correct_result = dfs(grid, start, goal)
    print(f"\nCorrect DFS path length: {correct_result.path_length}")
    print(f"Our path is valid: {len(path) > 0}")
```

### Summary of Fixes

| Bug | Problem | Fix |
|-----|---------|-----|
| 1 | Start marked visited too early | Initialize with empty set |
| 2 | No visited check after pop | Add `if current in visited: continue` |
| 3 | Path is backwards | Add `path.reverse()` |
| 4 | Goal check before visited mark | Move goal check after `visited.add()` |

### What You Should Understand

**Key DFS Principles**:
1. **Mark visited when popping**, not when pushing
2. **Check visited immediately after popping** to skip duplicates
3. **Goal check after marking** ensures consistency
4. **Path reconstruction goes backwards** and needs reversal

**Why These Bugs Matter**:
- Bug 1 & 2: Can cause infinite loops or incorrect exploration
- Bug 3: Returns path in wrong direction
- Bug 4: Can cause KeyError in parent lookup

**Testing DFS**:
- Always verify path direction (start → goal)
- Check that all positions in path are connected
- Test on grids with multiple paths to goal
- Verify no positions repeat (no loops)

---

## Additional Practice

### Challenge: Compare All Three Implementations

```python
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dfs import dfs

# Create test grid
grid = Grid(20, 20, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (19, 19)
grid.generate_obstacles(start, goal)

# Run all three
bfs_result = bfs(grid, start, goal)
dfs_result = dfs(grid, start, goal)
bi_path, bi_nodes = bidirectional_bfs(grid, start, goal)

# Compare
print("Algorithm Comparison:")
print(f"BFS: path={bfs_result.path_length}, visited={bfs_result.nodes_visited}")
print(f"DFS: path={dfs_result.path_length}, visited={dfs_result.nodes_visited}")
print(f"Bidirectional BFS: path={len(bi_path) if bi_path else 'N/A'}, visited={bi_nodes}")
```

---

**Next: Continue to Week 4 - Dijkstra's Algorithm →**
