# Week 8: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 7 Exercises](week_07.md)** | **📚 [Week 8 Documentation](../docs/week_08_gradio_ui.md)** | **✅ [Week 8 Solutions](../solutions/week_08_solutions.md)** | **➡️ [Next: Week 9 Exercises](week_09.md)**

---

**🔑 Concepts/links you'll need:** Gradio Blocks/Interface — [quickstart](https://www.gradio.app/guides/quickstart); passing functions as callbacks ([Week 0 §7](../docs/week_00_python_prerequisites.md#prereq-typehints)); `try/except` for input validation ([Week 0 §9](../docs/week_00_python_prerequisites.md#prereq-tryexcept)).

## Warm-up Exercise (Trivial)

### Task: Launch a Two-Line Gradio App

Before wiring up pathfinding, make *any* Gradio app appear in your browser so the toolkit isn't a
cold open.

```python
import gradio as gr

def greet(name):
    return f"Hello, {name}! Gradio is working."

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

**You're done when** the app opens at `http://127.0.0.1:7860`, you type a name, and see the
greeting. Press `Ctrl+C` to stop. *(New to passing a function as `fn`? See [Week 0 §7](../docs/week_00_python_prerequisites.md#prereq-typehints).)*

---

## Exercise 1: Basic Gradio Interface (Beginner)

**Goal**: Create a simple Gradio interface for a single pathfinding algorithm.

**Task**: Build a basic Gradio app that allows users to:
1. Configure grid dimensions (width and height sliders)
2. Set obstacle density (slider from 0.0 to 0.5)
3. Generate a grid with obstacles
4. Run BFS algorithm on the grid
5. Display the visualization and basic metrics

**Requirements**:
- Use `gr.Blocks()` for the interface
- Include grid dimension sliders (10-50 range)
- Include obstacle density slider
- Add "Generate Grid" and "Run BFS" buttons
- Display grid visualization using `gr.Plot()`
- Show success status in a textbox

**Starter Code**:

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
    # TODO: Create Grid instance
    # TODO: Generate obstacles (use default start/goal positions)
    # TODO: Create visualization
    # TODO: Return figure and status message
    pass

def run_bfs_algorithm(start_row, start_col, goal_row, goal_col):
    """Run BFS on the current grid."""
    global current_grid
    # TODO: Check if grid exists
    # TODO: Create start and goal tuples
    # TODO: Run BFS
    # TODO: Create visualization with result
    # TODO: Return figure and status message
    pass

def create_interface():
    """Create the Gradio interface."""
    with gr.Blocks(title="BFS Pathfinding") as demo:
        # TODO: Add title markdown

        # TODO: Create layout with Row and Column
        # TODO: Add sliders for width, height, obstacle_density
        # TODO: Add number inputs for start and goal positions
        # TODO: Add "Generate Grid" and "Run BFS" buttons
        # TODO: Add plot output and status textbox

        # TODO: Connect button events to functions

        pass

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
```

**Expected Output**:
- A functional Gradio interface that generates grids and runs BFS
- Proper visualization showing obstacles, visited nodes, and path
- Status messages indicating success or errors

**Testing**:
1. Generate a 20x20 grid with 0.2 obstacle density
2. Run BFS from (0,0) to (19,19)
3. Verify that the path is found and visualized correctly

---

## Exercise 2: Multi-Algorithm Selector with State Management (Intermediate)

**Goal**: Extend the basic interface to support multiple algorithms with proper state management.

**Task**: Create a Gradio app that:
1. Supports all 6 algorithms (BFS, DFS, Dijkstra, Greedy, A*, Bidirectional BFS)
2. Provides heuristic selection for A* and Greedy algorithms
3. Displays detailed metrics in a DataFrame
4. Handles edge cases (no grid generated, invalid positions)
5. Provides helpful error messages

**Requirements**:
- Algorithm dropdown with all 6 algorithms
- Heuristic dropdown (Manhattan, Euclidean, Octile, Chebyshev)
- Disable heuristic dropdown when not using A* or Greedy
- Display metrics table with: Algorithm, Success, Path Length, Path Cost, Nodes Visited, Runtime
- Add movement mode selection (4-directional vs 8-directional)
- Validate that start/goal positions are within grid bounds
- Show clear error messages for invalid states

**Starter Code**:

```python
import gradio as gr
import pandas as pd
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.algorithms import bfs, dfs, dijkstra, astar, greedy_best_first, bidirectional_bfs
from pathfinding_lab.heuristics import manhattan_distance, euclidean_distance, octile_distance, chebyshev_distance

current_grid = None

def get_heuristic(heuristic_name):
    """Map heuristic name to function."""
    # TODO: Create dictionary mapping names to heuristic functions
    pass

def generate_grid(width, height, obstacle_density, movement_mode, seed):
    """Generate grid with movement mode."""
    global current_grid
    # TODO: Convert movement_mode string to MovementMode enum
    # TODO: Create grid with movement mode and random seed
    # TODO: Generate obstacles
    # TODO: Return visualization and status
    pass

def run_selected_algorithm(algorithm, heuristic_name, start_row, start_col, goal_row, goal_col):
    """Run the selected algorithm on the current grid."""
    global current_grid

    # TODO: Validate that grid exists
    # TODO: Validate start and goal positions are within bounds
    # TODO: Create start and goal tuples

    # TODO: Use if-elif to select algorithm
    # TODO: For A* and Greedy, get heuristic function
    # TODO: Run algorithm and get result

    # TODO: Create visualization with result
    # TODO: Create metrics DataFrame with all result data
    # TODO: Return figure, metrics, and status message
    pass

def update_heuristic_visibility(algorithm):
    """Update heuristic dropdown visibility based on algorithm."""
    # TODO: Return gr.update(visible=True) if algorithm needs heuristic
    # TODO: Otherwise return gr.update(visible=False)
    pass

def create_interface():
    with gr.Blocks() as demo:
        # TODO: Create complete interface with:
        # - Algorithm dropdown
        # - Heuristic dropdown (conditionally visible)
        # - Grid configuration controls
        # - Movement mode radio buttons
        # - Position inputs
        # - Generate and Run buttons
        # - Plot output
        # - Metrics DataFrame output
        # - Status textbox

        # TODO: Connect algorithm dropdown change event to update_heuristic_visibility
        # TODO: Connect button events

        pass

    return demo
```

**Expected Output**:
- Interface with all 6 algorithms selectable
- Heuristic dropdown appears/disappears based on algorithm selection
- Comprehensive metrics table for each algorithm run
- Proper error handling with clear messages

**Testing**:
1. Generate a grid and run each of the 6 algorithms
2. Switch between algorithms requiring/not requiring heuristics
3. Try running an algorithm before generating a grid (should show error)
4. Try invalid start/goal positions (should show error)
5. Compare different heuristics with A*

---

## Exercise 3: Preset Grids and Export Features (Advanced)

**Goal**: Add advanced UI features including preset grids, export functionality, and algorithm recommendations.

**Task**: Enhance the Gradio app with:
1. Three preset grid buttons (Empty, Maze, Corridors)
2. Export visualization as PNG with timestamp
3. Algorithm recommendation based on grid characteristics
4. Animation frame export feature
5. Custom color scheme selector

**Requirements**:
- **Preset Grids**:
  - Empty: 0% obstacle density
  - Maze: 35% obstacle density with specific patterns
  - Corridors: Strategic obstacle placement for corridor-like structure
- **Export Feature**:
  - Save current visualization as high-resolution PNG
  - Include timestamp in filename
  - Return success message with file path
- **Algorithm Recommendation**:
  - Analyze grid characteristics (obstacle density, size, movement mode)
  - Recommend best algorithm with explanation
  - Update recommendation when grid changes
- **Animation Frames**:
  - Export individual frames showing search progression
  - Save as numbered sequence
- **Color Schemes**:
  - Provide 3 preset color schemes (Classic, High Contrast, Colorblind-Friendly)
  - Apply selected scheme to visualization

**Starter Code**:

```python
import gradio as gr
import os
from datetime import datetime
from pathfinding_lab.core.grid import Grid

current_grid = None
current_result = None
current_start = None
current_goal = None

def create_preset_grid(preset_name, width, height):
    """Create a preset grid configuration."""
    global current_grid

    if preset_name == "Empty":
        # TODO: Create grid with 0 obstacle density
        pass
    elif preset_name == "Maze":
        # TODO: Create grid with 0.35 obstacle density
        pass
    elif preset_name == "Corridors":
        # TODO: Create grid with strategic corridor pattern
        # Hint: Create vertical and horizontal corridors
        pass

    # TODO: Generate visualization
    # TODO: Return figure and status
    pass

def export_visualization(fig):
    """Export current visualization as PNG."""
    if fig is None:
        return "No visualization to export!"

    # TODO: Create exports directory if it doesn't exist
    # TODO: Generate filename with timestamp
    # TODO: Save figure as high-resolution PNG (dpi=300)
    # TODO: Return success message with file path
    pass

def recommend_algorithm(obstacle_density, width, height, movement_mode):
    """Recommend best algorithm based on grid characteristics."""
    # TODO: Analyze grid characteristics
    # TODO: Create recommendation logic:
    #   - Low density (<0.1): A* with Octile (fast on open grids)
    #   - High density (>0.3): BFS (reliable in mazes)
    #   - Medium density: A* with Manhattan (balanced)
    #   - Large grids (>30x30): Bidirectional BFS or A*
    #   - 8-directional movement: Use Octile/Chebyshev heuristics
    # TODO: Return recommendation string with explanation
    pass

def export_animation_frames(grid, start, goal, result):
    """Export animation frames showing search progression."""
    if result is None or not result.success:
        return "No successful result to animate!"

    # TODO: Create frames directory
    # TODO: Generate frame for each step in visited nodes
    # TODO: Save each frame as numbered PNG
    # TODO: Return success message with frame count
    pass

def apply_color_scheme(scheme_name):
    """Get color scheme dictionary."""
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

def create_interface():
    with gr.Blocks(title="Advanced Pathfinding Lab") as demo:
        gr.Markdown("# Advanced AI Pathfinding Laboratory")

        with gr.Row():
            with gr.Column(scale=1):
                # TODO: Add all standard controls

                gr.Markdown("### Presets")
                with gr.Row():
                    preset_empty_btn = gr.Button("Empty Grid")
                    preset_maze_btn = gr.Button("Maze")
                    preset_corridor_btn = gr.Button("Corridors")

                gr.Markdown("### Visualization Options")
                color_scheme_dropdown = gr.Dropdown(
                    choices=["Classic", "High Contrast", "Colorblind Friendly"],
                    value="Classic",
                    label="Color Scheme"
                )

                gr.Markdown("### Export")
                export_viz_btn = gr.Button("Export Visualization")
                export_frames_btn = gr.Button("Export Animation Frames")

                gr.Markdown("### Recommendation")
                recommendation_text = gr.Textbox(label="Algorithm Recommendation", lines=3)

            with gr.Column(scale=2):
                # TODO: Add visualization and metrics outputs
                pass

        # TODO: Connect all button events
        # TODO: Update recommendation when grid parameters change
        # TODO: Apply color scheme when changed

        pass

    return demo
```

**Expected Output**:
- Three preset grid buttons that generate different grid types
- Export functionality that saves visualizations to files
- Dynamic algorithm recommendations based on grid characteristics
- Animation frame export for creating visualizations
- Color scheme selector that changes visualization colors

**Testing**:
1. Generate each preset grid and verify patterns
2. Export a visualization and verify PNG file creation
3. Change grid parameters and verify recommendation updates
4. Export animation frames and verify numbered sequence
5. Try each color scheme and verify colors change correctly

---

## Exercise 4: Debugging Challenge - Broken Gradio Interface

**Goal**: Fix multiple bugs in a broken Gradio interface.

**Background**: A junior developer created a Gradio interface for the pathfinding lab, but it has several bugs that prevent it from working correctly. Your task is to identify and fix all bugs.

**Given Code** (with bugs):

```python
import gradio as gr
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.visualization.grid_plot import create_grid_plot

# Bug 1: Missing global keyword in function
current_grid = None

def generate_grid(width, height, obstacle_density):
    """Generate a new grid."""
    # Bug 2: Not using global keyword
    current_grid = Grid(
        width=width,  # Bug 3: Not converting to int
        height=height,
        obstacle_density=obstacle_density
    )
    start = (0, 0)
    goal = (width-1, height-1)  # Bug 4: Using width instead of converting to int
    current_grid.generate_obstacles(start, goal)

    fig = create_grid_plot(current_grid, start, goal)
    return fig, "Grid generated"

def run_algorithm(start_row, start_col, goal_row, goal_col):
    """Run A* algorithm."""
    # Bug 5: Not checking if current_grid is None
    start = (start_row, start_col)  # Bug 6: Not converting to int
    goal = (goal_row, goal_col)

    result = astar(current_grid, start, goal, manhattan_distance)

    # Bug 7: Not including start and goal in visualization
    fig = create_grid_plot(current_grid, result)

    # Bug 8: Returning wrong number of outputs
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

        # Bug 9: Incorrect output order
        gen_btn.click(
            fn=generate_grid,
            inputs=[width, height, obstacle_density],
            outputs=[status, plot]  # Bug 9: Wrong order
        )

        # Bug 10: Missing metrics_output (should have 3 outputs)
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

**Your Task**:
1. Identify all bugs in the code above
2. Fix each bug and explain why it was causing problems
3. Test the fixed interface to ensure it works correctly

**List of Bugs to Find**:
- [ ] Bug 1: Missing global keyword
- [ ] Bug 2: Not using global in generate_grid
- [ ] Bug 3: Not converting slider value to int
- [ ] Bug 4: Using wrong variable for goal position
- [ ] Bug 5: Not checking if grid is None
- [ ] Bug 6: Not converting number inputs to int
- [ ] Bug 7: Incorrect arguments to create_grid_plot
- [ ] Bug 8: Wrong number of return values
- [ ] Bug 9: Wrong output order in button event
- [ ] Bug 10: Missing output component

**Expected Output**:
- A corrected version of the code with all bugs fixed
- Comments explaining each bug and the fix
- A working Gradio interface that generates grids and runs A* successfully

**Testing**:
1. Generate a 20x20 grid with 0.2 obstacle density
2. Run A* from (0,0) to (19,19)
3. Verify visualization shows obstacles, visited nodes, and path correctly
4. Try running algorithm before generating grid (should show error message)

**Hint**: Pay attention to:
- Global state management
- Type conversions (float to int)
- Function signatures and return values
- Event handler input/output connections
- Proper argument passing to visualization functions

---

## Bonus Challenge: Comparison Mode with Real-Time Updates

**Goal**: Create a comparison mode that runs multiple algorithms and displays live progress.

**Task**: Build an advanced interface feature that:
1. Runs all 6 algorithms simultaneously on the same grid
2. Shows live progress as each algorithm completes
3. Displays side-by-side visualizations
4. Creates comprehensive comparison charts
5. Exports comparison report as PDF

**Requirements**:
- Use `gr.Progress()` to show completion status
- Update comparison table as each algorithm finishes
- Create 3 comparison charts (nodes visited, runtime, path cost)
- Generate PDF report with all visualizations and metrics
- Handle timeouts for algorithms that take too long

This challenge combines multiple advanced Gradio features and requires careful state management!

---

## Submission Checklist

For each exercise, ensure:
- [ ] Code runs without errors
- [ ] All requirements are implemented
- [ ] Proper error handling is included
- [ ] UI is user-friendly with clear labels
- [ ] Status messages provide helpful feedback
- [ ] Code includes comments explaining key sections
- [ ] Testing steps have been completed
- [ ] Edge cases are handled appropriately

---

---

**✅ [See Solutions](../solutions/week_08_solutions.md)** | **📚 [Back to Week 8 Docs](../docs/week_08_gradio_ui.md)** | **➡️ [Next: Week 9 Exercises](week_09.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
