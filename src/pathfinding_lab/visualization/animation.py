"""Animation placeholder — step-by-step animation is not yet implemented."""

import warnings

# TODO: Implement step-by-step animation of algorithm execution
# This would show the algorithm exploring nodes in real-time
# Could use Matplotlib animation or Plotly frames


def create_animation(grid, result):
    """
    Create an animated visualization of the pathfinding process.

    Args:
        grid: The grid
        result: SearchResult with visited_order

    Returns:
        Animation object (to be implemented)

    Raises:
        NotImplementedError: Always, until this feature is implemented.
    """
    warnings.warn(
        "create_animation() is not yet implemented. "
        "See the Future Improvements section in README.md for status.",
        stacklevel=2,
    )
    raise NotImplementedError(
        "Step-by-step animation has not been implemented yet. "
        "Contributions are welcome — see README.md for the feature wishlist."
    )
