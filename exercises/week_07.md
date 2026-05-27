# Week 7: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 6 Exercises](week_06.md)** | **📚 [Week 7 Documentation](../docs/week_07_visualization.md)** | **✅ [Week 7 Solutions](../solutions/week_07_solutions.md)** | **➡️ [Next: Week 8 Exercises](week_08.md)**

---

## Beginner Exercise: Custom Color Scheme Visualizer

### Task

Create a function that allows users to customize the color scheme for grid visualization. Your function should generate a grid plot with user-specified colors for each cell type.

### Requirements

- Write a function `visualize_with_colors(grid, start, goal, result, color_scheme: dict) -> Figure`
- The `color_scheme` dictionary should map cell types to color names:
  - `'empty'`, `'obstacle'`, `'visited'`, `'path'`, `'start'`, `'goal'`
- Generate a test grid (20x20) with 15% obstacle density
- Run BFS on the grid
- Create three different visualizations with different color schemes:
  - Default scheme (white, black, lightblue, yellow, green, red)
  - Dark theme (dark gray, light gray, cyan, orange, lime, pink)
  - Colorblind-friendly (white, black, blue, yellow, darkgreen, darkred)
- Save all three visualizations as separate PNG files

### Hints

- Use `ListedColormap` from `matplotlib.colors`
- Map color names in order: empty, obstacle, visited, path, start, goal
- Test with matplotlib's named colors: https://matplotlib.org/stable/gallery/color/named_colors.html
- Ensure sufficient contrast between adjacent colors
- Use `plt.savefig()` to save each visualization

### Example Usage

```python
color_scheme_default = {
    'empty': 'white',
    'obstacle': 'black',
    'visited': 'lightblue',
    'path': 'yellow',
    'start': 'green',
    'goal': 'red'
}

fig = visualize_with_colors(grid, start, goal, result, color_scheme_default)
fig.savefig('visualization_default.png', dpi=150, bbox_inches='tight')
```

### Success Criteria

- ✅ Function accepts custom color scheme dictionary
- ✅ All six cell types are properly colored
- ✅ Three different color schemes implemented
- ✅ Visualizations saved as PNG files
- ✅ All visualizations clearly show path and visited nodes

## Intermediate Exercise: Algorithm Animation Frame Exporter

### Task

Create a tool that exports individual frames showing the step-by-step execution of a pathfinding algorithm. Each frame should show the state of the grid after processing each node in the visited_order list.

### Requirements

- Write a function `export_animation_frames(grid, start, goal, result, output_dir='frames') -> List[str]`
- Create a separate PNG file for each step in the algorithm's execution
- Frame naming: `frame_0000.png`, `frame_0001.png`, etc.
- Each frame should show:
  - All visited nodes up to that point
  - Current node being processed (highlighted differently)
  - Start and goal positions
  - Obstacles
- Return list of generated filenames
- Include a summary frame at the end showing the final path
- Test with A* on a 15x15 grid with moderate obstacles

### Hints

- Iterate through `result.visited_order` to get node-by-node execution
- Use a different color for the "current" node (e.g., orange)
- Zero-pad frame numbers: `f"frame_{i:04d}.png"` gives `frame_0042.png`
- Create output directory if it doesn't exist: `os.makedirs(output_dir, exist_ok=True)`
- For final frame, overlay the complete path on top of visited nodes
- Consider limiting to first 100 frames for large grids

### Example Output Structure

```
frames/
├── frame_0000.png  # Start position only
├── frame_0001.png  # First node explored
├── frame_0002.png  # Second node explored
├── ...
├── frame_0150.png  # Last node explored
└── frame_final.png # Complete path shown
```

### Analysis Questions

After generating frames, answer:
1. How many frames were generated?
2. At which frame does the algorithm first reach the goal?
3. How many additional frames are processed after reaching the goal?
4. What pattern do you observe in how the algorithm explores the space?

### Bonus Challenge

Create a simple script to combine all frames into a video using `imageio`:

```python
import imageio

frames = []
for filename in sorted(frame_filenames):
    frames.append(imageio.imread(filename))
imageio.mimsave('algorithm_animation.gif', frames, fps=10)
```

## Advanced Exercise: Multi-Metric Comparison Dashboard

### Task

Build a comprehensive dashboard that compares multiple algorithms across multiple metrics with multiple visualization types. Your dashboard should provide both visual and tabular comparisons.

### Requirements

- Create a class `VisualizationDashboard` with methods:
  - `add_result(algorithm_name, result)` - Store algorithm results
  - `generate_grid_comparison()` - 2x3 subplot showing all algorithms' paths
  - `generate_metric_plots()` - Bar charts for 4+ metrics
  - `generate_efficiency_scatter()` - Scatter plot of nodes_visited vs runtime
  - `generate_detailed_table()` - Formatted comparison table with rankings
  - `export_dashboard(filename)` - Save complete dashboard as single image
- Test with 6 algorithms:
  - BFS, DFS, Dijkstra, Greedy Best-First, A* (Manhattan), A* (Octile)
- Use a consistent 25x25 grid with 20% obstacles
- Dashboard should fit on a single page when saved

### Hints

- Use `plt.subplots()` with a complex layout (e.g., `GridSpec`)
- Calculate rankings: 1st, 2nd, 3rd for each metric
- Color-code rankings: gold, silver, bronze
- Use `plt.tight_layout()` to prevent overlapping
- Consider using `fig.suptitle()` for overall dashboard title
- Normalize metrics for fair comparison (e.g., min-max scaling)

### Dashboard Layout Suggestion

```
+------------------------+------------------------+------------------------+
|   BFS Grid Result      |  Dijkstra Grid Result  |  Greedy Grid Result   |
+------------------------+------------------------+------------------------+
| A* (Man.) Grid Result  | A* (Oct.) Grid Result  |  DFS Grid Result      |
+------------------------+------------------------+------------------------+
|           Nodes Visited Bar Chart                |  Runtime Bar Chart    |
+--------------------------------------------------+-----------------------+
|           Path Cost Bar Chart                    | Efficiency Scatter    |
+--------------------------------------------------+-----------------------+
|                    Detailed Comparison Table                            |
+-------------------------------------------------------------------------+
```

### Success Criteria

- ✅ Dashboard displays 6 algorithm results
- ✅ Grid visualizations show clear differences in exploration patterns
- ✅ Bar charts compare at least 4 metrics
- ✅ Scatter plot shows relationship between two metrics
- ✅ Table includes rankings for each metric
- ✅ Entire dashboard saved as single high-resolution image
- ✅ Dashboard is readable and professionally formatted

### Bonus Analysis

Add a method `generate_efficiency_report()` that returns a string containing:
- Most efficient algorithm (fewest nodes visited)
- Fastest algorithm (lowest runtime)
- Most memory-efficient (fewest nodes in path)
- Best overall (weighted score combining multiple metrics)

## Debugging Challenge: Broken Visualization Code

### Buggy Code

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.result import SearchResult


def buggy_visualize_path(grid, start, goal, result):
    """Visualization with multiple bugs."""

    # Bug 1: Wrong grid dimensions (swapped height and width)
    vis_grid = np.zeros((grid.width, grid.height))

    # Mark obstacles
    for obstacle in grid.obstacles:
        row, col = obstacle
        vis_grid[row, col] = 1

    # Bug 2: Not checking if result exists or has visited_order
    for pos in result.visited_order:
        row, col = pos
        vis_grid[row, col] = 2

    # Bug 3: Path overwrites start and goal
    for pos in result.path:
        row, col = pos
        vis_grid[row, col] = 3

    # Mark start and goal (but they might be overwritten above)
    start_row, start_col = start
    goal_row, goal_col = goal
    vis_grid[start_row, start_col] = 4
    vis_grid[goal_row, goal_col] = 5

    # Bug 4: Color list has wrong number of colors (only 5, need 6)
    colors = ['white', 'black', 'lightblue', 'yellow', 'green']
    cmap = ListedColormap(colors)

    # Bug 5: Grid lines not offset properly
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(vis_grid, cmap=cmap, vmin=0, vmax=5)

    # Grid lines in wrong positions
    ax.set_xticks(np.arange(0, grid.width, 1))
    ax.set_yticks(np.arange(0, grid.height, 1))
    ax.grid(which='major', color='gray', linestyle='-', linewidth=0.5)

    # Bug 6: Legend missing
    ax.set_title("Path Visualization")

    return fig


# Test code
grid = Grid(20, 20)
grid.generate_random_obstacles(density=0.15)
start = (2, 2)
goal = (18, 18)

from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance

result = astar(grid, start, goal, manhattan_distance)

# This will have bugs!
fig = buggy_visualize_path(grid, start, goal, result)
plt.savefig('buggy_visualization.png')
plt.show()
```

### Expected Behavior

The visualization should:
1. Display a properly-sized grid matching the Grid dimensions
2. Handle missing results gracefully (check before accessing)
3. Keep start and goal visible at all times
4. Use all 6 colors correctly
5. Show grid lines between cells (not through centers)
6. Include a clear legend

### Bugs to Find and Fix

1. **Bug 1**: Grid dimensions swapped - should be `(height, width)`, not `(width, height)`
2. **Bug 2**: No null checks - crashes if `result` is None or `visited_order` is empty
3. **Bug 3**: Path overwrites start/goal - should skip start and goal when marking path
4. **Bug 4**: Missing color in list - needs 6 colors (0-5), only has 5
5. **Bug 5**: Grid lines through cell centers - need offset by -0.5 and use minor ticks
6. **Bug 6**: No legend - should include legend showing what each color represents

### Hints

- Test with a successful result and a failed result (no path found)
- Check array dimensions: `vis_grid.shape` should match `(grid.height, grid.width)`
- Verify start and goal are always visible after all marking
- Count colors: 6 values (0-5) need 6 colors
- Grid lines should form cell boundaries, not cut through cells
- Use `matplotlib.patches.Patch` to create legend

### Corrected Code Structure

```python
def fixed_visualize_path(grid, start, goal, result):
    # Fix 1: Correct dimensions
    vis_grid = np.zeros((grid.height, grid.width))

    # Mark obstacles (unchanged)
    for obstacle in grid.obstacles:
        row, col = obstacle
        vis_grid[row, col] = 1

    # Fix 2: Check result exists and has data
    if result and result.visited_order:
        for pos in result.visited_order:
            row, col = pos
            if pos != start and pos != goal:  # Fix 3: Skip start/goal
                vis_grid[row, col] = 2

    # Fix 3: Skip start and goal when marking path
    if result and result.path:
        for pos in result.path:
            row, col = pos
            if pos != start and pos != goal:
                vis_grid[row, col] = 3

    # Mark start and goal (now they won't be overwritten)
    start_row, start_col = start
    goal_row, goal_col = goal
    vis_grid[start_row, start_col] = 4
    vis_grid[goal_row, goal_col] = 5

    # Fix 4: All 6 colors
    colors = ['white', 'black', 'lightblue', 'yellow', 'green', 'red']
    cmap = ListedColormap(colors)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(vis_grid, cmap=cmap, vmin=0, vmax=5)

    # Fix 5: Offset grid lines by -0.5 and use minor ticks
    ax.set_xticks(np.arange(-0.5, grid.width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.height, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    ax.tick_params(which='minor', size=0)

    # Fix 6: Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='Start'),
        Patch(facecolor='red', label='Goal'),
        Patch(facecolor='black', label='Obstacle'),
        Patch(facecolor='lightblue', label='Visited'),
        Patch(facecolor='yellow', label='Path'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

    ax.set_title("Path Visualization")
    plt.tight_layout()

    return fig
```

### Testing Your Fix

Test your corrected code with:
1. A successful pathfinding result
2. A failed result (no path exists due to obstacles)
3. A result with empty visited_order
4. Different grid sizes (10x10, 50x50)
5. Save and visually inspect the output

---

**See solutions/week_07_solutions.md for complete answers and explanations**

---

**✅ [See Solutions](../solutions/week_07_solutions.md)** | **📚 [Back to Week 7 Docs](../docs/week_07_visualization.md)** | **➡️ [Next: Week 8 Exercises](week_08.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
