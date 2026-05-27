# Week 8 Solutions: Building Interactive UIs with Gradio

## Exercise 1 Solution: Basic Gradio Interface (Beginner)

### Explanation

This solution creates a simple Gradio interface for running BFS on a pathfinding grid. The key components are:

1. **Global state management** using `current_grid` to persist the grid between function calls
2. **Grid generation** that creates obstacles and visualizes the initial grid
3. **Algorithm execution** that runs BFS and displays the results
4. **Gradio layout** with controls on the left and visualization on the right

The interface provides a minimal but functional UI for pathfinding visualization.

### Code

```python
import gradio as gr
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.visualization.grid_plot import create_grid_plot

# Global state
current_grid = None

def generate_grid(width, height, obstacle_density):
    """Generate a new grid with obstacles."""
    global current_grid

    # Convert to int and create grid
    current_grid = Grid(
        width=int(width),
        height=int(height),
        obstacle_density=obstacle_density
    )

    # Use default start/goal positions (top-left to bottom-right)
    start = (0, 0)
    goal = (int(height) - 1, int(width) - 1)

    # Generate obstacles (avoiding start and goal)
    current_grid.generate_obstacles(start, goal)

    # Create visualization
    fig = create_grid_plot(current_grid, start, goal)

    status_msg = f"Grid generated: {int(width)}x{int(height)} with {len(current_grid.obstacles)} obstacles"
    return fig, status_msg

def run_bfs_algorithm(start_row, start_col, goal_row, goal_col):
    """Run BFS on the current grid."""
    global current_grid

    # Check if grid exists
    if current_grid is None:
        return None, "Please generate a grid first!"

    # Convert to int and create position tuples
    start = (int(start_row), int(start_col))
    goal = (int(goal_row), int(goal_col))

    # Run BFS
    result = bfs(current_grid, start, goal)

    # Create visualization with result
    fig = create_grid_plot(current_grid, start, goal, result)

    # Create status message
    if result.success:
        status_msg = f"Path found! Length: {result.path_length}, Nodes visited: {result.nodes_visited}"
    else:
        status_msg = f"No path found. Nodes visited: {result.nodes_visited}"

    return fig, status_msg

def create_interface():
    """Create the Gradio interface."""
    with gr.Blocks(title="BFS Pathfinding") as demo:
        gr.Markdown("# BFS Pathfinding Visualization")
        gr.Markdown("Generate a grid with obstacles and run BFS to find a path.")

        with gr.Row():
            # Left column: Controls
            with gr.Column(scale=1):
                gr.Markdown("### Grid Configuration")
                width = gr.Slider(10, 50, value=20, step=1, label="Width")
                height = gr.Slider(10, 50, value=20, step=1, label="Height")
                obstacle_density = gr.Slider(0.0, 0.5, value=0.2, step=0.05, label="Obstacle Density")

                gr.Markdown("### Positions")
                with gr.Row():
                    start_row = gr.Number(value=0, label="Start Row", precision=0)
                    start_col = gr.Number(value=0, label="Start Col", precision=0)
                with gr.Row():
                    goal_row = gr.Number(value=19, label="Goal Row", precision=0)
                    goal_col = gr.Number(value=19, label="Goal Col", precision=0)

                gr.Markdown("### Actions")
                generate_btn = gr.Button("Generate Grid", variant="secondary")
                run_btn = gr.Button("Run BFS", variant="primary")

            # Right column: Visualization
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="Grid Visualization")
                status_output = gr.Textbox(label="Status", lines=2)

        # Connect button events
        generate_btn.click(
            fn=generate_grid,
            inputs=[width, height, obstacle_density],
            outputs=[plot_output, status_output]
        )

        run_btn.click(
            fn=run_bfs_algorithm,
            inputs=[start_row, start_col, goal_row, goal_col],
            outputs=[plot_output, status_output]
        )

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
```

### Key Concepts

- **Global state management**: Using `global current_grid` to maintain state between function calls
- **Type conversion**: Converting slider values (floats) to integers for grid dimensions
- **Error handling**: Checking if grid exists before running algorithm
- **Gradio layout**: Using `gr.Row()` and `gr.Column()` to create a two-column layout
- **Event handlers**: Connecting button clicks to Python functions with inputs and outputs
- **Component types**: Using `gr.Slider()`, `gr.Number()`, `gr.Button()`, `gr.Plot()`, and `gr.Textbox()`

### Testing Advice

1. **Test grid generation**: Generate multiple grids with different parameters to verify obstacles appear correctly
2. **Test BFS execution**: Run BFS with different start/goal positions
3. **Test error handling**: Try running BFS before generating a grid (should show error message)
4. **Test edge cases**: Try start/goal at grid boundaries (0,0) and (19,19)
5. **Test visualization**: Verify that obstacles, visited nodes, and path are colored correctly

---

## Exercise 2 Solution: Multi-Algorithm Selector with State Management (Intermediate)

### Explanation

This solution extends the basic interface to support all 6 pathfinding algorithms with proper state management. Key features:

1. **Algorithm selection** using a dropdown menu
2. **Conditional heuristic selection** that appears only for A* and Greedy algorithms
3. **Movement mode** selection (4-directional vs 8-directional)
4. **Input validation** to ensure grid exists and positions are within bounds
5. **Comprehensive metrics** displayed in a pandas DataFrame

The interface provides a complete pathfinding laboratory experience.

### Code

```python
import gradio as gr
import pandas as pd
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.algorithms.dfs import dfs
from pathfinding_lab.algorithms.dijkstra import dijkstra
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.algorithms.greedy_best_first import greedy_best_first
from pathfinding_lab.algorithms.bidirectional_bfs import bidirectional_bfs
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.heuristics.euclidean import euclidean_distance
from pathfinding_lab.heuristics.octile import octile_distance
from pathfinding_lab.heuristics.chebyshev import chebyshev_distance
from pathfinding_lab.visualization.grid_plot import create_grid_plot

current_grid = None

def get_heuristic(heuristic_name):
    """Map heuristic name to function."""
    heuristic_map = {
        "Manhattan": manhattan_distance,
        "Euclidean": euclidean_distance,
        "Octile": octile_distance,
        "Chebyshev": chebyshev_distance
    }
    return heuristic_map.get(heuristic_name, manhattan_distance)

def generate_grid(width, height, obstacle_density, movement_mode, seed):
    """Generate grid with movement mode."""
    global current_grid

    # Convert movement_mode string to MovementMode enum
    movement = MovementMode.FOUR_DIRECTIONAL if movement_mode == "4-directional" else MovementMode.EIGHT_DIRECTIONAL

    # Create grid with movement mode and random seed
    current_grid = Grid(
        width=int(width),
        height=int(height),
        obstacle_density=obstacle_density,
        movement_mode=movement,
        random_seed=int(seed) if seed else None
    )

    # Generate obstacles
    start = (0, 0)
    goal = (int(height) - 1, int(width) - 1)
    current_grid.generate_obstacles(start, goal)

    # Create visualization
    fig = create_grid_plot(current_grid, start, goal)

    status_msg = f"Grid generated: {int(width)}x{int(height)}, {movement_mode}, {len(current_grid.obstacles)} obstacles"
    return fig, status_msg

def run_selected_algorithm(algorithm, heuristic_name, start_row, start_col, goal_row, goal_col):
    """Run the selected algorithm on the current grid."""
    global current_grid

    # Validate that grid exists
    if current_grid is None:
        return None, None, "Please generate a grid first!"

    # Convert to integers
    start = (int(start_row), int(start_col))
    goal = (int(goal_row), int(goal_col))

    # Validate start and goal positions are within bounds
    if not (0 <= start[0] < current_grid.height and 0 <= start[1] < current_grid.width):
        return None, None, f"Start position {start} is outside grid bounds!"
    if not (0 <= goal[0] < current_grid.height and 0 <= goal[1] < current_grid.width):
        return None, None, f"Goal position {goal} is outside grid bounds!"

    # Use if-elif to select algorithm
    if algorithm == "BFS":
        result = bfs(current_grid, start, goal)
    elif algorithm == "DFS":
        result = dfs(current_grid, start, goal)
    elif algorithm == "Dijkstra":
        result = dijkstra(current_grid, start, goal)
    elif algorithm == "Greedy Best-First":
        heuristic = get_heuristic(heuristic_name)
        result = greedy_best_first(current_grid, start, goal, heuristic)
    elif algorithm == "A*":
        heuristic = get_heuristic(heuristic_name)
        result = astar(current_grid, start, goal, heuristic)
    elif algorithm == "Bidirectional BFS":
        result = bidirectional_bfs(current_grid, start, goal)
    else:
        return None, None, f"Unknown algorithm: {algorithm}"

    # Create visualization with result
    fig = create_grid_plot(current_grid, start, goal, result)

    # Create metrics DataFrame with all result data
    metrics_df = pd.DataFrame([{
        'Algorithm': result.algorithm_name,
        'Success': '✓' if result.success else '✗',
        'Path Length': result.path_length if result.success else 'N/A',
        'Path Cost': f"{result.path_cost:.2f}" if result.success else 'N/A',
        'Nodes Visited': result.nodes_visited,
        'Runtime (ms)': f"{result.runtime_ms:.3f}",
    }])

    # Status message
    status_msg = result.message

    return fig, metrics_df, status_msg

def update_heuristic_visibility(algorithm):
    """Update heuristic dropdown visibility based on algorithm."""
    # Only show heuristic dropdown for algorithms that need it
    if algorithm in ["A*", "Greedy Best-First"]:
        return gr.update(visible=True)
    else:
        return gr.update(visible=False)

def create_interface():
    with gr.Blocks(title="Multi-Algorithm Pathfinding") as demo:
        gr.Markdown("# Multi-Algorithm Pathfinding Laboratory")
        gr.Markdown("Compare different pathfinding algorithms with various configurations.")

        with gr.Row():
            # Left column: Controls
            with gr.Column(scale=1):
                gr.Markdown("### Algorithm Selection")
                algorithm_dropdown = gr.Dropdown(
                    choices=["BFS", "DFS", "Dijkstra", "Greedy Best-First", "A*", "Bidirectional BFS"],
                    value="A*",
                    label="Algorithm"
                )

                heuristic_dropdown = gr.Dropdown(
                    choices=["Manhattan", "Euclidean", "Octile", "Chebyshev"],
                    value="Manhattan",
                    label="Heuristic (for A* and Greedy)",
                    visible=True  # Initially visible since A* is default
                )

                gr.Markdown("### Grid Configuration")
                width = gr.Slider(10, 50, value=20, step=1, label="Width")
                height = gr.Slider(10, 50, value=20, step=1, label="Height")
                obstacle_density = gr.Slider(0.0, 0.5, value=0.2, step=0.05, label="Obstacle Density")
                seed = gr.Number(value=42, label="Random Seed", precision=0)

                movement_radio = gr.Radio(
                    choices=["4-directional", "8-directional"],
                    value="4-directional",
                    label="Movement Mode"
                )

                gr.Markdown("### Positions")
                with gr.Row():
                    start_row = gr.Number(value=0, label="Start Row", precision=0)
                    start_col = gr.Number(value=0, label="Start Col", precision=0)
                with gr.Row():
                    goal_row = gr.Number(value=19, label="Goal Row", precision=0)
                    goal_col = gr.Number(value=19, label="Goal Col", precision=0)

                gr.Markdown("### Actions")
                generate_btn = gr.Button("Generate Grid", variant="secondary")
                run_btn = gr.Button("Run Algorithm", variant="primary")

            # Right column: Visualization and metrics
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="Grid Visualization")

                gr.Markdown("### Metrics")
                metrics_output = gr.Dataframe(label="Algorithm Performance")

                status_output = gr.Textbox(label="Status", lines=2)

        # Connect algorithm dropdown change event to update heuristic visibility
        algorithm_dropdown.change(
            fn=update_heuristic_visibility,
            inputs=[algorithm_dropdown],
            outputs=[heuristic_dropdown]
        )

        # Connect button events
        generate_btn.click(
            fn=generate_grid,
            inputs=[width, height, obstacle_density, movement_radio, seed],
            outputs=[plot_output, status_output]
        )

        run_btn.click(
            fn=run_selected_algorithm,
            inputs=[algorithm_dropdown, heuristic_dropdown, start_row, start_col, goal_row, goal_col],
            outputs=[plot_output, metrics_output, status_output]
        )

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
```

### Key Concepts

- **Conditional UI updates**: Using `gr.update(visible=True/False)` to show/hide components
- **Enum handling**: Converting string values to `MovementMode` enum
- **Algorithm selection**: Using a dictionary or if-elif chain to map algorithm names to functions
- **Input validation**: Checking grid existence and position bounds before execution
- **DataFrame display**: Using pandas DataFrame to show structured metrics
- **Event chaining**: Connecting dropdown changes to update other components
- **Comprehensive error messages**: Providing clear feedback for all error conditions

### Testing Advice

1. **Test all algorithms**: Run each of the 6 algorithms and verify they work correctly
2. **Test heuristic visibility**: Switch between algorithms and verify heuristic dropdown appears/disappears
3. **Test movement modes**: Generate grids with 4-directional and 8-directional movement
4. **Test validation**: Try invalid positions (negative, out of bounds) and verify error messages
5. **Test metrics**: Verify that all metrics (path length, cost, nodes visited, runtime) are displayed correctly
6. **Test edge cases**: Try running algorithm before generating grid, try start == goal, try unreachable goals

---

## Exercise 3 Solution: Preset Grids and Export Features (Advanced)

### Explanation

This solution adds advanced features to the Gradio interface:

1. **Preset grids** for common scenarios (empty, maze, corridors)
2. **Export functionality** to save visualizations as PNG files
3. **Algorithm recommendations** based on grid characteristics
4. **Animation frame export** for creating step-by-step visualizations
5. **Color scheme selection** for accessibility and preferences

These features provide a professional, production-ready interface.

### Code

```python
import gradio as gr
import os
import numpy as np
from datetime import datetime
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.visualization.grid_plot import create_grid_plot
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

current_grid = None
current_result = None
current_start = None
current_goal = None
current_fig = None
current_color_scheme = "Classic"

def create_preset_grid(preset_name, width, height):
    """Create a preset grid configuration."""
    global current_grid, current_start, current_goal

    width = int(width)
    height = int(height)
    current_start = (0, 0)
    current_goal = (height - 1, width - 1)

    if preset_name == "Empty":
        # Create grid with 0 obstacle density
        current_grid = Grid(width=width, height=height, obstacle_density=0.0)
        current_grid.generate_obstacles(current_start, current_goal)
        status = f"Empty grid created: {width}x{height} with no obstacles"

    elif preset_name == "Maze":
        # Create grid with 0.35 obstacle density
        current_grid = Grid(width=width, height=height, obstacle_density=0.35, random_seed=42)
        current_grid.generate_obstacles(current_start, current_goal)
        status = f"Maze grid created: {width}x{height} with {len(current_grid.obstacles)} obstacles"

    elif preset_name == "Corridors":
        # Create grid with strategic corridor pattern
        current_grid = Grid(width=width, height=height, obstacle_density=0.0)

        # Create vertical corridors every 5 columns
        for col in range(2, width - 2, 5):
            for row in range(0, height):
                # Leave gaps for horizontal movement
                if row % 4 != 0:
                    pos = (row, col)
                    if pos != current_start and pos != current_goal:
                        current_grid.obstacles.add(pos)

        # Create horizontal corridors every 4 rows
        for row in range(2, height - 2, 4):
            for col in range(0, width):
                # Leave gaps for vertical movement
                if col % 5 != 0:
                    pos = (row, col)
                    if pos != current_start and pos != current_goal:
                        current_grid.obstacles.add(pos)

        status = f"Corridor grid created: {width}x{height} with {len(current_grid.obstacles)} obstacles"

    # Generate visualization
    fig = create_grid_plot(current_grid, current_start, current_goal)

    return fig, status

def export_visualization(fig):
    """Export current visualization as PNG."""
    global current_fig

    if fig is None:
        return "No visualization to export!"

    # Create exports directory if it doesn't exist
    export_dir = "exports"
    os.makedirs(export_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{export_dir}/pathfinding_{timestamp}.png"

    # Save figure as high-resolution PNG (dpi=300)
    fig.savefig(filename, dpi=300, bbox_inches='tight')

    return f"✓ Exported to {filename}"

def recommend_algorithm(obstacle_density, width, height, movement_mode):
    """Recommend best algorithm based on grid characteristics."""
    grid_size = width * height

    recommendations = []

    # Analyze obstacle density
    if obstacle_density < 0.1:
        recommendations.append("Low obstacle density detected:")
        recommendations.append("• A* with Octile heuristic (fast on open grids)")
        recommendations.append("• Bidirectional BFS (efficient for sparse obstacles)")
    elif obstacle_density > 0.3:
        recommendations.append("High obstacle density detected (maze-like):")
        recommendations.append("• BFS (reliable, guarantees shortest path)")
        recommendations.append("• Bidirectional BFS (faster than BFS in mazes)")
    else:
        recommendations.append("Medium obstacle density detected:")
        recommendations.append("• A* with Manhattan (balanced performance)")
        recommendations.append("• Dijkstra (reliable when heuristic is uncertain)")

    # Analyze grid size
    if grid_size > 900:  # 30x30
        recommendations.append("\nLarge grid detected:")
        recommendations.append("• Bidirectional BFS or A* recommended")
        recommendations.append("• Avoid DFS (may be very slow)")

    # Analyze movement mode
    if movement_mode == "8-directional":
        recommendations.append("\n8-directional movement:")
        recommendations.append("• Use Octile or Chebyshev heuristics for A*")
        recommendations.append("• Manhattan heuristic may be less accurate")

    return "\n".join(recommendations)

def export_animation_frames(grid, start, goal, result):
    """Export animation frames showing search progression."""
    if result is None or not result.success:
        return "No successful result to animate!"

    # Create frames directory
    frames_dir = "frames"
    os.makedirs(frames_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate frame for each step in visited nodes
    visited_so_far = set()
    frame_count = 0

    # Create frames at regular intervals (every 10 nodes)
    step_size = max(1, len(result.visited) // 20)  # Generate ~20 frames

    for i in range(0, len(result.visited), step_size):
        visited_so_far.update(result.visited[:i+1])

        # Create a partial result
        partial_result = type(result)(
            success=False,
            path=[],
            path_length=0,
            path_cost=0.0,
            nodes_visited=len(visited_so_far),
            visited=list(visited_so_far),
            algorithm_name=result.algorithm_name,
            runtime_ms=0.0,
            message=f"Frame {frame_count + 1}"
        )

        # Create visualization
        fig = create_grid_plot(grid, start, goal, partial_result)

        # Save frame
        filename = f"{frames_dir}/frame_{timestamp}_{frame_count:03d}.png"
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close(fig)

        frame_count += 1

    # Add final frame with complete path
    final_fig = create_grid_plot(grid, start, goal, result)
    filename = f"{frames_dir}/frame_{timestamp}_{frame_count:03d}.png"
    final_fig.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(final_fig)
    frame_count += 1

    return f"✓ Exported {frame_count} frames to {frames_dir}/"

def apply_color_scheme(scheme_name):
    """Get color scheme dictionary."""
    global current_color_scheme
    current_color_scheme = scheme_name

    schemes = {
        "Classic": {
            'empty': '#FFFFFF',
            'obstacle': '#000000',
            'visited': '#87CEEB',
            'path': '#FFD700',
            'start': '#00FF00',
            'goal': '#FF0000'
        },
        "High Contrast": {
            'empty': '#FFFFFF',
            'obstacle': '#000000',
            'visited': '#0066FF',
            'path': '#FFFF00',
            'start': '#00FF00',
            'goal': '#FF0000'
        },
        "Colorblind Friendly": {
            'empty': '#FFFFFF',
            'obstacle': '#000000',
            'visited': '#0173B2',
            'path': '#DE8F05',
            'start': '#029E73',
            'goal': '#CC78BC'
        }
    }
    return schemes.get(scheme_name, schemes["Classic"])

def run_with_color_scheme(start_row, start_col, goal_row, goal_col):
    """Run A* with current color scheme."""
    global current_grid, current_result, current_start, current_goal, current_fig

    if current_grid is None:
        return None, "Please generate a grid first!"

    current_start = (int(start_row), int(start_col))
    current_goal = (int(goal_row), int(goal_col))

    # Run A*
    current_result = astar(current_grid, current_start, current_goal, manhattan_distance)

    # Get current color scheme
    colors = apply_color_scheme(current_color_scheme)

    # Create custom visualization with color scheme
    # (Note: In production, you'd modify create_grid_plot to accept color scheme)
    current_fig = create_grid_plot(current_grid, current_start, current_goal, current_result)

    status = f"Path found! Length: {current_result.path_length}" if current_result.success else "No path found"
    return current_fig, status

def create_interface():
    with gr.Blocks(title="Advanced Pathfinding Lab") as demo:
        gr.Markdown("# Advanced AI Pathfinding Laboratory")
        gr.Markdown("Full-featured pathfinding interface with presets, export, and recommendations.")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Grid Configuration")
                width = gr.Slider(10, 50, value=20, step=1, label="Width")
                height = gr.Slider(10, 50, value=20, step=1, label="Height")
                obstacle_density = gr.Slider(0.0, 0.5, value=0.2, step=0.05, label="Obstacle Density")
                movement_mode = gr.Radio(
                    choices=["4-directional", "8-directional"],
                    value="4-directional",
                    label="Movement Mode"
                )

                gr.Markdown("### Presets")
                with gr.Row():
                    preset_empty_btn = gr.Button("Empty Grid", size="sm")
                    preset_maze_btn = gr.Button("Maze", size="sm")
                    preset_corridor_btn = gr.Button("Corridors", size="sm")

                gr.Markdown("### Positions")
                with gr.Row():
                    start_row = gr.Number(value=0, label="Start Row", precision=0)
                    start_col = gr.Number(value=0, label="Start Col", precision=0)
                with gr.Row():
                    goal_row = gr.Number(value=19, label="Goal Row", precision=0)
                    goal_col = gr.Number(value=19, label="Goal Col", precision=0)

                gr.Markdown("### Visualization Options")
                color_scheme_dropdown = gr.Dropdown(
                    choices=["Classic", "High Contrast", "Colorblind Friendly"],
                    value="Classic",
                    label="Color Scheme"
                )

                run_btn = gr.Button("Run A*", variant="primary")

                gr.Markdown("### Export")
                export_viz_btn = gr.Button("Export Visualization")
                export_frames_btn = gr.Button("Export Animation Frames")

            with gr.Column(scale=2):
                plot_output = gr.Plot(label="Grid Visualization")
                status_output = gr.Textbox(label="Status", lines=2)

                gr.Markdown("### Algorithm Recommendation")
                recommendation_text = gr.Textbox(label="Recommended Algorithms", lines=6)

        # Connect preset button events
        preset_empty_btn.click(
            fn=lambda w, h: create_preset_grid("Empty", w, h),
            inputs=[width, height],
            outputs=[plot_output, status_output]
        )

        preset_maze_btn.click(
            fn=lambda w, h: create_preset_grid("Maze", w, h),
            inputs=[width, height],
            outputs=[plot_output, status_output]
        )

        preset_corridor_btn.click(
            fn=lambda w, h: create_preset_grid("Corridors", w, h),
            inputs=[width, height],
            outputs=[plot_output, status_output]
        )

        # Connect color scheme change
        color_scheme_dropdown.change(
            fn=lambda scheme: scheme,  # Just store the selection
            inputs=[color_scheme_dropdown],
            outputs=[]
        )

        # Connect run button
        run_btn.click(
            fn=run_with_color_scheme,
            inputs=[start_row, start_col, goal_row, goal_col],
            outputs=[plot_output, status_output]
        )

        # Connect export buttons
        export_viz_btn.click(
            fn=export_visualization,
            inputs=[plot_output],
            outputs=[status_output]
        )

        export_frames_btn.click(
            fn=lambda: export_animation_frames(current_grid, current_start, current_goal, current_result),
            inputs=[],
            outputs=[status_output]
        )

        # Update recommendation when grid parameters change
        width.change(
            fn=recommend_algorithm,
            inputs=[obstacle_density, width, height, movement_mode],
            outputs=[recommendation_text]
        )
        height.change(
            fn=recommend_algorithm,
            inputs=[obstacle_density, width, height, movement_mode],
            outputs=[recommendation_text]
        )
        obstacle_density.change(
            fn=recommend_algorithm,
            inputs=[obstacle_density, width, height, movement_mode],
            outputs=[recommendation_text]
        )
        movement_mode.change(
            fn=recommend_algorithm,
            inputs=[obstacle_density, width, height, movement_mode],
            outputs=[recommendation_text]
        )

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
```

### Key Concepts

- **Preset configurations**: Creating predefined grid patterns for common scenarios
- **File I/O**: Saving matplotlib figures to disk with timestamps
- **Directory management**: Creating directories if they don't exist
- **Rule-based recommendations**: Analyzing grid characteristics to suggest algorithms
- **Animation generation**: Creating frame sequences for visualizations
- **Custom color schemes**: Providing accessibility options
- **Multiple event handlers**: Connecting multiple inputs to update recommendations
- **Lambda functions**: Using inline functions for simple event handlers

### Testing Advice

1. **Test presets**: Click each preset button and verify the grid patterns are correct
2. **Test export**: Export a visualization and check that the PNG file is created with correct timestamp
3. **Test recommendations**: Change grid parameters and verify recommendations update appropriately
4. **Test animation frames**: Export frames and verify numbered sequence is created
5. **Test color schemes**: Try each color scheme (note: implementation may need visualization updates)
6. **Test file system**: Check that `exports/` and `frames/` directories are created properly

---

## Exercise 4 Solution: Debugging Challenge - Broken Gradio Interface

### Bugs Found and Fixes

#### Bug 1: Missing global keyword in generate_grid

**Problem**: The function creates a local `current_grid` variable instead of updating the global one.

**Fix**: Add `global current_grid` at the start of the function.

```python
def generate_grid(width, height, obstacle_density):
    """Generate a new grid."""
    global current_grid  # FIX: Add global keyword
    current_grid = Grid(...)
```

#### Bug 2: Not converting slider values to int

**Problem**: Gradio sliders return float values, but Grid expects integers for width/height.

**Fix**: Convert to int:

```python
current_grid = Grid(
    width=int(width),  # FIX: Convert to int
    height=int(height),  # FIX: Convert to int
    obstacle_density=obstacle_density
)
```

#### Bug 3: Using width/height directly for goal position

**Problem**: Using the float slider value directly instead of converted int.

**Fix**: Use the already-created grid's dimensions or convert to int:

```python
goal = (int(height) - 1, int(width) - 1)  # FIX: Convert to int
```

#### Bug 4: Not checking if grid is None

**Problem**: Accessing `current_grid` without checking if it exists causes crashes.

**Fix**: Add None check:

```python
def run_algorithm(start_row, start_col, goal_row, goal_col):
    """Run A* algorithm."""
    # FIX: Check if grid exists
    if current_grid is None:
        return None, "Please generate a grid first!"

    # ... rest of code
```

#### Bug 5: Not converting number inputs to int

**Problem**: gr.Number returns float, but positions need int.

**Fix**: Convert to int:

```python
start = (int(start_row), int(start_col))  # FIX: Convert to int
goal = (int(goal_row), int(goal_col))  # FIX: Convert to int
```

#### Bug 6: Incorrect arguments to create_grid_plot

**Problem**: Passing `result` instead of separate `start`, `goal`, and `result` parameters.

**Fix**: Pass all required parameters:

```python
fig = create_grid_plot(current_grid, start, goal, result)  # FIX: Add start and goal
```

#### Bug 7: Wrong output order in button event

**Problem**: The outputs list order doesn't match the return value order from generate_grid.

**Fix**: Match the order:

```python
gen_btn.click(
    fn=generate_grid,
    inputs=[width, height, obstacle_density],
    outputs=[plot, status]  # FIX: Correct order (was [status, plot])
)
```

#### Bug 8: Missing global keyword in run_algorithm

**Problem**: Function needs to access global `current_grid`.

**Fix**: Add global keyword:

```python
def run_algorithm(start_row, start_col, goal_row, goal_col):
    """Run A* algorithm."""
    global current_grid  # FIX: Add global keyword
    # ... rest of code
```

### Corrected Code

```python
import gradio as gr
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.visualization.grid_plot import create_grid_plot

current_grid = None

def generate_grid(width, height, obstacle_density):
    """Generate a new grid."""
    global current_grid  # FIX 1: Add global keyword

    current_grid = Grid(
        width=int(width),  # FIX 2: Convert to int
        height=int(height),  # FIX 2: Convert to int
        obstacle_density=obstacle_density
    )
    start = (0, 0)
    goal = (int(height) - 1, int(width) - 1)  # FIX 3: Convert to int
    current_grid.generate_obstacles(start, goal)

    fig = create_grid_plot(current_grid, start, goal)
    return fig, "Grid generated"

def run_algorithm(start_row, start_col, goal_row, goal_col):
    """Run A* algorithm."""
    global current_grid  # FIX 8: Add global keyword

    # FIX 4: Check if grid exists
    if current_grid is None:
        return None, "Please generate a grid first!"

    start = (int(start_row), int(start_col))  # FIX 5: Convert to int
    goal = (int(goal_row), int(goal_col))  # FIX 5: Convert to int

    result = astar(current_grid, start, goal, manhattan_distance)

    # FIX 6: Include start and goal in visualization
    fig = create_grid_plot(current_grid, start, goal, result)

    return fig, "Algorithm complete"

def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Pathfinding Lab")

        with gr.Row():
            with gr.Column():
                width = gr.Slider(10, 50, value=20, label="Width")
                height = gr.Slider(10, 50, value=20, label="Height")
                obstacle_density = gr.Slider(0, 0.5, value=0.2, label="Obstacles")

                start_row = gr.Number(value=0, label="Start Row")
                start_col = gr.Number(value=0, label="Start Col")
                goal_row = gr.Number(value=19, label="Goal Row")
                goal_col = gr.Number(value=19, label="Goal Col")

                gen_btn = gr.Button("Generate")
                run_btn = gr.Button("Run")

            with gr.Column():
                plot = gr.Plot()
                status = gr.Textbox(label="Status")

        # FIX 7: Correct output order
        gen_btn.click(
            fn=generate_grid,
            inputs=[width, height, obstacle_density],
            outputs=[plot, status]  # Was [status, plot]
        )

        run_btn.click(
            fn=run_algorithm,
            inputs=[start_row, start_col, goal_row, goal_col],
            outputs=[plot, status]
        )

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
```

### What You Should Understand

**Key Learning Outcomes**:

1. **Global State Management**: Always use `global` keyword when modifying global variables inside functions. Without it, Python creates a new local variable.

2. **Type Conversion**: Gradio components have specific return types:
   - `gr.Slider()` returns float
   - `gr.Number()` returns float
   - Always convert to int when needed for dimensions or indices

3. **None Checking**: Always validate that required state exists before using it. This prevents crashes and provides better user experience.

4. **Function Signatures**: Match return values to output components. If a button event specifies 3 outputs, the function must return 3 values.

5. **Output Order**: The order of items in the `outputs` list must match the order of return values from the function.

6. **Debugging Process**:
   - Read error messages carefully
   - Check function signatures and return types
   - Verify input/output connections
   - Test each component individually
   - Use print statements or debuggers to inspect values

**Common Gradio Patterns to Remember**:
- Global state for persistence between calls
- Type conversion for slider/number inputs
- None checking before using global state
- Matching return values to output components
- Proper event handler connections

---

## Summary

These Week 8 solutions demonstrate:
- Building functional Gradio interfaces with proper state management
- Supporting multiple algorithms with conditional UI elements
- Adding advanced features (presets, export, recommendations)
- Debugging common Gradio interface issues

Key takeaways:
1. Use global state carefully with proper `global` keywords
2. Always convert Gradio component outputs to expected types
3. Validate inputs and state before using them
4. Match function returns to output component lists
5. Use event handlers to create interactive workflows

---

**Continue to Week 9: Benchmarking →**
