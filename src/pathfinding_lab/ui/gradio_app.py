"""Main Gradio application interface."""

import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd

from src.pathfinding_lab.algorithms.astar import astar
from src.pathfinding_lab.algorithms.bfs import bfs
from src.pathfinding_lab.algorithms.bidirectional_bfs import bidirectional_bfs
from src.pathfinding_lab.algorithms.dfs import dfs
from src.pathfinding_lab.algorithms.dijkstra import dijkstra
from src.pathfinding_lab.algorithms.greedy_best_first import greedy_best_first
from src.pathfinding_lab.core.grid import Grid
from src.pathfinding_lab.core.result import SearchResult
from src.pathfinding_lab.core.types import MovementMode
from src.pathfinding_lab.heuristics.chebyshev import chebyshev_distance
from src.pathfinding_lab.heuristics.euclidean import euclidean_distance
from src.pathfinding_lab.heuristics.manhattan import manhattan_distance
from src.pathfinding_lab.heuristics.octile import octile_distance
from src.pathfinding_lab.heuristics.weighted import weighted_manhattan_distance
from src.pathfinding_lab.visualization.comparison_plot import (
    create_comparison_plot,
    create_comparison_table,
)
from src.pathfinding_lab.visualization.grid_plot import create_grid_plot

# Global state to maintain grid between calls
current_grid = None


def get_heuristic(heuristic_name: str):
    """Get heuristic function by name."""
    heuristic_map = {
        "Manhattan": manhattan_distance,
        "Euclidean": euclidean_distance,
        "Chebyshev": chebyshev_distance,
        "Octile": octile_distance,
        "Weighted Manhattan": lambda p1, p2: weighted_manhattan_distance(p1, p2, 1.2),
    }
    return heuristic_map.get(heuristic_name, manhattan_distance)


def generate_grid(width, height, obstacle_density, seed, movement_mode, start_row, start_col, goal_row, goal_col):
    """Generate a new grid with obstacles."""
    global current_grid

    movement = MovementMode.FOUR_DIRECTIONAL if movement_mode == "4-directional" else MovementMode.EIGHT_DIRECTIONAL

    current_grid = Grid(
        width=int(width),
        height=int(height),
        obstacle_density=obstacle_density,
        movement_mode=movement,
        random_seed=int(seed) if seed else None
    )

    start = (int(start_row), int(start_col))
    goal = (int(goal_row), int(goal_col))

    current_grid.generate_obstacles(start, goal)

    # Create visualization
    fig = create_grid_plot(current_grid, start, goal)

    return fig, f"Grid generated: {width}x{height} with {len(current_grid.obstacles)} obstacles"


def run_algorithm(algorithm, heuristic_name, start_row, start_col, goal_row, goal_col):
    """Run selected algorithm on current grid."""
    global current_grid

    if current_grid is None:
        return None, None, "Please generate a grid first!"

    start = (int(start_row), int(start_col))
    goal = (int(goal_row), int(goal_col))

    # Get algorithm function
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

    # Create visualization
    fig = create_grid_plot(current_grid, start, goal, result)

    # Create metrics dataframe
    metrics_df = pd.DataFrame([{
        'Algorithm': result.algorithm_name,
        'Success': '✓' if result.success else '✗',
        'Path Length': result.path_length if result.success else 'N/A',
        'Path Cost': f"{result.path_cost:.2f}" if result.success else 'N/A',
        'Nodes Visited': result.nodes_visited,
        'Runtime (ms)': f"{result.runtime_ms:.3f}",
    }])

    return fig, metrics_df, result.message


def compare_algorithms(heuristic_name, start_row, start_col, goal_row, goal_col):
    """Compare all algorithms on current grid."""
    global current_grid

    if current_grid is None:
        return None, None, "Please generate a grid first!"

    start = (int(start_row), int(start_col))
    goal = (int(goal_row), int(goal_col))
    heuristic = get_heuristic(heuristic_name)

    # Run all algorithms
    results = []

    results.append(bfs(current_grid, start, goal))
    results.append(dfs(current_grid, start, goal))
    results.append(dijkstra(current_grid, start, goal))
    results.append(greedy_best_first(current_grid, start, goal, heuristic))
    results.append(astar(current_grid, start, goal, heuristic))
    results.append(bidirectional_bfs(current_grid, start, goal))

    # Create comparison table
    comparison_df = create_comparison_table(results)

    # Create comparison plot
    comparison_fig = create_comparison_plot(results)

    return comparison_fig, comparison_df, "Comparison complete!"


def create_gradio_interface():
    """Create the Gradio interface."""
    with gr.Blocks(title="AI Pathfinding Laboratory") as demo:
        gr.Markdown("# 🎯 AI Pathfinding Laboratory")
        gr.Markdown(
            "Educational pathfinding algorithms laboratory with visualization and benchmarking."
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Configuration")

                # Algorithm selection
                algorithm_dropdown = gr.Dropdown(
                    choices=["BFS", "DFS", "Dijkstra", "Greedy Best-First", "A*", "Bidirectional BFS"],
                    value="A*",
                    label="Algorithm"
                )

                heuristic_dropdown = gr.Dropdown(
                    choices=["Manhattan", "Euclidean", "Chebyshev", "Octile", "Weighted Manhattan"],
                    value="Manhattan",
                    label="Heuristic (for A* and Greedy)"
                )

                # Grid parameters
                with gr.Group():
                    gr.Markdown("#### Grid Settings")
                    width_slider = gr.Slider(10, 50, value=20, step=1, label="Width")
                    height_slider = gr.Slider(10, 50, value=20, step=1, label="Height")
                    obstacle_slider = gr.Slider(0.0, 0.5, value=0.2, step=0.05, label="Obstacle Density")
                    seed_number = gr.Number(value=42, label="Random Seed", precision=0)
                    movement_radio = gr.Radio(
                        choices=["4-directional", "8-directional"],
                        value="4-directional",
                        label="Movement Mode"
                    )

                # Position controls
                with gr.Group():
                    gr.Markdown("#### Positions")
                    with gr.Row():
                        start_row = gr.Number(value=0, label="Start Row", precision=0)
                        start_col = gr.Number(value=0, label="Start Col", precision=0)
                    with gr.Row():
                        goal_row = gr.Number(value=19, label="Goal Row", precision=0)
                        goal_col = gr.Number(value=19, label="Goal Col", precision=0)

                # Action buttons
                gr.Markdown("#### Actions")
                generate_btn = gr.Button("Generate Grid", variant="secondary")
                run_btn = gr.Button("Run Algorithm", variant="primary")
                compare_btn = gr.Button("Compare All Algorithms", variant="secondary")

            with gr.Column(scale=2):
                gr.Markdown("### Visualization")
                plot_output = gr.Plot(label="Grid Visualization")

                gr.Markdown("### Metrics")
                metrics_output = gr.Dataframe(label="Algorithm Metrics")

                status_output = gr.Textbox(label="Status", lines=2)

        # Connect event handlers
        generate_btn.click(
            fn=generate_grid,
            inputs=[
                width_slider,
                height_slider,
                obstacle_slider,
                seed_number,
                movement_radio,
                start_row,
                start_col,
                goal_row,
                goal_col,
            ],
            outputs=[plot_output, status_output],
        )

        run_btn.click(
            fn=run_algorithm,
            inputs=[
                algorithm_dropdown,
                heuristic_dropdown,
                start_row,
                start_col,
                goal_row,
                goal_col,
            ],
            outputs=[plot_output, metrics_output, status_output],
        )

        compare_btn.click(
            fn=compare_algorithms,
            inputs=[heuristic_dropdown, start_row, start_col, goal_row, goal_col],
            outputs=[plot_output, metrics_output, status_output],
        )

        # Instructions
        with gr.Accordion("Instructions", open=False):
            gr.Markdown("""
            ### How to Use

            1. **Configure Grid**: Set grid size, obstacle density, and random seed
            2. **Set Positions**: Define start and goal coordinates
            3. **Generate Grid**: Click to create a random grid with obstacles
            4. **Select Algorithm**: Choose from BFS, DFS, Dijkstra, Greedy, A*, or Bidirectional BFS
            5. **Choose Heuristic**: Select heuristic for A* and Greedy Best-First
            6. **Run Algorithm**: Execute the selected algorithm
            7. **Compare All**: Run and compare all algorithms

            ### Color Legend
            - 🟢 Green: Start position
            - 🔴 Red: Goal position
            - ⬛ Black: Obstacles
            - 🔵 Light Blue: Visited nodes
            - 🟡 Yellow: Final path
            """)

    return demo
