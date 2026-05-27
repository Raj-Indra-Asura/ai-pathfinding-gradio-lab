# Week 7: Visualization Techniques for Pathfinding

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 6](week_06_heuristics.md)** | **📝 [Week 7 Exercises](../exercises/week_07.md)** | **✅ [Week 7 Solutions](../solutions/week_07_solutions.md)** | **➡️ [Next: Week 8](week_08_gradio_ui.md)**

---

## Learning Goals

By the end of this week, you will understand:
- How to visualize grids, paths, and visited nodes using Matplotlib
- Color schemes and their importance for clarity
- Creating comparison plots for multiple algorithms
- Building informative legends and titles
- Performance considerations for real-time visualization
- Exporting visualizations for reports and presentations

## Theory

### Why Visualization Matters

Visualization is crucial for understanding pathfinding algorithms:

1. **Debugging**: See exactly which nodes are visited and in what order
2. **Algorithm Comparison**: Visually compare efficiency between algorithms
3. **Education**: Understand how algorithms explore the search space
4. **Presentation**: Communicate results to stakeholders
5. **Intuition Building**: Develop mental models of algorithm behavior

### Visualization Components

A complete pathfinding visualization includes:

**1. Grid Structure**
- Grid lines showing cell boundaries
- Clear coordinate system (row, column)
- Appropriate sizing for readability

**2. Cell States**
- **Empty cells**: Walkable space (white or light gray)
- **Obstacles**: Blocked cells (black or dark gray)
- **Start position**: Where the path begins (green)
- **Goal position**: Target destination (red)
- **Visited nodes**: Cells explored by the algorithm (light blue)
- **Final path**: The discovered path (yellow or orange)

**3. Metadata**
- Algorithm name
- Path length and cost
- Number of visited nodes
- Runtime in milliseconds
- Success/failure status

**4. Legend**
- Clear labels for each color/symbol
- Positioned to not obscure the grid
- Consistent across all visualizations

### Color Psychology and Accessibility

**Standard Color Scheme**:
- **Green (start)**: "Go" - universally understood
- **Red (goal)**: Target, destination
- **Black (obstacles)**: Impassable, like walls
- **Light blue (visited)**: Explored territory
- **Yellow/Orange (path)**: The solution, highlighted

**Accessibility Considerations**:
- Avoid red-green combinations (colorblind friendly)
- Use patterns or shapes in addition to colors
- Ensure sufficient contrast (WCAG 2.1 AA compliance)
- Provide text labels where possible

### Matplotlib Basics for Grid Visualization

Matplotlib is the industry-standard plotting library for Python. Key concepts:

**1. Figure and Axes**
```python
fig, ax = plt.subplots(figsize=(10, 10))
```
- `fig`: The entire figure/canvas
- `ax`: The plot area where you draw
- `figsize`: Size in inches (width, height)

**2. Imshow for Grid Display**
```python
ax.imshow(grid_array, cmap=colormap, vmin=0, vmax=5)
```
- Displays a 2D array as an image
- `cmap`: Color mapping for values
- `vmin/vmax`: Value range for color scaling

**3. Grid Lines**
```python
ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
```
- Creates cell boundaries
- Minor ticks offset by 0.5 to center on cells

**4. Legends**
```python
from matplotlib.patches import Patch
legend = [Patch(facecolor='green', label='Start')]
ax.legend(handles=legend)
```
- Manual legend creation for custom colors
- Positioned outside plot area

## Code Walkthrough

### Grid Visualization Implementation

File: `src/pathfinding_lab/visualization/grid_plot.py`

**Step 1: Create Base Grid Array**

```python
vis_grid = np.zeros((grid.height, grid.width))
```

Start with a 2D NumPy array filled with zeros (empty cells).

**Step 2: Mark Obstacles**

```python
for obstacle in grid.obstacles:
    row, col = obstacle
    vis_grid[row, col] = 1  # 1 = obstacle
```

Set obstacle cells to value 1 for color mapping.

**Step 3: Overlay Visited Nodes**

```python
if result and result.visited_order:
    for pos in result.visited_order:
        row, col = pos
        if pos != start and pos != goal:
            vis_grid[row, col] = 2  # 2 = visited
```

Mark all visited nodes (except start/goal) with value 2.

**Step 4: Highlight the Path**

```python
if result and result.path:
    for pos in result.path:
        row, col = pos
        if pos != start and pos != goal:
            vis_grid[row, col] = 3  # 3 = path
```

Path gets value 3, overwriting visited markers.

**Step 5: Mark Start and Goal**

```python
start_row, start_col = start
goal_row, goal_col = goal
vis_grid[start_row, start_col] = 4  # 4 = start
vis_grid[goal_row, goal_col] = 5    # 5 = goal
```

Start and goal are marked last to ensure they're always visible.

**Step 6: Create Color Map**

```python
from matplotlib.colors import ListedColormap
colors = ['white', 'black', 'lightblue', 'yellow', 'green', 'red']
cmap = ListedColormap(colors)
```

Maps values 0-5 to specific colors:
- 0 → white (empty)
- 1 → black (obstacle)
- 2 → lightblue (visited)
- 3 → yellow (path)
- 4 → green (start)
- 5 → red (goal)

**Step 7: Display with Matplotlib**

```python
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(vis_grid, cmap=cmap, vmin=0, vmax=5)
```

The `imshow` function displays the grid array as an image with the custom color map.

**Step 8: Add Grid Lines**

```python
ax.set_xticks(np.arange(-0.5, grid.width, 1), minor=True)
ax.set_yticks(np.arange(-0.5, grid.height, 1), minor=True)
ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
```

Grid lines positioned between cells (offset by -0.5) create clear cell boundaries.

**Step 9: Add Title and Labels**

```python
title = f"{result.algorithm_name}\n"
title += f"Path Length: {result.path_length}, "
title += f"Cost: {result.path_cost:.2f}, "
title += f"Visited: {result.nodes_visited}, "
title += f"Time: {result.runtime_ms:.2f}ms"
ax.set_title(title)
```

Informative title showing all key metrics.

### Comparison Visualization

File: `src/pathfinding_lab/visualization/comparison_plot.py`

**Creating Comparison Bar Charts**:

```python
def create_comparison_plot(results: List[SearchResult]) -> plt.Figure:
    fig, axes = plt.subplots(1, 3, figsize=(12, 6))

    algorithms = [r.algorithm_name for r in results]
    nodes_visited = [r.nodes_visited for r in results]
    runtime_ms = [r.runtime_ms for r in results]
    path_costs = [r.path_cost if r.success else 0 for r in results]

    # Three subplots: nodes visited, runtime, path cost
    axes[0].bar(range(len(algorithms)), nodes_visited, color='skyblue')
    axes[1].bar(range(len(algorithms)), runtime_ms, color='lightcoral')
    axes[2].bar(range(len(algorithms)), path_costs, color='lightgreen')
```

**Key insights**:
- Three metrics side-by-side for easy comparison
- Different colors for each metric
- Short algorithm names on x-axis to fit
- Rotated labels for better readability

**Creating Comparison Tables**:

```python
def create_comparison_table(results: List[SearchResult]) -> pd.DataFrame:
    data = []
    for result in results:
        data.append({
            'Algorithm': result.algorithm_name,
            'Success': '✓' if result.success else '✗',
            'Path Length': result.path_length if result.success else 'N/A',
            'Path Cost': f"{result.path_cost:.2f}" if result.success else 'N/A',
            'Nodes Visited': result.nodes_visited,
            'Runtime (ms)': f"{result.runtime_ms:.2f}",
        })
    return pd.DataFrame(data)
```

Pandas DataFrames provide:
- Tabular output
- Easy CSV export
- Integration with Gradio tables
- Sorting and filtering capabilities

## Common Mistakes

### 1. Inverting Row/Column Coordinates

**Problem**: Matplotlib's `imshow` treats the first index as row (y-axis) and second as column (x-axis), which can be counterintuitive.

```python
# Wrong: might accidentally swap row and col
vis_grid[col, row] = value  # ❌

# Correct: row first, then column
vis_grid[row, col] = value  # ✅
```

**Solution**: Always use `(row, col)` indexing consistently throughout your code. Remember: `grid[y][x]` in matrix notation.

### 2. Forgetting to Handle Missing Paths

**Problem**: If pathfinding fails, `result.path` is empty, causing errors when iterating.

```python
# Dangerous: assumes path exists
for pos in result.path:
    vis_grid[row, col] = 3  # May crash if path is empty
```

**Solution**: Always check before iterating:

```python
if result and result.path:
    for pos in result.path:
        row, col = pos
        vis_grid[row, col] = 3
```

### 3. Overlapping Colors Making Start/Goal Invisible

**Problem**: If you mark visited nodes or path first, start and goal might be overwritten.

```python
# Wrong order
vis_grid[start_row, start_col] = 4  # Mark start
# Later...
vis_grid[start_row, start_col] = 2  # Oops, marked as visited!
```

**Solution**: Always mark start and goal LAST to ensure they're visible:

```python
# Correct order:
# 1. Mark obstacles
# 2. Mark visited nodes (skip start/goal)
# 3. Mark path (skip start/goal)
# 4. Mark start and goal last
```

### 4. Poor Color Contrast

**Problem**: Light colors on white background are hard to see.

```python
# Bad: light yellow on white background
colors = ['white', 'lightyellow', 'lightgray']  # ❌
```

**Solution**: Use colors with sufficient contrast:

```python
# Good: clear contrast
colors = ['white', 'black', 'lightblue', 'orange', 'green', 'red']  # ✅
```

Test your visualizations in grayscale to ensure clarity.

### 5. Grid Lines Not Aligned with Cells

**Problem**: Grid lines in the middle of cells instead of between them.

```python
# Wrong: lines through cell centers
ax.set_xticks(np.arange(0, width, 1))  # ❌
```

**Solution**: Offset ticks by -0.5 to place lines between cells:

```python
# Correct: lines between cells
ax.set_xticks(np.arange(-0.5, width, 1), minor=True)  # ✅
```

### 6. Figure Size Too Small for Large Grids

**Problem**: Large grids (50x50+) become unreadable at default size.

```python
# Too small for a 50x50 grid
fig, ax = plt.subplots(figsize=(6, 6))  # ❌
```

**Solution**: Scale figure size with grid dimensions:

```python
# Scale with grid size
size = max(10, min(grid.width, grid.height) / 5)
fig, ax = plt.subplots(figsize=(size, size))  # ✅
```

## Mini Project Task

### This Week's Challenge: Multi-Algorithm Visualization Dashboard

Create a comprehensive visualization tool that compares 4 algorithms side-by-side on the same grid.

### Requirements

1. **Generate a test grid**:
   - 30x30 grid with random obstacles (20% density)
   - Fixed start (5, 5) and goal (25, 25)
   - Use a fixed random seed for reproducibility

2. **Run four algorithms**:
   - BFS
   - Dijkstra
   - A* with Manhattan heuristic
   - A* with Octile heuristic

3. **Create a 2x2 subplot visualization**:
   - Each subplot shows one algorithm's result
   - Same color scheme across all subplots
   - Clear title showing algorithm name and metrics

4. **Add a comparison table below the plots**:
   - Algorithm name, path length, cost, visited nodes, runtime
   - Sort by number of nodes visited (most efficient first)

5. **Export results**:
   - Save the figure as `algorithm_comparison.png`
   - Save the comparison table as `results.csv`

### Steps

1. **Setup the grid and algorithms**

```python
import numpy as np
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms import bfs, dijkstra, astar
from pathfinding_lab.heuristics import manhattan_distance, octile_distance
from pathfinding_lab.visualization import create_grid_plot
import matplotlib.pyplot as plt

# Create grid
np.random.seed(42)
grid = Grid(30, 30)
grid.generate_random_obstacles(density=0.2)
start, goal = (5, 5), (25, 25)
```

2. **Run algorithms and collect results**

```python
results = []
results.append(bfs.breadth_first_search(grid, start, goal))
results.append(dijkstra.dijkstra(grid, start, goal))
results.append(astar.astar(grid, start, goal, manhattan_distance))
results.append(astar.astar(grid, start, goal, octile_distance))
```

3. **Create 2x2 subplot visualization**

```python
fig, axes = plt.subplots(2, 2, figsize=(16, 16))
axes = axes.flatten()

for idx, result in enumerate(results):
    # Use existing create_grid_plot or create subplot manually
    # Plot on axes[idx]
    pass
```

4. **Create comparison table and save**

```python
from pathfinding_lab.visualization import create_comparison_table

df = create_comparison_table(results)
df = df.sort_values('Nodes Visited')
print(df)
df.to_csv('results.csv', index=False)
plt.savefig('algorithm_comparison.png', dpi=150, bbox_inches='tight')
```

### Success Criteria

- ✅ Four algorithms visualized in 2x2 grid
- ✅ Each subplot clearly shows visited nodes and path
- ✅ Start (green) and goal (red) visible in all subplots
- ✅ Comparison table sorted by efficiency
- ✅ Outputs saved to files
- ✅ Results are reproducible (same seed gives same output)

### Expected Observations

After completing this project, you should observe:

1. **BFS explores uniformly** - circular expansion pattern
2. **Dijkstra similar to BFS on uniform cost grids**
3. **A* with Manhattan** - slightly more directed toward goal
4. **A* with Octile** - most efficient, fewest nodes visited
5. **All find same path length** on unweighted grids (if optimal)
6. **Runtime differences** are small but measurable

## Reflection Questions

1. **Why do we visualize visited nodes separately from the path?**
   - What insights does this provide about algorithm efficiency?
   - Can two algorithms find the same path but visit different numbers of nodes?

2. **How does color choice affect understanding?**
   - What happens if you use red for visited nodes and green for the path?
   - Why is consistency important across visualizations?

3. **What are the tradeoffs of visualization quality vs performance?**
   - At what grid size does matplotlib become slow?
   - When would you choose simpler visualizations?

4. **How would you visualize algorithm execution in real-time?**
   - What would an animation show that a static image doesn't?
   - How would you balance frame rate and smoothness?

5. **What other metrics could be visualized?**
   - How would you show heuristic values (h-scores)?
   - Could you visualize the frontier/open set at each step?

## Additional Resources

- **Matplotlib Documentation**: https://matplotlib.org/stable/tutorials/index.html
- **Choosing Colormaps**: https://matplotlib.org/stable/tutorials/colors/colormaps.html
- **Color Accessibility**: https://colorbrewer2.org/
- **Red Blob Games Visualization Examples**: https://www.redblobgames.com/pathfinding/a-star/introduction.html
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/index.html

## Next Week Preview

Next week, we'll build the **Gradio UI** that brings everything together:
- Interactive controls for grid configuration
- Algorithm and heuristic selectors
- Real-time visualization updates
- Metrics display
- Comparison mode
- Export functionality

You'll learn how to create a web-based interface that makes your pathfinding laboratory accessible to anyone with a browser!

---

**Continue to Week 8: Gradio UI →**
