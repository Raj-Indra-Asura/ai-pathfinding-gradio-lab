# Week 3: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 2 Exercises](week_02.md)** | **📚 [Week 3 Documentation](../docs/week_03_bfs_dfs.md)** | **✅ [Week 3 Solutions](../solutions/week_03_solutions.md)** | **➡️ [Next: Week 4 Exercises](week_04.md)**

---

## Overview

These exercises will help you master Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms. You'll implement, test, and analyze both algorithms to understand their differences.

## Exercise 1: BFS Step Counter (Beginner)

**Goal**: Implement a function that counts how many steps BFS takes to reach each cell.

**Description**: Create a function that runs BFS from a start position and returns a dictionary mapping each reachable position to the minimum number of steps needed to reach it from the start.

**Requirements**:
- Start from position `(0, 0)`
- Return a dictionary: `{(row, col): steps}`
- Use BFS to ensure minimum steps
- Handle unreachable cells (don't include them)

**Starter Code**:
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
    # TODO: Implement this function
    pass

# Test your implementation
grid = Grid(8, 8, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
grid.generate_obstacles(start, (7, 7))

steps = bfs_step_counter(grid, start)

# Print results for a few cells
print(f"Steps to reach (3, 3): {steps.get((3, 3), 'unreachable')}")
print(f"Steps to reach (7, 7): {steps.get((7, 7), 'unreachable')}")
print(f"Total reachable cells: {len(steps)}")
```

**Expected Behavior**:
- `(0, 0)` should have 0 steps
- Adjacent cells should have 1 step
- Each cell has the minimum number of steps needed

**Testing Tips**:
- Try on a grid with no obstacles first
- Verify that adjacent cells differ by 1 step
- Check that unreachable cells are not in the dictionary

---

## Exercise 2: DFS Path Validator (Intermediate)

**Goal**: Implement a function that validates whether a DFS path is valid.

**Description**: Given a path found by DFS, verify that:
1. The path starts at the start position
2. The path ends at the goal position
3. Each consecutive pair of positions are neighbors
4. No position appears twice (no loops)
5. No obstacles are in the path

**Requirements**:
- Return `True` if path is valid, `False` otherwise
- Return a string describing the error if invalid
- Handle edge cases (empty path, single cell path)

**Starter Code**:
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
        - is_valid: True if path is valid, False otherwise
        - error_message: Empty string if valid, description of error otherwise
    """
    # TODO: Implement validation logic
    pass

# Test with a valid path
grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
start = (0, 0)
goal = (2, 2)

valid_path = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
is_valid, error = validate_path(grid, valid_path, start, goal)
print(f"Valid path: {is_valid}, Error: '{error}'")

# Test with an invalid path (has a loop)
invalid_path = [(0, 0), (0, 1), (1, 1), (0, 1), (2, 1), (2, 2)]
is_valid, error = validate_path(grid, invalid_path, start, goal)
print(f"Invalid path: {is_valid}, Error: '{error}'")
```

**Expected Behavior**:
- Valid path returns `(True, "")`
- Invalid path returns `(False, "description of error")`

**Validation Checks**:
1. Path is not empty
2. Path starts at start position
3. Path ends at goal position
4. Each consecutive pair are neighbors
5. No position repeats
6. No obstacles in path

---

## Exercise 3: Bidirectional BFS (Advanced)

**Goal**: Implement a bidirectional BFS that searches from both start and goal simultaneously.

**Description**: Bidirectional BFS runs two BFS searches at the same time: one from start toward goal, and one from goal toward start. When they meet in the middle, you've found a path.

**Requirements**:
- Run BFS from start and goal simultaneously
- Alternate between expanding from each end
- Stop when the two searches meet
- Reconstruct the complete path
- Should be faster than regular BFS on large grids

**Starter Code**:
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
        - path: List of positions from start to goal, or None if no path
        - nodes_visited: Total number of nodes explored
    """
    # TODO: Implement bidirectional BFS
    # Hint: Keep two queues, two visited sets, and two parent dictionaries
    # Hint: Check for intersection after each expansion
    # Hint: When they meet, reconstruct both halves of the path
    pass

# Test on a large grid
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

print(f"\nSpeed improvement: {regular_result.nodes_visited / bi_nodes:.2f}x")
```

**Expected Behavior**:
- Should find the same path length as regular BFS
- Should visit fewer nodes than regular BFS
- Typically 2-4x faster on large grids

**Algorithm Outline**:
1. Initialize two queues (forward and backward)
2. Initialize two visited sets and parent dictionaries
3. Alternate: expand one node from forward queue, then one from backward queue
4. After each expansion, check if the expanded node exists in the other visited set
5. If found, reconstruct path from both halves

---

## Exercise 4: Debugging - Broken DFS (Debugging Challenge)

**Goal**: Find and fix bugs in a broken DFS implementation.

**Description**: The following DFS implementation has several bugs. Run it, observe the problems, and fix them.

**Buggy Code**:
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

def buggy_dfs(grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
    """Buggy DFS implementation - find and fix the bugs!"""
    stack = [start]
    visited = {start}  # Bug 1: Should we mark start as visited immediately?
    parent = {}

    while stack:
        current = stack.pop()

        # Bug 2: Goal check placement
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path  # Bug 3: What's wrong with this path?

        # Bug 4: Neighbor exploration
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                parent[neighbor] = current
                stack.append(neighbor)

    return []  # No path found

# Test the buggy DFS
grid = Grid(8, 8, 0.1, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (7, 7)
grid.generate_obstacles(start, goal)

path = buggy_dfs(grid, start, goal)
print(f"Path found: {path}")
print(f"Path length: {len(path)}")

# Verify path
if len(path) > 0:
    print(f"Starts at {path[0]}, should be {start}")
    print(f"Ends at {path[-1]}, should be {goal}")
```

**Bugs to Find**:
There are 4 bugs in this code. Can you find them all?

**Questions to Consider**:
1. When should nodes be marked as visited in DFS?
2. Where should the goal check happen?
3. What's wrong with the path reconstruction?
4. What happens to the visited set?

**Testing**:
- Run the buggy code and observe the output
- Compare with the correct DFS implementation
- Test on multiple grids to see different failure modes

**Hints**:
- Bug 1: Think about when DFS marks nodes as visited
- Bug 2: Consider the order of operations
- Bug 3: Look at the path direction
- Bug 4: Check if visited is being updated properly

---

## Success Criteria

### Exercise 1 (BFS Step Counter)
- ✅ Returns correct minimum steps for all reachable cells
- ✅ Start position has 0 steps
- ✅ Unreachable cells are not in the dictionary
- ✅ Works with both 4-directional and 8-directional movement

### Exercise 2 (DFS Path Validator)
- ✅ Correctly validates valid paths
- ✅ Detects all types of invalid paths
- ✅ Returns helpful error messages
- ✅ Handles edge cases (empty paths, single cell)

### Exercise 3 (Bidirectional BFS)
- ✅ Finds paths with same length as regular BFS
- ✅ Visits fewer nodes than regular BFS
- ✅ Correctly reconstructs the complete path
- ✅ Handles cases where no path exists

### Exercise 4 (Debugging)
- ✅ Identifies all 4 bugs
- ✅ Understands why each bug causes problems
- ✅ Fixes produce a working DFS implementation
- ✅ Can explain the correct DFS algorithm

---

## Bonus Challenges

### Challenge 1: DFS with Path Length Limit
Modify DFS to stop exploring paths longer than a given limit. This is useful when you know the path shouldn't be too long.

### Challenge 2: BFS Visualization
Create a function that returns the BFS exploration order as a list of "layers" (all nodes at distance 0, then 1, then 2, etc.).

### Challenge 3: Iterative Deepening DFS
Implement iterative deepening DFS (IDDFS), which combines the space efficiency of DFS with the optimality of BFS.

### Challenge 4: Performance Comparison Tool
Create a tool that runs BFS and DFS on 100 random grids and compares:
- Average path lengths
- Average nodes visited
- Success rates
- Runtime

---

## Additional Resources

- [BFS Visualization](https://visualgo.net/en/dfsbfs)
- [Why BFS finds shortest paths](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [DFS Applications](https://www.geeksforgeeks.org/applications-of-depth-first-search/)
- [Bidirectional Search](https://en.wikipedia.org/wiki/Bidirectional_search)

---

---

**✅ [See Solutions](../solutions/week_03_solutions.md)** | **📚 [Back to Week 3 Docs](../docs/week_03_bfs_dfs.md)** | **➡️ [Next: Week 4 Exercises](week_04.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
