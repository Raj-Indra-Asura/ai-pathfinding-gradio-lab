# Week 2: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 1 Exercises](week_01.md)** | **📚 [Week 2 Documentation](../docs/week_02_grid_model.md)** | **✅ [Week 2 Solutions](../solutions/week_02_solutions.md)** | **➡️ [Next: Week 3 Exercises](week_03.md)**

---

**🔑 Concepts/links you'll need:** tuples & `(row, col)` ([Week 0 §1](../docs/week_00_python_prerequisites.md#prereq-tuples)); sets/dicts & O(1) lookup ([Week 0 §2](../docs/week_00_python_prerequisites.md#prereq-collections)); classes & `self` ([Week 0 §3](../docs/week_00_python_prerequisites.md#prereq-classes)); enums like `MovementMode` ([Week 0 §6](../docs/week_00_python_prerequisites.md#prereq-enums)).

## Warm-up Exercise (Trivial)

### Task: Create a Grid and Look Around

Get comfortable with the `Grid` object before anything harder. Create a small grid, print its
dimensions, and print the neighbors of one cell.

```python
from pathfinding_lab.core.grid import Grid

grid = Grid(width=5, height=4)
print("Dimensions (width x height):", grid.width, "x", grid.height)
print("Neighbors of (1, 1):", grid.get_neighbors((1, 1)))
print("Is (0, 0) valid?", grid.is_valid((0, 0)))
print("Is (9, 9) valid?", grid.is_valid((9, 9)))
```

**You're done when** you can explain why `(1, 1)` has the number of neighbors it does, and why
`(9, 9)` is invalid on this grid. *(New to tuples/classes? See [Week 0 §1 & §3](../docs/week_00_python_prerequisites.md#prereq-tuples).)*

---

## Beginner Exercise

### Task: Grid Distance Calculator

Create a function that calculates the Manhattan distance between any two positions on a grid, then verify it matches the heuristic function.

### Requirements
- Write a function `calculate_manhattan(pos1, pos2)` that returns the Manhattan distance
- Test it on at least 5 different position pairs
- Compare your results with the built-in `manhattan_distance()` function
- Handle edge cases (same position, diagonal positions)

### Hints
- Manhattan distance = |row1 - row2| + |col1 - col2|
- Remember: absolute value for differences
- Test with positions at grid boundaries

### Starter Code
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def calculate_manhattan(pos1, pos2):
    # Your code here
    pass

# Test cases
test_cases = [
    ((0, 0), (5, 5)),
    ((3, 2), (3, 2)),
    ((0, 0), (0, 10)),
    ((5, 5), (2, 3)),
]

for pos1, pos2 in test_cases:
    your_result = calculate_manhattan(pos1, pos2)
    correct_result = manhattan_distance(pos1, pos2)
    print(f"{pos1} to {pos2}: Your={your_result}, Correct={correct_result}")
```

---

## Intermediate Exercise

### Task: Custom Grid with Diagonal Barriers

Create a grid where diagonal lines of obstacles divide the space, then verify that 4-directional movement requires going around while 8-directional can cut through gaps.

### Requirements
- Create a 15x15 grid
- Place diagonal obstacles from (0, 0) to (14, 14)
- Leave gaps every 3 cells
- Test pathfinding with both movement modes
- Compare the number of neighbors at position (7, 7) for both modes

### Hints
- Diagonal line: row == col
- Use modulo operator (%) for gaps
- Call `get_neighbors()` with different movement modes
- Visualize the grid to verify your pattern

### Starter Code
```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

def create_diagonal_barrier_grid():
    # Create grid with 4-directional movement
    grid = Grid(15, 15, 0.0, MovementMode.FOUR_DIRECTIONAL)

    # Add diagonal obstacles with gaps
    # Your code here

    return grid

# Test
grid_4dir = create_diagonal_barrier_grid()
neighbors_4 = grid_4dir.get_neighbors((7, 7))
print(f"4-directional neighbors at (7,7): {len(neighbors_4)}")

# Change to 8-directional
grid_8dir = Grid(15, 15, 0.0, MovementMode.EIGHT_DIRECTIONAL)
# Copy obstacles from grid_4dir
for obs in grid_4dir.obstacles:
    grid_8dir.add_obstacle(obs)

neighbors_8 = grid_8dir.get_neighbors((7, 7))
print(f"8-directional neighbors at (7,7): {len(neighbors_8)}")
```

---

## Advanced Exercise

### Task: Grid Connectivity Checker

Write a function that determines if a path exists between start and goal using a simple flood-fill algorithm (no pathfinding needed yet).

### Requirements
- Implement `is_connected(grid, start, goal)` that returns True/False
- Use BFS-style exploration (queue) without tracking the path
- Handle grids with no connection
- Test on various grid configurations
- Should work with both movement modes

### Hints
- You need a queue (use `collections.deque`)
- Track visited cells to avoid infinite loops
- Only check connectivity, don't build the path
- If you reach goal, return True immediately
- If queue empties without finding goal, return False

### Starter Code
```python
from collections import deque
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

def is_connected(grid, start, goal):
    """Check if a path exists from start to goal."""
    # Your code here
    pass

# Test cases
def test_connectivity():
    # Test 1: Empty grid - should be connected
    grid1 = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    assert is_connected(grid1, (0, 0), (9, 9)) == True
    print("✓ Test 1 passed: Empty grid is connected")

    # Test 2: Create a wall blocking the path
    grid2 = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    for row in range(10):
        grid2.add_obstacle((row, 5))  # Vertical wall
    assert is_connected(grid2, (0, 0), (0, 9)) == False
    print("✓ Test 2 passed: Blocked path detected")

    # Test 3: Wall with a gap
    grid3 = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    for row in range(10):
        if row != 5:  # Gap at row 5
            grid3.add_obstacle((row, 5))
    assert is_connected(grid3, (0, 0), (0, 9)) == True
    print("✓ Test 3 passed: Path through gap found")

    print("All connectivity tests passed!")

test_connectivity()
```

---

## Debugging Challenge

### Buggy Code

The following code is supposed to count how many empty cells are reachable from a starting position, but it has several bugs:

```python
def count_reachable_cells(grid, start):
    """Count all cells reachable from start position."""
    visited = []  # Bug: Should use set for O(1) lookup
    queue = [start]
    count = 0

    while queue:
        current = queue.pop(0)

        if current in visited:
            continue

        visited.append(current)
        count += 1

        # Get neighbors
        neighbors = grid.get_neighbors(start)  # Bug: Should use 'current' not 'start'

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)

    return count  # Bug: Counts start position, actual reachable count should be count - 1

# Test
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

grid = Grid(5, 5, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
grid.generate_obstacles((0, 0), (4, 4))
reachable = count_reachable_cells(grid, (0, 0))
print(f"Reachable cells: {reachable}")
```

### Expected Behavior

The function should:
1. Count all cells that can be reached from the start position
2. Not count the start position itself
3. Use efficient data structures
4. Handle obstacles correctly

### Hints
- Check the data structure for visited cells
- Look carefully at variable names in the neighbor retrieval
- Consider what "reachable" means - should it include the start?
- Think about algorithm efficiency

---

---

**✅ [See Solutions](../solutions/week_02_solutions.md)** | **📚 [Back to Week 2 Docs](../docs/week_02_grid_model.md)** | **➡️ [Next: Week 3 Exercises](week_03.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
