"""Benchmark utilities for comparing algorithms."""

import time
from typing import Callable, Dict, List

from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.result import SearchResult
from pathfinding_lab.core.types import Position


def benchmark_algorithm(
    algorithm_func: Callable,
    grid: Grid,
    start: Position,
    goal: Position,
    num_runs: int = 1
) -> Dict[str, float]:
    """
    Benchmark an algorithm over multiple runs.

    Args:
        algorithm_func: Algorithm function to benchmark
        grid: Grid to search on
        start: Start position
        goal: Goal position
        num_runs: Number of runs to average

    Returns:
        Dictionary with benchmark statistics
    """
    runtimes = []
    nodes_visited_list = []

    for _ in range(num_runs):
        result = algorithm_func(grid, start, goal)
        runtimes.append(result.runtime_ms)
        nodes_visited_list.append(result.nodes_visited)

    return {
        'avg_runtime_ms': sum(runtimes) / len(runtimes),
        'min_runtime_ms': min(runtimes),
        'max_runtime_ms': max(runtimes),
        'avg_nodes_visited': sum(nodes_visited_list) / len(nodes_visited_list),
    }


def run_comparison(
    algorithms: List[tuple],
    grid: Grid,
    start: Position,
    goal: Position
) -> List[SearchResult]:
    """
    Run multiple algorithms and collect results.

    Args:
        algorithms: List of (name, function, kwargs) tuples
        grid: Grid to search on
        start: Start position
        goal: Goal position

    Returns:
        List of SearchResult objects
    """
    results = []

    for name, func, kwargs in algorithms:
        try:
            result = func(grid, start, goal, **kwargs)
            results.append(result)
        except Exception as e:
            # Create error result
            results.append(SearchResult(
                algorithm_name=name,
                success=False,
                message=f"Error: {str(e)}"
            ))

    return results
