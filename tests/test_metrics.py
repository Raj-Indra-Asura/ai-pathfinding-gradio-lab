"""Tests for metrics and evaluation."""

import pytest

from pathfinding_lab.algorithms.bfs import bfs
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.metrics.evaluator import evaluate_result, calculate_heuristic_quality


def test_evaluate_result():
    """Test result evaluation."""
    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    start = (0, 0)
    goal = (2, 2)

    result = bfs(grid, start, goal)
    metrics = evaluate_result(result)

    assert 'algorithm' in metrics
    assert 'success' in metrics
    assert 'path_length' in metrics
    assert 'nodes_visited' in metrics
    assert 'efficiency' in metrics


def test_heuristic_quality():
    """Test heuristic quality calculation."""
    quality = calculate_heuristic_quality(actual_cost=10.0, estimated_cost=8.0)

    assert 'absolute_error' in quality
    assert 'relative_error' in quality
    assert 'is_admissible' in quality

    assert quality['is_admissible'] is True  # 8 <= 10


def test_heuristic_inadmissible():
    """Test inadmissible heuristic detection."""
    quality = calculate_heuristic_quality(actual_cost=10.0, estimated_cost=12.0)

    assert quality['is_admissible'] is False  # 12 > 10
