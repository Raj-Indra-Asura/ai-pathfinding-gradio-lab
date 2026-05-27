# AI Pathfinding Lab - Jupyter Notebooks

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **📚 [Main README](../README.md)**

---

This directory contains interactive Jupyter notebooks for learning pathfinding algorithms.

## 📚 Notebooks Overview

### [01_grid_basics.ipynb](01_grid_basics.ipynb)
**Related to**: [Week 2 - Grid Model](../docs/week_02_grid_model.md)
- **Topics**: Grid creation, obstacles, neighbors, coordinate systems
- **Level**: Beginner
- **Duration**: 30 minutes
- **Prerequisites**: None

### [02_bfs_dfs.ipynb](02_bfs_dfs.ipynb)
**Related to**: [Week 3 - BFS and DFS](../docs/week_03_bfs_dfs.md)
- **Topics**: Breadth-First Search and Depth-First Search
- **Level**: Beginner
- **Duration**: 45-60 minutes
- **Prerequisites**: 01_grid_basics
- **Key Concepts**:
  - BFS guarantees shortest path (unweighted)
  - DFS explores deeply but doesn't guarantee optimal paths
  - Queue vs Stack data structures
  - Performance comparison on various grids

### [03_dijkstra_astar.ipynb](03_dijkstra_astar.ipynb)
**Related to**: [Week 4 - Dijkstra](../docs/week_04_dijkstra.md) & [Week 5 - A*](../docs/week_05_astar.md)
- **Topics**: Dijkstra's Algorithm and A* Search
- **Level**: Intermediate
- **Duration**: 60-75 minutes
- **Prerequisites**: 02_bfs_dfs
- **Key Concepts**:
  - Weighted graphs and movement costs
  - Optimal pathfinding with Dijkstra
  - Heuristic-guided search with A*
  - Admissible heuristics
  - Performance benchmarking

### [04_heuristics.ipynb](04_heuristics.ipynb)
**Related to**: [Week 6 - Heuristics](../docs/week_06_heuristics.md)
- **Topics**: Comprehensive heuristic function analysis
- **Level**: Intermediate
- **Duration**: 60-90 minutes
- **Prerequisites**: 03_dijkstra_astar
- **Key Concepts**:
  - All 5 heuristic functions (Manhattan, Euclidean, Octile, Chebyshev, Weighted)
  - Mathematical formulas and visualizations
  - Admissibility and consistency testing
  - Heuristic selection guide
  - Performance trade-offs

### [05_algorithm_comparison.ipynb](05_algorithm_comparison.ipynb)
**Related to**: [Week 9 - Benchmarking](../docs/week_09_benchmarking.md)
- **Topics**: Benchmarking all algorithms
- **Level**: Advanced
- **Duration**: 75-90 minutes
- **Prerequisites**: All previous notebooks
- **Key Concepts**:
  - Side-by-side comparison of 6 algorithms
  - Performance metrics and statistical analysis
  - Scalability testing
  - Scenario-based recommendations
  - Decision guide for algorithm selection

### [06_learned_heuristics.ipynb](06_learned_heuristics.ipynb)
**Related to**: [Week 10 - ML Heuristics](../docs/week_10_ml_heuristic.md)
- **Topics**: Machine learning-based heuristics
- **Level**: Advanced
- **Duration**: 90-120 minutes
- **Prerequisites**: All previous notebooks, basic ML knowledge
- **Key Concepts**:
  - Training data generation
  - Random Forest model training
  - Feature engineering
  - Learned vs classical heuristics
  - Admissibility challenges with ML
  - Performance trade-offs (accuracy vs speed)

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

3. **Work through notebooks in order** (01 → 02 → 03 → 04 → 05 → 06)

## Learning Path

### Week 1-2: Foundations
- 01_grid_basics
- 02_bfs_dfs

### Week 3-4: Optimal Algorithms
- 03_dijkstra_astar
- 04_heuristics

### Week 5-6: Advanced Topics
- 05_algorithm_comparison
- 06_learned_heuristics

## Key Features

Each notebook includes:
- ✓ Clear explanations with markdown cells
- ✓ Working code examples
- ✓ Interactive visualizations
- ✓ Performance comparisons
- ✓ Hands-on exercises
- ✓ Real-world applications

## Tips for Success

1. **Run all cells in order** - later cells depend on earlier ones
2. **Experiment** - modify parameters and see what happens
3. **Complete exercises** - hands-on practice reinforces learning
4. **Compare results** - notice patterns in algorithm behavior
5. **Read error messages** - they provide valuable feedback

## Common Issues

### Import Errors
If you get import errors, ensure you're running from the notebooks directory and the parent directory is accessible:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent))
```

### Visualization Issues
If plots don't display:
```python
%matplotlib inline
```

### Performance
For faster execution on large grids, reduce:
- Grid size
- Number of samples
- Number of test iterations

## Additional Resources

- **Main Application**: `../app.py` - Interactive Gradio interface
- **Source Code**: `../src/pathfinding_lab/` - Algorithm implementations
- **Tests**: `../tests/` - Unit tests for all algorithms
- **Documentation**: Repository README.md

## Feedback

Found an issue or have suggestions? Please open an issue on the repository!

## License

Part of the AI Pathfinding Gradio Lab project.

---

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **📚 [Main README](../README.md)** | **🚀 [Week 1: Get Started](../docs/week_01_python_project_setup.md)**
