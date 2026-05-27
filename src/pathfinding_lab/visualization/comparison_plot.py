"""Comparison visualization for multiple algorithms."""

from typing import List

import matplotlib.pyplot as plt
import pandas as pd

from pathfinding_lab.core.result import SearchResult


def create_comparison_table(results: List[SearchResult]) -> pd.DataFrame:
    """
    Create a comparison table for multiple algorithm results.

    Args:
        results: List of SearchResult objects

    Returns:
        Pandas DataFrame with comparison metrics
    """
    data = []
    for result in results:
        data.append({
            'Algorithm': result.algorithm_name,
            'Success': '✓' if result.success else '✗',
            'Path Length': result.path_length if result.success else 'N/A',
            'Path Cost': f"{result.path_cost:.2f}" if result.success else 'N/A',
            'Nodes Visited': result.nodes_visited,
            'Runtime (ms)': f"{result.runtime_ms:.2f}",
        })

    return pd.DataFrame(data)


def create_comparison_plot(results: List[SearchResult], figsize: tuple = (12, 6)) -> plt.Figure:
    """
    Create bar charts comparing algorithm performance.

    Args:
        results: List of SearchResult objects
        figsize: Figure size

    Returns:
        Matplotlib Figure with comparison charts
    """
    fig, axes = plt.subplots(1, 3, figsize=figsize)

    algorithms = [r.algorithm_name for r in results]
    nodes_visited = [r.nodes_visited for r in results]
    runtime_ms = [r.runtime_ms for r in results]
    path_costs = [r.path_cost if r.success else 0 for r in results]

    # Nodes visited comparison
    axes[0].bar(range(len(algorithms)), nodes_visited, color='skyblue')
    axes[0].set_title('Nodes Visited')
    axes[0].set_xticks(range(len(algorithms)))
    axes[0].set_xticklabels([a.split()[0] for a in algorithms], rotation=45, ha='right')
    axes[0].set_ylabel('Count')

    # Runtime comparison
    axes[1].bar(range(len(algorithms)), runtime_ms, color='lightcoral')
    axes[1].set_title('Runtime')
    axes[1].set_xticks(range(len(algorithms)))
    axes[1].set_xticklabels([a.split()[0] for a in algorithms], rotation=45, ha='right')
    axes[1].set_ylabel('Milliseconds')

    # Path cost comparison
    axes[2].bar(range(len(algorithms)), path_costs, color='lightgreen')
    axes[2].set_title('Path Cost')
    axes[2].set_xticks(range(len(algorithms)))
    axes[2].set_xticklabels([a.split()[0] for a in algorithms], rotation=45, ha='right')
    axes[2].set_ylabel('Cost')

    plt.tight_layout()
    return fig
