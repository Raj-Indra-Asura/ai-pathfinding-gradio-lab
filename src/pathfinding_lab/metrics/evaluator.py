"""Metrics evaluation for pathfinding algorithms."""

from typing import Dict

from src.pathfinding_lab.core.result import SearchResult


def evaluate_result(result: SearchResult) -> Dict[str, any]:
    """
    Evaluate a pathfinding result and extract key metrics.

    Args:
        result: SearchResult to evaluate

    Returns:
        Dictionary of metrics
    """
    return {
        'algorithm': result.algorithm_name,
        'success': result.success,
        'path_length': result.path_length,
        'path_cost': result.path_cost,
        'nodes_visited': result.nodes_visited,
        'runtime_ms': result.runtime_ms,
        'efficiency': result.path_length / result.nodes_visited if result.nodes_visited > 0 else 0,
    }


def calculate_heuristic_quality(actual_cost: float, estimated_cost: float) -> Dict[str, float]:
    """
    Calculate quality metrics for a heuristic function.

    Args:
        actual_cost: Actual optimal path cost
        estimated_cost: Heuristic estimate

    Returns:
        Dictionary with quality metrics
    """
    error = abs(actual_cost - estimated_cost)
    relative_error = error / actual_cost if actual_cost > 0 else 0

    return {
        'absolute_error': error,
        'relative_error': relative_error,
        'is_admissible': estimated_cost <= actual_cost,
    }
