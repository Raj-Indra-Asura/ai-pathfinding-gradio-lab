# Week 7: Solutions

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 6 Solutions](week_06_solutions.md)** | **📚 [Week 7 Documentation](../docs/week_07_visualization.md)** | **📝 [Week 7 Exercises](../exercises/week_07.md)** | **➡️ [Next: Week 8 Solutions](week_08_solutions.md)**

---

## Beginner Exercise Solution: Custom Color Scheme Visualizer

### Explanation

This exercise teaches you to customize matplotlib color schemes using `ListedColormap`. The key is understanding how to map numeric values (0-5) to color names, and how to create a flexible function that accepts user-defined color schemes.

**Key concepts**:
- Color mapping with `ListedColormap`
- Dictionary-based configuration
- Testing different themes for accessibility
- Saving matplotlib figures to files

### Code

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import Position
from pathfinding_lab.core.result import SearchResult
from typing import Dict


def visualize_with_colors(
    grid: Grid,
    start: Position,
    goal: Position,
    result: SearchResult,
    color_scheme: Dict[str, str]
) -> plt.Figure:
    """
    Create a grid visualization with custom colors.

    Args:
        grid: The grid to visualize
        start: Start position
        goal: Goal position
        result: Search result with path and visited nodes
        color_scheme: Dictionary mapping cell types to color names

    Returns:
        Matplotlib Figure object
    """
    # Create visualization grid
    vis_grid = np.zeros((grid.height, grid.width))

    # Mark obstacles
    for obstacle in grid.obstacles:
        row, col = obstacle
        vis_grid[row, col] = 1

    # Mark visited nodes (skip start and goal)
    if result and result.visited_order:
        for pos in result.visited_order:
            row, col = pos
            if pos != start and pos != goal:
                vis_grid[row, col] = 2

    # Mark path (skip start and goal)
    if result and result.path:
        for pos in result.path:
            row, col = pos
            if pos != start and pos != goal:
                vis_grid[row, col] = 3

    # Mark start and goal last to ensure visibility
    start_row, start_col = start
    goal_row, goal_col = goal
    vis_grid[start_row, start_col] = 4
    vis_grid[goal_row, goal_col] = 5

    # Create color map from scheme
    colors = [
        color_scheme['empty'],
        color_scheme['obstacle'],
        color_scheme['visited'],
        color_scheme['path'],
        color_scheme['start'],
        color_scheme['goal']
    ]
    cmap = ListedColormap(colors)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(vis_grid, cmap=cmap, vmin=0, vmax=5)

    # Add grid lines
    ax.set_xticks(np.arange(-0.5, grid.width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.height, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    ax.tick_params(which='minor', size=0)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_scheme['start'], label='Start'),
        Patch(facecolor=color_scheme['goal'], label='Goal'),
        Patch(facecolor=color_scheme['obstacle'], label='Obstacle'),
        Patch(facecolor=color_scheme['visited'], label='Visited'),
        Patch(facecolor=color_scheme['path'], label='Path'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

    # Add title
    if result and result.success:
        title = f"{result.algorithm_name}\nPath: {result.path_length} steps, Cost: {result.path_cost:.2f}"
    else:
        title = "No path found"
    ax.set_title(title)

    plt.tight_layout()
    return fig


# Test with three color schemes
def test_color_schemes():
    """Test function demonstrating three different color schemes."""
    from pathfinding_lab.algorithms.bfs import breadth_first_search

    # Create test grid
    np.random.seed(42)
    grid = Grid(20, 20)
    grid.generate_random_obstacles(density=0.15)
    start = (2, 2)
    goal = (18, 18)

    # Run BFS
    result = breadth_first_search(grid, start, goal)

    # Default scheme
    color_scheme_default = {
        'empty': 'white',
        'obstacle': 'black',
        'visited': 'lightblue',
        'path': 'yellow',
        'start': 'green',
        'goal': 'red'
    }
    fig1 = visualize_with_colors(grid, start, goal, result, color_scheme_default)
    fig1.savefig('visualization_default.png', dpi=150, bbox_inches='tight')
    print("✓ Saved visualization_default.png")

    # Dark theme
    color_scheme_dark = {
        'empty': 'darkgray',
        'obstacle': 'lightgray',
        'visited': 'cyan',
        'path': 'orange',
        'start': 'lime',
        'goal': 'hotpink'
    }
    fig2 = visualize_with_colors(grid, start, goal, result, color_scheme_dark)
    fig2.savefig('visualization_dark.png', dpi=150, bbox_inches='tight')
    print("✓ Saved visualization_dark.png")

    # Colorblind-friendly scheme
    color_scheme_accessible = {
        'empty': 'white',
        'obstacle': 'black',
        'visited': 'royalblue',
        'path': 'gold',
        'start': 'darkgreen',
        'goal': 'darkred'
    }
    fig3 = visualize_with_colors(grid, start, goal, result, color_scheme_accessible)
    fig3.savefig('visualization_accessible.png', dpi=150, bbox_inches='tight')
    print("✓ Saved visualization_accessible.png")

    plt.close('all')
    return [fig1, fig2, fig3]


if __name__ == "__main__":
    test_color_schemes()
```

### Key Concepts

- **Dictionary-based configuration**: Using dictionaries for flexible, user-customizable settings
- **ListedColormap**: Maps discrete values to specific colors
- **Color accessibility**: Dark themes and colorblind-friendly palettes improve usability
- **Legend positioning**: `bbox_to_anchor=(1, 1)` places legend outside plot area
- **File saving**: `savefig()` with `bbox_inches='tight'` prevents clipping

### Testing Advice

1. **Verify all three schemes**: Check that all three PNG files are created
2. **Inspect colors visually**: Open each PNG and verify colors match expectations
3. **Test with failed paths**: Try with unreachable goals to test error handling
4. **Test edge cases**: Try with grids where start==goal or no obstacles
5. **Accessibility check**: Convert to grayscale to verify sufficient contrast

## Intermediate Exercise Solution: Algorithm Animation Frame Exporter

### Explanation

This exercise creates an animation by exporting individual frames showing algorithm progression. Each frame captures the state after processing one node, allowing you to see exactly how the algorithm explores the search space step-by-step.

**Key concepts**:
- Iterating through `visited_order` for frame-by-frame execution
- Using a "current node" color to highlight active processing
- Zero-padding filenames for proper sorting
- Directory creation and management

### Code

```python
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import Position
from pathfinding_lab.core.result import SearchResult
from typing import List


def export_animation_frames(
    grid: Grid,
    start: Position,
    goal: Position,
    result: SearchResult,
    output_dir: str = 'frames'
) -> List[str]:
    """
    Export animation frames showing algorithm execution step-by-step.

    Args:
        grid: The grid being searched
        start: Start position
        goal: Goal position
        result: Search result with visited_order
        output_dir: Directory to save frames

    Returns:
        List of generated frame filenames
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Color scheme (7 colors: empty, obstacle, visited, current, path, start, goal)
    colors = ['white', 'black', 'lightblue', 'orange', 'yellow', 'green', 'red']
    cmap = ListedColormap(colors)

    frame_filenames = []

    if not result or not result.visited_order:
        print("No visited nodes to animate")
        return frame_filenames

    # Generate frames for each visited node
    visited_set = set()
    max_frames = min(len(result.visited_order), 100)  # Limit to 100 frames

    for i, current_pos in enumerate(result.visited_order[:max_frames]):
        # Create visualization grid
        vis_grid = np.zeros((grid.height, grid.width))

        # Mark obstacles
        for obstacle in grid.obstacles:
            row, col = obstacle
            vis_grid[row, col] = 1

        # Mark all visited nodes so far
        for visited_pos in visited_set:
            row, col = visited_pos
            if visited_pos != start and visited_pos != goal:
                vis_grid[row, col] = 2

        # Mark current node (if not start/goal)
        if current_pos != start and current_pos != goal:
            row, col = current_pos
            vis_grid[row, col] = 3  # Current node (orange)

        # Mark start and goal
        start_row, start_col = start
        goal_row, goal_col = goal
        vis_grid[start_row, start_col] = 5
        vis_grid[goal_row, goal_col] = 6

        # Create frame
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(vis_grid, cmap=cmap, vmin=0, vmax=6)

        # Grid lines
        ax.set_xticks(np.arange(-0.5, grid.width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, grid.height, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        ax.tick_params(which='minor', size=0)

        # Title
        ax.set_title(f"{result.algorithm_name} - Step {i+1}/{max_frames}\nNodes visited: {len(visited_set)+1}")

        # Save frame
        filename = os.path.join(output_dir, f"frame_{i:04d}.png")
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        plt.close(fig)

        frame_filenames.append(filename)
        visited_set.add(current_pos)

    # Generate final frame with complete path
    if result.path:
        vis_grid = np.zeros((grid.height, grid.width))

        # Mark obstacles
        for obstacle in grid.obstacles:
            row, col = obstacle
            vis_grid[row, col] = 1

        # Mark all visited nodes
        for visited_pos in visited_set:
            row, col = visited_pos
            if visited_pos != start and visited_pos != goal:
                vis_grid[row, col] = 2

        # Mark path
        for path_pos in result.path:
            row, col = path_pos
            if path_pos != start and path_pos != goal:
                vis_grid[row, col] = 4  # Path (yellow)

        # Mark start and goal
        vis_grid[start_row, start_col] = 5
        vis_grid[goal_row, goal_col] = 6

        # Create final frame
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(vis_grid, cmap=cmap, vmin=0, vmax=6)

        ax.set_xticks(np.arange(-0.5, grid.width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, grid.height, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        ax.tick_params(which='minor', size=0)

        ax.set_title(f"{result.algorithm_name} - Complete Path\nLength: {result.path_length}, Cost: {result.path_cost:.2f}")

        filename = os.path.join(output_dir, "frame_final.png")
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        plt.close(fig)

        frame_filenames.append(filename)

    print(f"✓ Generated {len(frame_filenames)} frames in {output_dir}/")
    return frame_filenames


def test_animation_export():
    """Test animation frame export."""
    from pathfinding_lab.algorithms.astar import astar
    from pathfinding_lab.heuristics.manhattan import manhattan_distance

    # Create test grid
    np.random.seed(42)
    grid = Grid(15, 15)
    grid.generate_random_obstacles(density=0.20)
    start = (2, 2)
    goal = (12, 12)

    # Run A*
    result = astar(grid, start, goal, manhattan_distance)

    # Export frames
    frames = export_animation_frames(grid, start, goal, result, output_dir='frames')

    print(f"\nAnalysis:")
    print(f"1. Total frames generated: {len(frames)}")

    # Find when goal was first reached
    goal_frame = -1
    for i, pos in enumerate(result.visited_order):
        if pos == goal:
            goal_frame = i
            break

    if goal_frame >= 0:
        print(f"2. Goal first reached at frame: {goal_frame}")
        print(f"3. Additional frames after reaching goal: {len(result.visited_order) - goal_frame - 1}")

    print(f"4. Exploration pattern: A* explores nodes in a directed manner toward the goal")

    return frames


if __name__ == "__main__":
    frames = test_animation_export()

    # Bonus: Create GIF (requires imageio)
    try:
        import imageio
        images = []
        for filename in sorted(frames):
            images.append(imageio.imread(filename))
        imageio.mimsave('algorithm_animation.gif', images, fps=10)
        print("✓ Created algorithm_animation.gif")
    except ImportError:
        print("Install imageio to create GIF: pip install imageio")
```

### Key Concepts

- **Frame-by-frame visualization**: Each frame captures algorithm state at one step
- **Current node highlighting**: Orange color shows which node is being processed
- **Visited set accumulation**: Builds up visited nodes over frames
- **Zero-padded filenames**: `f"{i:04d}"` ensures proper alphabetical sorting
- **Frame limiting**: Cap at 100 frames to prevent excessive output

### Testing Advice

1. **Verify frame count**: Should match visited nodes (up to 100)
2. **Check frame order**: Frames should be numbered sequentially
3. **View animation**: Use image viewer or create GIF to see progression
4. **Test with different algorithms**: Compare BFS (uniform expansion) vs A* (directed)
5. **Measure directory size**: Large grids can create many large files

## Advanced Exercise Solution: Multi-Metric Comparison Dashboard

### Explanation

This comprehensive dashboard combines multiple visualization types (grid plots, bar charts, scatter plots, tables) into a single figure for algorithm comparison. The key is using matplotlib's layout management to create a professional multi-panel visualization.

**Key concepts**:
- Complex subplot layouts with `GridSpec`
- Storing and managing multiple algorithm results
- Calculating rankings across metrics
- Combining different plot types in one figure

### Code

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.result import SearchResult
from typing import List, Dict, Tuple


class VisualizationDashboard:
    """Comprehensive dashboard for algorithm comparison."""

    def __init__(self, grid: Grid, start: tuple, goal: tuple):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.results: List[SearchResult] = []
        self.algorithm_names: List[str] = []

    def add_result(self, algorithm_name: str, result: SearchResult):
        """Add an algorithm result to the dashboard."""
        self.algorithm_names.append(algorithm_name)
        self.results.append(result)

    def generate_grid_comparison(self, axes: List[plt.Axes]):
        """Generate grid visualizations for all algorithms."""
        colors = ['white', 'black', 'lightblue', 'yellow', 'green', 'red']
        cmap = ListedColormap(colors)

        for idx, (ax, result, name) in enumerate(zip(axes, self.results, self.algorithm_names)):
            # Create visualization grid
            vis_grid = np.zeros((self.grid.height, self.grid.width))

            # Mark obstacles
            for obstacle in self.grid.obstacles:
                row, col = obstacle
                vis_grid[row, col] = 1

            # Mark visited nodes
            if result and result.visited_order:
                for pos in result.visited_order:
                    row, col = pos
                    if pos != self.start and pos != self.goal:
                        vis_grid[row, col] = 2

            # Mark path
            if result and result.path:
                for pos in result.path:
                    row, col = pos
                    if pos != self.start and pos != self.goal:
                        vis_grid[row, col] = 3

            # Mark start and goal
            start_row, start_col = self.start
            goal_row, goal_col = self.goal
            vis_grid[start_row, start_col] = 4
            vis_grid[goal_row, goal_col] = 5

            # Display
            ax.imshow(vis_grid, cmap=cmap, vmin=0, vmax=5)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(f"{name}\nVisited: {result.nodes_visited}", fontsize=10)

    def generate_metric_plots(self, axes: List[plt.Axes]):
        """Generate bar charts for metrics."""
        nodes_visited = [r.nodes_visited for r in self.results]
        runtime_ms = [r.runtime_ms for r in self.results]
        path_costs = [r.path_cost if r.success else 0 for r in self.results]
        path_lengths = [r.path_length if r.success else 0 for r in self.results]

        metrics = [
            (nodes_visited, 'Nodes Visited', 'skyblue'),
            (runtime_ms, 'Runtime (ms)', 'lightcoral'),
            (path_costs, 'Path Cost', 'lightgreen'),
            (path_lengths, 'Path Length', 'plum')
        ]

        for ax, (data, title, color) in zip(axes, metrics):
            ax.bar(range(len(self.algorithm_names)), data, color=color)
            ax.set_title(title, fontsize=10)
            ax.set_xticks(range(len(self.algorithm_names)))
            ax.set_xticklabels([n.split()[0] for n in self.algorithm_names],
                              rotation=45, ha='right', fontsize=8)
            ax.set_ylabel('Count' if 'Length' in title else 'Value', fontsize=8)

    def generate_efficiency_scatter(self, ax: plt.Axes):
        """Generate scatter plot of nodes_visited vs runtime."""
        nodes_visited = [r.nodes_visited for r in self.results]
        runtime_ms = [r.runtime_ms for r in self.results]

        ax.scatter(nodes_visited, runtime_ms, s=100, alpha=0.6, c='coral')

        for i, name in enumerate(self.algorithm_names):
            ax.annotate(name.split()[0],
                       (nodes_visited[i], runtime_ms[i]),
                       fontsize=8, ha='right')

        ax.set_xlabel('Nodes Visited', fontsize=10)
        ax.set_ylabel('Runtime (ms)', fontsize=10)
        ax.set_title('Efficiency: Nodes vs Runtime', fontsize=10)
        ax.grid(True, alpha=0.3)

    def generate_detailed_table(self) -> pd.DataFrame:
        """Generate detailed comparison table with rankings."""
        data = []

        for result, name in zip(self.results, self.algorithm_names):
            data.append({
                'Algorithm': name,
                'Success': '✓' if result.success else '✗',
                'Path Length': result.path_length if result.success else 'N/A',
                'Path Cost': f"{result.path_cost:.2f}" if result.success else 'N/A',
                'Nodes Visited': result.nodes_visited,
                'Runtime (ms)': f"{result.runtime_ms:.2f}",
            })

        df = pd.DataFrame(data)

        # Add rankings
        df['Efficiency Rank'] = df['Nodes Visited'].rank().astype(int)
        df['Speed Rank'] = pd.to_numeric(df['Runtime (ms)']).rank().astype(int)

        return df

    def export_dashboard(self, filename: str = 'dashboard.png'):
        """Export complete dashboard as single image."""
        # Create figure with custom layout
        fig = plt.figure(figsize=(18, 12))
        gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.3)

        # Grid comparisons (top 2 rows)
        grid_axes = []
        for i in range(6):
            row = i // 3
            col = i % 3
            ax = fig.add_subplot(gs[row, col])
            grid_axes.append(ax)

        if len(self.results) <= 6:
            self.generate_grid_comparison(grid_axes[:len(self.results)])

        # Metric plots (row 3)
        metric_axes = []
        for col in range(3):
            ax = fig.add_subplot(gs[2, col])
            metric_axes.append(ax)

        # Efficiency scatter (row 3, col 3 - spans remaining space)
        scatter_ax = fig.add_subplot(gs[2, 2])

        self.generate_metric_plots(metric_axes[:3])
        self.generate_efficiency_scatter(scatter_ax)

        # Table (row 4, spans all columns)
        table_ax = fig.add_subplot(gs[3, :])
        table_ax.axis('off')

        df = self.generate_detailed_table()
        table_data = df.values.tolist()
        table = table_ax.table(cellText=table_data, colLabels=df.columns,
                              cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2)

        # Overall title
        fig.suptitle(f'Algorithm Comparison Dashboard\nGrid: {self.grid.width}x{self.grid.height}',
                    fontsize=14, fontweight='bold')

        # Save
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Dashboard saved to {filename}")
        plt.close(fig)

        return filename

    def generate_efficiency_report(self) -> str:
        """Generate text report of efficiency analysis."""
        df = self.generate_detailed_table()

        report = "Efficiency Analysis Report\n"
        report += "=" * 50 + "\n\n"

        # Most efficient (fewest nodes)
        efficient_idx = df['Nodes Visited'].idxmin()
        report += f"Most Efficient: {df.loc[efficient_idx, 'Algorithm']}\n"
        report += f"  Nodes visited: {df.loc[efficient_idx, 'Nodes Visited']}\n\n"

        # Fastest
        fastest_idx = pd.to_numeric(df['Runtime (ms)']).idxmin()
        report += f"Fastest: {df.loc[fastest_idx, 'Algorithm']}\n"
        report += f"  Runtime: {df.loc[fastest_idx, 'Runtime (ms)']} ms\n\n"

        # Best path (if applicable)
        if df['Path Length'].dtype != object:
            best_path_idx = df['Path Length'].idxmin()
            report += f"Shortest Path: {df.loc[best_path_idx, 'Algorithm']}\n"
            report += f"  Path length: {df.loc[best_path_idx, 'Path Length']} steps\n\n"

        # Overall score (weighted combination)
        df['Overall Score'] = (
            df['Efficiency Rank'] * 0.4 +
            df['Speed Rank'] * 0.3 +
            df['Efficiency Rank'] * 0.3
        )
        best_overall_idx = df['Overall Score'].idxmin()
        report += f"Best Overall: {df.loc[best_overall_idx, 'Algorithm']}\n"
        report += f"  (Weighted score: {df.loc[best_overall_idx, 'Overall Score']:.2f})\n"

        return report


def test_dashboard():
    """Test the visualization dashboard."""
    from pathfinding_lab.algorithms import bfs, dfs, dijkstra, greedy_best_first, astar
    from pathfinding_lab.heuristics import manhattan_distance, octile_distance

    # Create test grid
    np.random.seed(42)
    grid = Grid(25, 25)
    grid.generate_random_obstacles(density=0.20)
    start = (2, 2)
    goal = (22, 22)

    # Create dashboard
    dashboard = VisualizationDashboard(grid, start, goal)

    # Run algorithms
    print("Running algorithms...")
    dashboard.add_result("BFS", bfs.breadth_first_search(grid, start, goal))
    dashboard.add_result("DFS", dfs.depth_first_search(grid, start, goal))
    dashboard.add_result("Dijkstra", dijkstra.dijkstra(grid, start, goal))
    dashboard.add_result("Greedy", greedy_best_first.greedy_best_first_search(
        grid, start, goal, manhattan_distance))
    dashboard.add_result("A* (Manhattan)", astar.astar(grid, start, goal, manhattan_distance))
    dashboard.add_result("A* (Octile)", astar.astar(grid, start, goal, octile_distance))

    # Generate dashboard
    dashboard.export_dashboard('algorithm_dashboard.png')

    # Generate report
    report = dashboard.generate_efficiency_report()
    print("\n" + report)

    # Save report
    with open('efficiency_report.txt', 'w') as f:
        f.write(report)
    print("✓ Report saved to efficiency_report.txt")


if __name__ == "__main__":
    test_dashboard()
```

### Key Concepts

- **GridSpec layout**: Flexible subplot arrangement with different sizes
- **Multi-metric comparison**: Visualizing multiple dimensions of algorithm performance
- **Ranking systems**: Computing relative performance across algorithms
- **Professional dashboards**: Combining plots, tables, and text in one figure
- **Weighted scoring**: Combining multiple metrics into overall performance score

### Testing Advice

1. **Verify all 6 algorithms**: Check that all grid visualizations appear
2. **Check metric consistency**: Ensure bar chart values match table values
3. **Inspect scatter plot**: Should show correlation between nodes and runtime
4. **Validate rankings**: Verify efficiency and speed rankings are correct
5. **Test with different grids**: Try open, maze, and weighted terrain

## Debugging Challenge Solution: Broken Visualization Code

### Bugs Found and Fixes

**Bug 1: Grid Dimensions Swapped**
- **Problem**: `vis_grid = np.zeros((grid.width, grid.height))`
- **Fix**: `vis_grid = np.zeros((grid.height, grid.width))`
- **Why**: NumPy arrays use (rows, columns) = (height, width) indexing

**Bug 2: No Null Checks**
- **Problem**: Direct access to `result.visited_order` without checking if result exists
- **Fix**: `if result and result.visited_order:`
- **Why**: Prevents crashes when pathfinding fails or result is None

**Bug 3: Path Overwrites Start/Goal**
- **Problem**: Marking path without checking if position is start or goal
- **Fix**: `if pos != start and pos != goal:` before marking
- **Why**: Ensures start and goal remain visible

**Bug 4: Missing Color**
- **Problem**: Only 5 colors in list, need 6 for values 0-5
- **Fix**: `colors = ['white', 'black', 'lightblue', 'yellow', 'green', 'red']`
- **Why**: Each value (0-5) needs corresponding color

**Bug 5: Grid Lines Through Centers**
- **Problem**: `ax.set_xticks(np.arange(0, grid.width, 1))` places lines at cell centers
- **Fix**: `ax.set_xticks(np.arange(-0.5, grid.width, 1), minor=True)`
- **Why**: Offset by -0.5 places lines between cells, not through them

**Bug 6: No Legend**
- **Problem**: Missing legend makes colors unclear
- **Fix**: Add legend with `matplotlib.patches.Patch` objects
- **Why**: Users need to understand what each color represents

### Complete Fixed Code

See the corrected code structure provided in the exercise. All bugs are fixed by:
1. Correcting array dimensions
2. Adding null/existence checks
3. Skipping start/goal when marking visited/path
4. Including all 6 colors
5. Using minor ticks with -0.5 offset
6. Adding complete legend

---

**Next: Week 8 Gradio UI →**

---

**📝 [Back to Week 7 Exercises](../exercises/week_07.md)** | **📚 [Week 7 Documentation](../docs/week_07_visualization.md)** | **➡️ [Next: Week 8 Solutions](week_08_solutions.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
