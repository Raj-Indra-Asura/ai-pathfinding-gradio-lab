"""Example configurations for quick testing."""

def get_example_configurations():
    """
    Get example configurations for the Gradio interface.

    Returns:
        List of example configurations
    """
    examples = [
        # [algorithm, heuristic, width, height, density, seed, movement, start_row, start_col, goal_row, goal_col]
        ["A*", "Manhattan", 20, 20, 0.2, 42, "4-directional", 0, 0, 19, 19],
        ["BFS", "Manhattan", 15, 15, 0.15, 123, "4-directional", 0, 0, 14, 14],
        ["Dijkstra", "Manhattan", 25, 25, 0.25, 999, "8-directional", 0, 0, 24, 24],
        ["Greedy Best-First", "Euclidean", 20, 20, 0.1, 555, "4-directional", 2, 2, 17, 17],
    ]

    return examples
