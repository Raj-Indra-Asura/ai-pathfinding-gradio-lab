# Week 5: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 4 Exercises](week_04.md)** | **📚 [Week 5 Documentation](../docs/week_05_astar.md)** | **✅ [Week 5 Solutions](../solutions/week_05_solutions.md)** | **➡️ [Next: Week 6 Exercises](week_06.md)**

---

## Overview

These exercises will help you master A* search with heuristics. You'll implement A* variations, understand admissibility, and compare different heuristic functions.

## Exercise 1: Custom Heuristic Evaluator (Beginner)

**Goal**: Create a tool that evaluates whether a custom heuristic is admissible.

**Description**: Implement a function that tests if a heuristic never overestimates by comparing it against actual shortest path costs on a sample grid.

**Requirements**:
- Test heuristic on multiple positions
- Compare h(n) against actual optimal cost
- Report which positions (if any) violate admissibility
- Return True if admissible, False otherwise

**Starter Code**:
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
        - is_admissible: True if no violations found
        - violations: List of violation descriptions
    """
    # TODO: Implement this function
    pass

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

**Expected Behavior**:
- Manhattan should pass (admissible)
- 2×Manhattan should fail (overestimates)
- Reports specific positions where violations occur

**Testing Tips**:
- Test on grids with and without obstacles
- Try different movement modes
- Test edge cases (start position, unreachable positions)

---

## Exercise 2: A* with Weighted Heuristics (Intermediate)

**Goal**: Implement weighted A* that trades optimality for speed.

**Description**: Weighted A* uses f(n) = g(n) + w×h(n) where w > 1. This makes the search faster but may not find the optimal path. Implement it and analyze the trade-off.

**Requirements**:
- Implement weighted A* with configurable weight
- Compare results with standard A* (w=1)
- Track path quality degradation vs speedup
- Test with weights from 1.0 to 3.0

**Starter Code**:
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
    # TODO: Implement weighted A*
    # Hint: Similar to A* but use f = g + weight * h
    pass

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

    quality = (baseline_cost / cost * 100) if cost > 0 else 0

    print(f"Weight {w}:")
    print(f"  Path cost: {cost:.2f}")
    print(f"  Nodes visited: {nodes}")
    print(f"  Path quality: {quality:.1f}% of optimal")
    print()
```

**Expected Behavior**:
- w=1.0: Optimal path (standard A*)
- w>1.0: Faster but potentially suboptimal
- Higher weights → fewer nodes visited, worse paths

**Analysis Questions**:
- At what weight does quality drop below 95%?
- What's the speedup from w=1 to w=2?
- Is the trade-off worth it?

---

## Exercise 3: Multi-Heuristic A* (Advanced)

**Goal**: Implement A* that dynamically chooses between multiple heuristics.

**Description**: Different heuristics work better in different situations. Create an A* variant that selects the best heuristic for each position based on local grid characteristics.

**Requirements**:
- Implement dynamic heuristic selection
- Support at least 3 different heuristics
- Choose based on obstacle density, distance to goal, or other factors
- Compare with single-heuristic A*

**Starter Code**:
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
        - heuristic_stats: Dict counting which heuristic was used
    """
    def select_heuristic(position, goal, grid):
        """Select best heuristic for this position."""
        # TODO: Implement heuristic selection logic
        # Ideas:
        # - Use Manhattan if close to goal
        # - Use Euclidean if far from goal
        # - Consider local obstacle density
        pass

    # TODO: Implement multi-heuristic A*
    pass

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

**Expected Behavior**:
- Adaptively chooses best heuristic
- Performance comparable to best single heuristic
- Shows how often each heuristic was selected

**Challenge Extensions**:
- Learn optimal selection strategy from multiple runs
- Consider directional preferences
- Account for movement mode

---

## Exercise 4: Debugging - Broken A* (Debugging Challenge)

**Goal**: Find and fix bugs in a broken A* implementation.

**Description**: This A* implementation has several bugs that prevent it from working correctly. Find and fix them all.

**Buggy Code**:
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance
import heapq

def buggy_astar(grid: Grid, start: tuple[int, int], goal: tuple[int, int], heuristic):
    """Buggy A* implementation - find and fix the bugs!"""
    # Bug 1: Initial cost calculation?
    h_start = heuristic(start, goal)
    pq = [(h_start, start)]  # Missing something?

    g_cost = {start: 0.0}
    parent = {}

    while pq:
        current_f, current = heapq.heappop(pq)

        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            # Bug 2: Path direction?
            return path, g_cost[goal]

        # Bug 3: Missing closed set check?

        for neighbor in grid.get_neighbors(current):
            move_cost = grid.get_movement_cost(current, neighbor)
            tentative_g = g_cost[current] + move_cost

            # Bug 4: Update condition?
            if neighbor not in g_cost:
                g_cost[neighbor] = tentative_g
                h = heuristic(current, goal)  # Bug 5: Which position's h?
                f = tentative_g + h
                parent[neighbor] = current
                heapq.heappush(pq, (f, neighbor))

    return [], float('inf')

# Test the buggy implementation
grid = Grid(15, 15, 0.15, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
start = (0, 0)
goal = (14, 14)
grid.generate_obstacles(start, goal)

path, cost = buggy_astar(grid, start, goal, manhattan_distance)
print(f"Buggy A* - Path length: {len(path)}, Cost: {cost:.2f}")

# Compare with correct implementation
from pathfinding_lab.algorithms.astar import astar
correct_result = astar(grid, start, goal, manhattan_distance)
print(f"Correct A* - Path length: {correct_result.path_length}, Cost: {correct_result.path_cost:.2f}")

# Are they the same?
print(f"\nResults match: {abs(cost - correct_result.path_cost) < 0.01}")
```

**Bugs to Find**:
There are 5 bugs in this code. Can you find them all?

**Questions to Consider**:
1. What information is missing from the priority queue tuple?
2. Is the path in the correct order?
3. Should we track which nodes have been processed?
4. When should we update g_cost?
5. Which position should we use for the heuristic calculation?

**Testing**:
- Run on multiple grids
- Compare with correct implementation
- Check if paths are optimal

**Hints**:
- Bug 1: Priority queue needs g_cost for tie-breaking
- Bug 2: Path reconstruction order
- Bug 3: Need closed set to avoid revisiting
- Bug 4: Should update on improvement, not just first visit
- Bug 5: Calculate h for neighbor, not current

---

## Success Criteria

### Exercise 1 (Heuristic Evaluator)
- ✅ Correctly identifies admissible heuristics
- ✅ Detects violations in non-admissible heuristics
- ✅ Reports specific positions and values
- ✅ Handles edge cases

### Exercise 2 (Weighted A*)
- ✅ Implements weighted heuristic correctly
- ✅ Shows speed vs quality trade-off
- ✅ Works with different weights
- ✅ Analyzes performance characteristics

### Exercise 3 (Multi-Heuristic)
- ✅ Dynamically selects heuristics
- ✅ Performance comparable to best single heuristic
- ✅ Tracks heuristic usage statistics
- ✅ Provides insights on when each works best

### Exercise 4 (Debugging)
- ✅ Identifies all 5 bugs
- ✅ Understands why each bug is problematic
- ✅ Fixes produce optimal paths
- ✅ Can explain A* invariants

---

## Bonus Challenges

### Challenge 1: Tie-Breaking in A*
Implement different tie-breaking strategies when multiple nodes have the same f-cost. Compare their effects on path quality and exploration.

### Challenge 2: Bounded-Suboptimal A*
Implement A* that guarantees paths within a bound (e.g., at most 10% worse than optimal) but is faster than standard A*.

### Challenge 3: Anytime A*
Create an A* variant that quickly finds a solution, then iteratively improves it if time allows.

### Challenge 4: Heuristic Learning
Analyze which heuristics work best on different grid patterns and create a classifier to automatically select the best one.

---

## Additional Resources

- [A* Optimizations](http://theory.stanford.edu/~amitp/GameProgramming/Variations.html)
- [Weighted A* Paper](https://www.cs.cmu.edu/~maxim/files/hsplanner_jair10.pdf)
- [Heuristic Design Guidelines](https://www.redblobgames.com/pathfinding/heuristics/differential.html)
- [A* Tie-Breaking](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#breaking-ties)

---

---

**✅ [See Solutions](../solutions/week_05_solutions.md)** | **📚 [Back to Week 5 Docs](../docs/week_05_astar.md)** | **➡️ [Next: Week 6 Exercises](week_06.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
