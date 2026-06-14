# Week 8: Building Interactive UIs with Gradio

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 7](week_07_visualization.md)** | **📝 [Week 8 Exercises](../exercises/week_08.md)** | **✅ [Week 8 Solutions](../solutions/week_08_solutions.md)** | **➡️ [Next: Week 9](week_09_benchmarking.md)**

---

## Learning Goals

By the end of this week, you will understand:
- What Gradio is and why it's ideal for ML/AI demos
- How to create interactive web interfaces without frontend code
- Building controls for pathfinding configuration
- Displaying visualizations and metrics in Gradio
- Handling state and user interactions
- Deploying Gradio apps

## Theory

### What is Gradio?

**Gradio** is a Python library for quickly building web interfaces for machine learning models and data science applications. It's perfect for this project because:

1. **Python-first**: Write UI code entirely in Python, no HTML/CSS/JavaScript required
2. **Fast prototyping**: Build interactive interfaces in minutes
3. **Shareable**: Easily deploy and share with others
4. **ML-focused**: Designed for showcasing models and visualizations
5. **Free hosting**: Gradio provides free hosting on Hugging Face Spaces

### Gradio vs Alternatives

**Gradio vs Streamlit**:
- Gradio: Better for ML model demos, simpler API, built-in sharing
- Streamlit: Better for data dashboards, more layout control, app-like feel

**Gradio vs Flask/FastAPI**:
- Gradio: No frontend code needed, automatic UI generation
- Flask/FastAPI: Full control, requires HTML/CSS/JS knowledge

**For our pathfinding lab**: Gradio is ideal because we want to focus on algorithms, not web development.

### Key Gradio Concepts

**1. Interface vs Blocks**

```python
# Interface: Simple, automatic layout
gr.Interface(fn=my_function, inputs=[...], outputs=[...])

# Blocks: Custom layout, more control
with gr.Blocks() as demo:
    with gr.Row():
        input1 = gr.Textbox()
        input2 = gr.Slider()
    output = gr.Plot()
    btn.click(fn=my_function, inputs=[input1, input2], outputs=output)
```

**Interface**: Best for simple input → function → output flows
**Blocks**: Best for complex layouts with multiple interactions (our choice)

**2. Input Components**

- `gr.Slider()`: Numeric ranges (grid size, obstacle density)
- `gr.Dropdown()`: Select from options (algorithm, heuristic)
- `gr.Number()`: Numeric input (start/goal coordinates)
- `gr.Checkbox()`: Boolean flags
- `gr.Textbox()`: Text input (seed values)

**3. Output Components**

- `gr.Plot()`: Matplotlib/Plotly figures
- `gr.Dataframe()`: Pandas DataFrames (metrics tables)
- `gr.Textbox()`: Status messages
- `gr.Image()`: PNG/JPG images

**4. Event Handling**

```python
button.click(
    fn=my_function,           # Function to call
    inputs=[input1, input2],  # Input components
    outputs=[output1]         # Output components
)
```

Events: `click`, `change`, `submit`, `upload`

## Code Walkthrough

### Application Structure

File: `src/pathfinding_lab/ui/gradio_app.py`

**Step 1: Import Dependencies**

```python
import gradio as gr
from pathfinding_lab.algorithms import bfs, dfs, dijkstra, astar
from pathfinding_lab.heuristics import manhattan_distance, octile_distance
from pathfinding_lab.visualization import create_grid_plot
```

**Step 2: Global State Management**

```python
current_grid = None

def generate_grid(width, height, obstacle_density, seed, ...):
    global current_grid
    current_grid = Grid(width, height, obstacle_density=obstacle_density)
    # ... generate obstacles and visualize
```

**Why global state?** Gradio functions are stateless, but we need to persist the grid between "generate" and "run algorithm" calls.

**Alternative approaches**:
- Use `gr.State()` component for per-session state
- Store grid in a database or cache
- Re-generate grid each time (slower)

**Step 3: Algorithm Selection and Execution**

```python
def run_algorithm(algorithm, heuristic_name, start_row, start_col, goal_row, goal_col):
    if current_grid is None:
        return None, None, "Please generate a grid first!"

    start = (int(start_row), int(start_col))
    goal = (int(goal_row), int(goal_col))

    if algorithm == "BFS":
        result = bfs(current_grid, start, goal)
    elif algorithm == "A*":
        heuristic = get_heuristic(heuristic_name)
        result = astar(current_grid, start, goal, heuristic)
    # ...

    fig = create_grid_plot(current_grid, start, goal, result)
    metrics = create_metrics_dataframe(result)
    return fig, metrics, "Success!"
```

**Key design decisions**:
- String-based algorithm selection (Gradio dropdowns return strings)
- Separate heuristic parameter (only used by A* and Greedy)
- Multiple return values for multiple outputs

**Step 4: Building the Gradio Interface**

```python
with gr.Blocks(title="Pathfinding Lab") as demo:
    gr.Markdown("# AI Pathfinding Laboratory")

    with gr.Row():
        # Left column: controls
        with gr.Column():
            width = gr.Slider(10, 50, value=20, label="Grid Width")
            height = gr.Slider(10, 50, value=20, label="Grid Height")
            obstacle_density = gr.Slider(0, 0.5, value=0.2, label="Obstacle Density")
            # ... more controls

        # Right column: visualization
        with gr.Column():
            grid_plot = gr.Plot(label="Grid Visualization")
            status = gr.Textbox(label="Status")

    # Button events
    generate_btn.click(
        fn=generate_grid,
        inputs=[width, height, obstacle_density, ...],
        outputs=[grid_plot, status]
    )
```

**Layout structure**:
- `gr.Row()`: Horizontal layout
- `gr.Column()`: Vertical layout
- Nested rows/columns create complex layouts

### Comparison Mode

```python
def compare_algorithms(start, goal):
    algorithms = ["BFS", "DFS", "Dijkstra", "A* (Manhattan)", "A* (Octile)"]
    results = []

    for algo in algorithms:
        result = run_algorithm_by_name(algo, start, goal)
        results.append(result)

    comparison_fig = create_comparison_plot(results)
    comparison_table = create_comparison_table(results)

    return comparison_fig, comparison_table
```

**Comparison mode** runs multiple algorithms on the same grid and displays side-by-side metrics.

## Common Mistakes

### 1. Forgetting to Handle None/Empty State

**Problem**: Accessing `current_grid` before it's generated causes crashes.

```python
# Bad: No check for None
def run_algorithm(...):
    result = astar(current_grid, start, goal, heuristic)  # Crashes if None!
```

**Solution**: Always check state before using it:

```python
# Good: Check before use
def run_algorithm(...):
    if current_grid is None:
        return None, None, "Please generate a grid first!"
    result = astar(current_grid, start, goal, heuristic)
```

### 2. Not Converting Slider Values to Int

**Problem**: Gradio sliders return floats, but grid dimensions need integers.

```python
# Bad: Using float for grid size
grid = Grid(width, height)  # width=20.5 causes issues!
```

**Solution**: Explicitly convert to int:

```python
# Good: Convert to int
grid = Grid(int(width), int(height))
```

### 3. Matplotlib Figure Management

**Problem**: Not closing figures leads to memory leaks.

```python
# Bad: Creating figures without cleanup
def generate_viz():
    fig = plt.figure()
    # ... create plot
    return fig  # Figure stays in memory!
```

**Solution**: Use `plt.close()` after returning or use context managers:

```python
# Good: Close after use
def generate_viz():
    fig = create_grid_plot(...)
    # Gradio displays it, then we can close
    return fig
```

### 4. Blocking the UI with Long Computations

**Problem**: Long-running algorithms freeze the UI.

```python
# Bad: Synchronous execution blocks UI
def run_algorithm(...):
    result = expensive_algorithm()  # UI frozen during this!
    return result
```

**Solution**: For production apps, use async/queuing:

```python
# Better: Use Gradio's queue feature
demo.queue()
demo.launch()
```

### 5. Inconsistent Component Return Types

**Problem**: Returning wrong types for output components.

```python
# Bad: Returning string for Plot component
return "Error message"  # Plot expects Figure object!
```

**Solution**: Match return types to component types:

```python
# Good: Return None for Plot, string for Textbox
return None, "Error message"  # (Plot, Textbox)
```

## Mini Project Task

### This Week's Challenge: Custom Gradio Interface

Build a simplified version of the pathfinding lab with your own custom UI design and additional features.

### Requirements

1. **Custom layout**: Create your own row/column arrangement
2. **Preset grids**: Add buttons for common scenarios:
   - Empty grid (no obstacles)
   - Maze (high obstacle density)
   - Corridors (strategic obstacle placement)
3. **Animation toggle**: Add checkbox to enable/disable path animation
4. **Export functionality**: Add button to download results as image
5. **Algorithm recommendations**: Display which algorithm is best for current grid

### Steps

1. **Create new Gradio Blocks interface**

```python
with gr.Blocks() as custom_demo:
    gr.Markdown("## My Custom Pathfinding Lab")

    with gr.Row():
        # Your layout here
        pass
```

2. **Add preset buttons**

```python
preset_empty = gr.Button("Empty Grid")
preset_maze = gr.Button("Maze")
preset_corridor = gr.Button("Corridor")

preset_empty.click(fn=lambda: generate_preset("empty"), outputs=[...])
```

3. **Implement export feature**

```python
def export_results(fig):
    fig.savefig("pathfinding_result.png", dpi=300, bbox_inches='tight')
    return "Exported to pathfinding_result.png"

export_btn.click(fn=export_results, inputs=[grid_plot], outputs=[status])
```

4. **Add algorithm recommendation**

```python
def recommend_algorithm(obstacle_density, grid_size):
    if obstacle_density < 0.1:
        return "Recommendation: A* with Octile (fast on open grids)"
    elif obstacle_density > 0.3:
        return "Recommendation: BFS (reliable in mazes)"
    else:
        return "Recommendation: A* with Manhattan (balanced)"
```

### Success Criteria

- ✅ Custom layout different from main app
- ✅ Three preset grid buttons functional
- ✅ Export feature saves visualization
- ✅ Algorithm recommendation updates based on parameters
- ✅ All controls properly connected to functions

## Reflection Questions

1. **Why use Gradio instead of a traditional web framework?**
   - What are the tradeoffs of simplicity vs control?
   - When would you choose Flask/React instead?

2. **How does state management work in Gradio?**
   - What are the limitations of global state?
   - When would you use `gr.State()` instead?

3. **What makes a good UI for algorithm visualization?**
   - What controls are essential vs nice-to-have?
   - How do you balance simplicity and functionality?

4. **How would you deploy this Gradio app?**
   - What platforms support Gradio?
   - What environment variables might you need?

5. **What improvements would make the UI more user-friendly?**
   - Error messages and validation?
   - Progress indicators for long operations?
   - Tooltips and help text?

## Additional Resources

- **Gradio Documentation**: https://gradio.app/docs/
- **Gradio Guides**: https://gradio.app/guides/
- **Gradio Quickstart**: https://gradio.app/quickstart/
- **Hugging Face Spaces**: https://huggingface.co/spaces (free Gradio hosting)
- **Gradio Blocks Guide**: https://gradio.app/blocks-and-event-listeners/

## Next Week Preview

Next week, we'll focus on **benchmarking and performance analysis**:
- Systematic algorithm comparison
- Statistical analysis of results
- Performance metrics beyond runtime
- Generating comprehensive reports
- Identifying algorithm strengths/weaknesses

You'll learn how to rigorously evaluate algorithm performance across different scenarios!

---

**Continue to Week 9: Benchmarking →**

---

## End-to-End Pipeline Connection

Week 8 connects the learning project into an interactive product:

```text
controls → validation → grid creation → algorithm dispatch → visualization → metrics display
```

This is where separate modules become an application a learner can use.

### Gradio Application Architecture

A clear Gradio callback should do five jobs in order:

1. read raw control values
2. validate and convert them into project types
3. call the core/algorithm functions
4. convert results into plots and tables
5. return user-friendly outputs

Keep algorithm logic out of the UI layer. The UI should orchestrate the pipeline, not contain the pathfinding implementation.

### State Management Mindset

The app often needs to generate a grid once and run several algorithms on it. That means grid state matters. If the grid changes between runs without the learner realizing it, comparisons become unfair.

For reliable comparisons:

- reuse the same generated grid
- preserve start and goal positions
- keep random seed visible
- clearly regenerate only when the user asks

### Error Handling for Learners

Good UI errors should explain the next action:

- Start or goal outside grid: ask the learner to choose valid coordinates.
- Start or goal on an obstacle: regenerate or move the point.
- No path found: show the explored region and explain that obstacles block all routes.
- Very large grid is slow: suggest reducing size or obstacle density.

### Comparison Mode Pipeline

Comparison mode should run multiple algorithms on the same grid, collect each `SearchResult`, and display a table with path length, path cost, nodes visited, runtime, and success.

This directly prepares learners for Week 9 benchmarking.

### Week 8 Build Checkpoint

You are ready for Week 9 when you can use the UI to generate one grid, run at least two algorithms on it, compare their plots and metrics, and explain the difference.
