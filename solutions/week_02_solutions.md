# Week 2: Solutions

## Beginner Exercise Solution

### Explanation

The Manhattan distance is the sum of absolute differences in coordinates. It's called "Manhattan" because it's like walking on a city grid where you can only move along streets (not diagonally through buildings).

The key insight is that we need to take the absolute value of the differences to handle cases where pos2 might be "before" pos1 in either dimension.

### Code

```python
from pathfinding_lab.heuristics.manhattan import manhattan_distance

def calculate_manhattan(pos1, pos2):
    """Calculate Manhattan distance between two positions."""
    row1, col1 = pos1
    row2, col2 = pos2
    return abs(row1 - row2) + abs(col1 - col2)

# Test cases
test_cases = [
    ((0, 0), (5, 5)),      # Expected: 10
    ((3, 2), (3, 2)),      # Expected: 0 (same position)
    ((0, 0), (0, 10)),     # Expected: 10 (horizontal)
    ((5, 5), (2, 3)),      # Expected: 5
    ((10, 5), (2, 15)),    # Expected: 18
]

print("Testing Manhattan distance implementation:")
for pos1, pos2 in test_cases:
    your_result = calculate_manhattan(pos1, pos2)
    correct_result = manhattan_distance(pos1, pos2)
    match = "✓" if your_result == correct_result else "✗"
    print(f"{match} {pos1} to {pos2}: Your={your_result}, Correct={correct_result}")
```

### Key Concepts

- **Absolute value**: Ensures distance is always positive regardless of direction
- **Component-wise distance**: Calculate separately for rows and columns, then sum
- **Zero distance**: Same position gives distance of 0
- **Symmetric**: Distance from A to B equals distance from B to A

### Testing Advice

Test edge cases:
- Same position: `(5, 5)` to `(5, 5)` → 0
- Horizontal line: `(3, 0)` to `(3, 10)` → 10
- Vertical line: `(0, 5)` to `(10, 5)` → 10
- General case: `(2, 3)` to `(7, 9)` → 5 + 6 = 11

---

## Intermediate Exercise Solution

### Explanation

This exercise teaches about obstacle patterns and how movement mode affects navigation. By placing obstacles on a diagonal with gaps, we create a situation where:
- 4-directional movement must go around obstacles
- 8-directional movement can sometimes move through diagonal gaps

The key is using `row == col` to identify diagonal positions and the modulo operator to create gaps.

### Code

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.visualization.grid_plot import create_grid_plot
import matplotlib.pyplot as plt

def create_diagonal_barrier_grid():
    """Create a grid with diagonal obstacles and gaps."""
    grid = Grid(15, 15, 0.0, MovementMode.FOUR_DIRECTIONAL)

    # Add diagonal obstacles (row == col) with gaps every 3 cells
    for i in range(15):
        if i % 3 != 0:  # Leave gaps at 0, 3, 6, 9, 12
            grid.add_obstacle((i, i))

    return grid

# Create and test both movement modes
grid_4dir = create_diagonal_barrier_grid()
neighbors_4 = grid_4dir.get_neighbors((7, 7))
print(f"4-directional neighbors at (7,7): {len(neighbors_4)}")
print(f"Neighbors: {neighbors_4}")

# Create 8-directional version with same obstacles
grid_8dir = Grid(15, 15, 0.0, MovementMode.EIGHT_DIRECTIONAL)
for obs in grid_4dir.obstacles:
    grid_8dir.add_obstacle(obs)

neighbors_8 = grid_8dir.get_neighbors((7, 7))
print(f"\n8-directional neighbors at (7,7): {len(neighbors_8)}")
print(f"Neighbors: {neighbors_8}")

# Visualize
fig = create_grid_plot(grid_4dir, (0, 0), (14, 14))
plt.title("Diagonal Barrier Grid (gaps every 3 cells)")
plt.show()
```

**Expected output:**
- 4-directional at (7,7): Should have 2-3 neighbors (blocked by diagonal)
- 8-directional at (7,7): Should have more neighbors (can move diagonally)

### Key Concepts

- **Diagonal patterns**: Use `row == col` for main diagonal
- **Gap creation**: Modulo operator `i % 3` creates regular gaps
- **Movement mode impact**: 8-directional has more options
- **Obstacle copying**: Can copy obstacles between grids while changing movement mode

### Testing Advice

```python
# Verify the pattern visually
assert (6, 6) in grid_4dir.obstacles  # Should be blocked
assert (6, 9) in grid_4dir.obstacles  # Should be blocked
assert (9, 9) not in grid_4dir.obstacles  # Gap at multiples of 3

# Count obstacles
expected_obstacles = 15 - 5  # 15 positions, 5 gaps (0,3,6,9,12)
assert len(grid_4dir.obstacles) == expected_obstacles
print(f"✓ Correct number of obstacles: {len(grid_4dir.obstacles)}")
```

---

## Advanced Exercise Solution

### Explanation

This connectivity checker uses a simplified BFS (Breadth-First Search) that only checks if a goal is reachable, without tracking the actual path. This is a fundamental algorithm that we'll expand on in Week 3.

The algorithm:
1. Start with a queue containing just the start position
2. Mark visited cells to avoid loops
3. For each cell, explore all neighbors
4. If we reach the goal, return True
5. If the queue empties without finding goal, return False

### Code

```python
from collections import deque
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

def is_connected(grid, start, goal):
    """Check if a path exists from start to goal using BFS."""
    # Early exit if start is goal
    if start == goal:
        return True

    # Initialize BFS
    queue = deque([start])
    visited = {start}

    # Explore the grid
    while queue:
        current = queue.popleft()

        # Check if we reached the goal
        if current == goal:
            return True

        # Explore neighbors
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Queue empty, goal not found
    return False

# Comprehensive test suite
def test_connectivity():
    print("Testing connectivity checker...\n")

    # Test 1: Empty grid - should be connected
    grid1 = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result1 = is_connected(grid1, (0, 0), (9, 9))
    assert result1 == True
    print("✓ Test 1: Empty grid is connected")

    # Test 2: Completely blocked path
    grid2 = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    for row in range(10):
        grid2.add_obstacle((row, 5))  # Vertical wall
    result2 = is_connected(grid2, (0, 0), (0, 9))
    assert result2 == False
    print("✓ Test 2: Blocked path correctly detected")

    # Test 3: Wall with gap
    grid3 = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    for row in range(10):
        if row != 5:  # Gap at row 5
            grid3.add_obstacle((row, 5))
    result3 = is_connected(grid3, (0, 0), (0, 9))
    assert result3 == True
    print("✓ Test 3: Path through gap found")

    # Test 4: Start equals goal
    grid4 = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    result4 = is_connected(grid4, (2, 2), (2, 2))
    assert result4 == True
    print("✓ Test 4: Start equals goal")

    # Test 5: Dense obstacles
    grid5 = Grid(10, 10, 0.4, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
    grid5.generate_obstacles((0, 0), (9, 9))
    result5 = is_connected(grid5, (0, 0), (9, 9))
    # This may or may not be connected depending on obstacle generation
    print(f"✓ Test 5: Dense grid (40% obstacles) - Connected: {result5}")

    print("\n✅ All connectivity tests passed!")

test_connectivity()
```

### Key Concepts

- **BFS (Breadth-First Search)**: Explores level by level
- **Queue (deque)**: FIFO structure for BFS
- **Visited set**: Prevents infinite loops and duplicate work
- **Early exit**: Return immediately when goal found
- **Exhaustive search**: Only return False after checking everything

### Testing Advice

Create test grids with known connectivity:
```python
def create_test_maze():
    """Create a maze with known path."""
    grid = Grid(7, 7, 0.0, MovementMode.FOUR_DIRECTIONAL)
    # Create walls
    for i in range(5):
        grid.add_obstacle((i, 3))
    # Leave gap at (5, 3)
    return grid

maze = create_test_maze()
# Should find path through gap at row 5
assert is_connected(maze, (0, 0), (0, 6)) == True
```

---

## Debugging Challenge Solution

### Bugs Found

**Bug 1: Inefficient data structure**
- **Location**: `visited = []`
- **Problem**: Using a list for visited makes `if current in visited` an O(n) operation
- **Fix**: Use a set: `visited = set()`
- **Impact**: Dramatically improves performance on large grids

**Bug 2: Wrong variable in neighbor retrieval**
- **Location**: `neighbors = grid.get_neighbors(start)`
- **Problem**: Always gets neighbors of start position, not current position
- **Fix**: Change to: `neighbors = grid.get_neighbors(current)`
- **Impact**: Algorithm only explores neighbors of start, not the whole reachable area

**Bug 3: Off-by-one in count**
- **Location**: `return count`
- **Problem**: The problem statement says "reachable cells" which could include or exclude start
- **Fix**: Depends on requirements. If we want cells reachable FROM start (not including it): `return count - 1`
- **Impact**: Clarifies what we're counting

**Bug 4: Inefficient queue operation** (bonus)
- **Location**: `queue.pop(0)`
- **Problem**: `list.pop(0)` is O(n) because it shifts all elements
- **Fix**: Use `collections.deque` and `popleft()` for O(1) operation
- **Impact**: Much faster for large queues

### Corrected Code

```python
from collections import deque
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode

def count_reachable_cells(grid, start):
    """Count all cells reachable from start position (excluding start itself)."""
    visited = set()  # Fix 1: Use set for O(1) lookup
    queue = deque([start])  # Fix 4: Use deque for O(1) popleft
    count = 0

    while queue:
        current = queue.popleft()  # Fix 4: Use popleft() not pop(0)

        if current in visited:
            continue

        visited.add(current)  # Fix 1: set.add() not list.append()
        count += 1

        # Fix 2: Get neighbors of CURRENT not start
        neighbors = grid.get_neighbors(current)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)

    # Fix 3: Don't count the start position itself
    return count - 1

# Test
grid = Grid(5, 5, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
grid.generate_obstacles((0, 0), (4, 4))
reachable = count_reachable_cells(grid, (0, 0))
total_cells = grid.width * grid.height
obstacles = len(grid.obstacles)
expected_max = total_cells - obstacles - 1  # -1 for start position

print(f"Grid: {grid.width}x{grid.height}")
print(f"Obstacles: {obstacles}")
print(f"Reachable cells from (0,0): {reachable}")
print(f"Expected maximum: {expected_max}")
print(f"Match: {reachable <= expected_max}")
```

### What You Should Understand

1. **Data structure choice matters**: List vs Set vs Deque each have different performance characteristics
   - List: O(n) for `in` check
   - Set: O(1) for `in` check
   - Deque: O(1) for popleft/append, O(n) for random access

2. **Variable scope**: Using the wrong variable (`start` vs `current`) completely breaks the algorithm logic

3. **Off-by-one errors**: Always clarify whether you're counting "from start" (inclusive) or "reachable from start" (exclusive)

4. **Algorithm efficiency**: Small changes like `pop(0)` → `popleft()` can make huge performance differences

5. **Testing reveals bugs**: Without proper testing, these bugs might go unnoticed until they cause problems in production

---

**Next: Week 3 Exercises →**
