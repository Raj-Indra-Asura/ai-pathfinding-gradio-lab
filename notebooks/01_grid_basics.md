# Notebook 01: Grid Basics

## Overview
This notebook explores the grid data structure, which is the foundation of pathfinding algorithms.

## Topics Covered
- Creating Grid objects
- Adding and removing obstacles
- Understanding coordinate systems
- Generating neighbors (4-directional and 8-directional)
- Visualizing grids

## Setup

```python
# Install requirements
# pip install -r requirements.txt

# Imports
from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.types import MovementMode
from src.pathfinding_lab.visualization.grid_plot import create_grid_plot
import matplotlib.pyplot as plt
```

## Exercise 1: Create a Basic Grid

```python
# Create a 10x10 grid with no obstacles
grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)

# Verify dimensions
print(f"Grid size: {grid.width}x{grid.height}")
print(f"Number of obstacles: {len(grid.obstacles)}")
```

## Exercise 2: Add Obstacles

```python
# Add some obstacles manually
grid.add_obstacle((5, 5))
grid.add_obstacle((5, 6))
grid.add_obstacle((5, 7))

# Or generate random obstacles
start = (0, 0)
goal = (9, 9)
grid.generate_obstacles(start, goal)

print(f"Total obstacles: {len(grid.obstacles)}")
```

## Exercise 3: Explore Neighbors

```python
# Get neighbors of a position
position = (5, 5)
neighbors = grid.get_neighbors(position)

print(f"Neighbors of {position}:")
for neighbor in neighbors:
    print(f"  {neighbor}")
```

## Exercise 4: Visualize

```python
# Create visualization
start = (0, 0)
goal = (9, 9)
fig = create_grid_plot(grid, start, goal)
plt.show()
```

## Challenge

Create a grid where you manually place obstacles to spell out your initials!

## Conclusion

You've learned:
- How to create and manipulate grids
- The coordinate system (row, col)
- How neighbor generation works
- Basic visualization

**Next**: Continue to Notebook 02 - BFS and DFS
