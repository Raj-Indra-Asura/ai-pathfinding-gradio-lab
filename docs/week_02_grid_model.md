# Week 2: Grid Model

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 1](week_01_python_project_setup.md)** | **📝 [Week 2 Exercises](../exercises/week_02.md)** | **✅ [Week 2 Solutions](../solutions/week_02_solutions.md)** | **🔬 [Notebook](../notebooks/01_grid_basics.ipynb)** | **➡️ [Next: Week 3](week_03_bfs_dfs.md)**

---

## Learning Goals

By the end of this week, you will:
- Understand 2D grid representation for pathfinding
- Learn about nodes, cells, and coordinates
- Master obstacle handling and neighbor generation
- Understand 4-directional vs 8-directional movement
- Implement grid operations confidently

## Theory

### Grid Representation

A **grid** is the fundamental data structure for pathfinding. Think of it like a chess board or game map where:
- Each cell can be empty (traversable) or blocked (obstacle)
- Positions are represented as (row, col) coordinates
- We can move between adjacent cells

#### Why Use Grids?

Grids are perfect for:
- **Game maps**: 2D games like Pac-Man, tower defense
- **Robot navigation**: Warehouse robots, autonomous vehicles
- **Puzzle solving**: Sliding puzzles, maze solving
- **Route planning**: City navigation on a discretized map

### Coordinate System

We use **matrix-style coordinates** (row, col):
```
(0,0) (0,1) (0,2)
(1,0) (1,1) (1,2)
(2,0) (2,1) (2,2)
```

**Important**:
- Row increases going DOWN
- Col increases going RIGHT
- Different from (x, y) Cartesian coordinates!

### Grid Components

```python
class Grid:
    width: int          # Number of columns
    height: int         # Number of rows
    grid: np.array      # 2D array for visualization
    obstacles: Set      # Fast lookup of blocked cells
```

### Movement Modes

**4-Directional Movement** (Cardinal directions):
- Up: (-1, 0)
- Right: (0, 1)
- Down: (1, 0)
- Left: (0, -1)

**8-Directional Movement** (Cardinal + Diagonal):
- Adds: (-1, -1), (-1, 1), (1, -1), (1, 1)
- Diagonal moves cost √2 ≈ 1.414
- Cardinal moves cost 1.0

### Obstacles

Obstacles are cells that cannot be traversed:
- Walls in a maze
- Water in a terrain map
- Buildings in city navigation

We use a **Set** for fast O(1) obstacle lookup:
```python
obstacles = {(2, 3), (2, 4), (2, 5)}  # Blocked cells
```

## Code Walkthrough

Let's examine the Grid class implementation (`src/pathfinding_lab/core/grid.py`):

### 1. Grid Initialization

```python
def __init__(self, width, height, obstacle_density, movement_mode, random_seed):
    self.width = width
    self.height = height
    self.obstacles = set()  # Fast lookup
    self.grid = np.zeros((height, width))  # For visualization
```

**Key Points**:
- Uses numpy array for efficient storage
- Separate `obstacles` set for O(1) lookup
- Configurable size and obstacle density

### 2. Generating Obstacles

```python
def generate_obstacles(self, start, goal):
    # Calculate number of obstacles
    num_obstacles = int(self.width * self.height * self.obstacle_density)

    # Keep start and goal clear
    protected = {start, goal}

    # Add random obstacles
    while len(self.obstacles) < num_obstacles:
        pos = (random.randint(0, self.height-1),
               random.randint(0, self.width-1))
        if pos not in protected:
            self.add_obstacle(pos)
```

**Why protect neighbors?** Ensures the start and goal aren't completely blocked, making pathfinding possible.

### 3. Getting Neighbors

```python
def get_neighbors(self, position):
    row, col = position
    neighbors = []

    if self.movement_mode == MovementMode.FOUR_DIRECTIONAL:
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    else:
        directions = [
            (-1, 0), (-1, 1), (0, 1), (1, 1),
            (1, 0), (1, -1), (0, -1), (-1, -1)
        ]

    for dr, dc in directions:
        new_pos = (row + dr, col + dc)
        if self.is_valid(new_pos) and not self.is_obstacle(new_pos):
            neighbors.append(new_pos)

    return neighbors
```

**Process**:
1. Get current position coordinates
2. Try each direction offset
3. Check if new position is valid and not blocked
4. Add valid neighbors to list

### 4. Movement Cost

```python
def get_movement_cost(self, from_pos, to_pos):
    row1, col1 = from_pos
    row2, col2 = to_pos

    # Check if diagonal
    if abs(row1 - row2) == 1 and abs(col1 - col2) == 1:
        return np.sqrt(2)  # ~1.414
    return 1.0  # Cardinal
```

**Why different costs?**
- Diagonal distance is longer: √(1² + 1²) = √2
- Accurate costs lead to better paths

## Common Mistakes

### 1. Confusing (row, col) with (x, y)

**Problem**: Using Cartesian (x, y) instead of matrix (row, col)
```python
# WRONG
position = (x, y)  # x is horizontal, y is vertical

# CORRECT
position = (row, col)  # row is vertical, col is horizontal
```

**Solution**: Always think "row-first" like reading a book.

### 2. Off-by-One Errors

**Problem**: Using `range(width)` for rows or vice versa
```python
# WRONG
for row in range(grid.width):  # width is for columns!
    for col in range(grid.height):
```

**Solution**: Match dimensions correctly:
```python
# CORRECT
for row in range(grid.height):  # rows = height
    for col in range(grid.width):  # cols = width
```

### 3. Not Checking Boundaries

**Problem**: Accessing cells outside the grid
```python
# WRONG - can crash with IndexError
neighbors.append((row - 1, col))
```

**Solution**: Always validate positions:
```python
# CORRECT
if 0 <= new_row < height and 0 <= new_col < width:
    neighbors.append((new_row, new_col))
```

### 4. Forgetting Diagonal Costs

**Problem**: Treating all moves as equal cost
```python
# WRONG
cost = 1.0  # Always 1, even for diagonals
```

**Solution**: Calculate based on direction:
```python
# CORRECT
if abs(row1 - row2) == 1 and abs(col1 - col2) == 1:
    cost = math.sqrt(2)  # Diagonal
else:
    cost = 1.0  # Cardinal
```

## Mini Project Task

### Task: Build a Maze Generator

Create a function that generates interesting maze patterns.

**Requirements**:
1. Create a `create_corridor_maze(width, height)` function
2. Generate vertical corridors with gaps
3. Make sure there's always a path from (0,0) to (height-1, width-1)
4. Return a Grid object with obstacles placed

**Starter Code**:
```python
def create_corridor_maze(width, height):
    grid = Grid(width, height, 0.0, MovementMode.FOUR_DIRECTIONAL)

    # Add vertical walls every 4 columns
    for col in range(2, width, 4):
        for row in range(height):
            # Leave gaps every 3 rows
            if row % 3 != 0:
                grid.add_obstacle((row, col))

    return grid
```

**Test Your Implementation**:
```python
from pathfinding_lab.visualization.grid_plot import create_grid_plot
import matplotlib.pyplot as plt

maze = create_corridor_maze(20, 20)
fig = create_grid_plot(maze, (0, 0), (19, 19))
plt.show()
```

### Success Criteria
- ✅ Maze has distinct corridors
- ✅ Gaps allow passage between corridors
- ✅ Visual verification shows interesting patterns
- ✅ Path exists from start to goal

## Reflection Questions

1. **Why use a Set for obstacles instead of checking the numpy array?**
   - Hint: Think about lookup time complexity

2. **What happens if you generate too many obstacles?**
   - Consider: When might no path exist?

3. **Why do we need both `grid` (numpy array) and `obstacles` (set)?**
   - Think about: Visualization vs pathfinding

4. **How would you modify the grid for weighted terrain?**
   - Example: Grass (cost 1), sand (cost 2), water (blocked)

5. **What's the trade-off between 4-directional and 8-directional movement?**
   - Consider: Path quality, computation time, realism

## Additional Resources

- [Grid Representation in Games](https://www.redblobgames.com/grids/)
- [Understanding Coordinates](https://processing.org/tutorials/2darray/)
- [Neighbor Generation Patterns](https://en.wikipedia.org/wiki/Moore_neighborhood)

## Next Week Preview

Next week, we'll implement our first pathfinding algorithms: **BFS (Breadth-First Search)** and **DFS (Depth-First Search)**. You'll learn:
- Queue-based exploration (BFS)
- Stack-based exploration (DFS)
- When to use each algorithm
- Why BFS finds shortest paths

**Preparation**: Make sure you're comfortable with:
- Creating grids
- Getting neighbors
- Understanding coordinates
- Checking obstacles

---

## 📚 Week 2 Resources

- **📝 [Week 2 Exercises](../exercises/week_02.md)** - Practice problems
- **✅ [Week 2 Solutions](../solutions/week_02_solutions.md)** - Detailed solutions
- **🔬 [Grid Basics Notebook](../notebooks/01_grid_basics.ipynb)** - Interactive exploration
- **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)** - Full 12-week guide

**➡️ [Continue to Week 3: BFS and DFS](week_03_bfs_dfs.md)** | **⬅️ [Back to Week 1](week_01_python_project_setup.md)** | **📖 [Back to Roadmap](../LEARNING_ROADMAP.md)**
