"""Control components for Gradio UI."""

import gradio as gr


def create_algorithm_controls():
    """Create algorithm selection controls."""
    algorithm_dropdown = gr.Dropdown(
        choices=[
            "BFS",
            "DFS",
            "Dijkstra",
            "Greedy Best-First",
            "A*",
            "Bidirectional BFS"
        ],
        value="A*",
        label="Algorithm"
    )

    heuristic_dropdown = gr.Dropdown(
        choices=[
            "Manhattan",
            "Euclidean",
            "Chebyshev",
            "Octile",
            "Weighted Manhattan"
        ],
        value="Manhattan",
        label="Heuristic (for A* and Greedy)"
    )

    return algorithm_dropdown, heuristic_dropdown


def create_grid_controls():
    """Create grid configuration controls."""
    width_slider = gr.Slider(
        minimum=10,
        maximum=50,
        value=20,
        step=1,
        label="Grid Width"
    )

    height_slider = gr.Slider(
        minimum=10,
        maximum=50,
        value=20,
        step=1,
        label="Grid Height"
    )

    obstacle_slider = gr.Slider(
        minimum=0.0,
        maximum=0.5,
        value=0.2,
        step=0.05,
        label="Obstacle Density"
    )

    seed_number = gr.Number(
        value=42,
        label="Random Seed",
        precision=0
    )

    movement_radio = gr.Radio(
        choices=["4-directional", "8-directional"],
        value="4-directional",
        label="Movement Mode"
    )

    return width_slider, height_slider, obstacle_slider, seed_number, movement_radio


def create_position_controls():
    """Create start and goal position controls."""
    start_row = gr.Number(value=0, label="Start Row", precision=0)
    start_col = gr.Number(value=0, label="Start Col", precision=0)
    goal_row = gr.Number(value=19, label="Goal Row", precision=0)
    goal_col = gr.Number(value=19, label="Goal Col", precision=0)

    return start_row, start_col, goal_row, goal_col


def create_action_buttons():
    """Create action buttons."""
    generate_btn = gr.Button("Generate Grid", variant="secondary")
    run_btn = gr.Button("Run Algorithm", variant="primary")
    compare_btn = gr.Button("Compare All Algorithms", variant="secondary")

    return generate_btn, run_btn, compare_btn
