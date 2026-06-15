# 🎯 AI Pathfinding Laboratory

An educational repository for learning pathfinding algorithms, heuristic search, visualization, and benchmarking using Python and Gradio. Perfect for beginner/intermediate AI/ML enthusiasts on a 12-week learning journey.

## 🌟 Features

- **6 Pathfinding Algorithms**: BFS, DFS, Dijkstra, Greedy Best-First, A*, Bidirectional BFS
- **5 Heuristic Functions**: Manhattan, Euclidean, Chebyshev, Octile, Weighted
- **Interactive Gradio Interface**: Real-time visualization and algorithm comparison
- **Comprehensive Learning Path**: 12-week structured curriculum with exercises
- **Benchmarking Tools**: Compare algorithm performance metrics
- **ML Heuristics** (Optional): Learn to train learned heuristics with scikit-learn
- **Full Test Suite**: pytest-based testing for all components

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Raj-Indra-Asura/ai-pathfinding-gradio-lab.git
cd ai-pathfinding-gradio-lab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install this project as an editable package (REQUIRED)
pip install -e .
```

> **Why `pip install -e .` is required:** this project uses a `src/` layout, so the
> `pathfinding_lab` package lives under `src/` rather than in the repository root.
> The editable install (`-e`) tells Python where to find it, so `import pathfinding_lab`
> works everywhere (tests, notebooks, and `app.py`) while still picking up your local
> edits immediately. **If you skip this step you will get `ModuleNotFoundError: No module
> named 'pathfinding_lab'`.**

### Smoke Test (confirm a healthy setup)

Run these three checks in order before starting Week 1. They verify the package,
the test suite, and the app all work:

```bash
# 1. Package layer: the package imports
python -c "import pathfinding_lab; print(pathfinding_lab.__version__)"

# 2. Test layer: the tests pass
pytest

# 3. Application layer: the app launches
python app.py
```

**Expected success output:**
- Step 1 prints a version number such as `0.1.0`.
- Step 2 ends with a green line like `==== NN passed in N.NNs ====`.
- Step 3 prints `Running on local URL:  http://127.0.0.1:7860` (press `Ctrl+C` to stop).

### Running the Application

```bash
python app.py
```

The Gradio interface will launch at `http://localhost:7860`

### Running Tests

```bash
pytest
```

## 📚 Repository Structure

```
ai-pathfinding-gradio-lab/
├── README.md                          # This file
├── app.py                             # Main application entry point
├── pyproject.toml                     # Project configuration
├── requirements.txt                   # Python dependencies
├── src/pathfinding_lab/              # Main package
│   ├── core/                         # Core data structures
│   │   ├── grid.py                   # Grid representation
│   │   ├── node.py                   # Node class
│   │   ├── result.py                 # Search result dataclass
│   │   └── types.py                  # Type definitions
│   ├── algorithms/                   # Pathfinding algorithms
│   │   ├── bfs.py                    # Breadth-First Search
│   │   ├── dfs.py                    # Depth-First Search
│   │   ├── dijkstra.py               # Dijkstra's Algorithm
│   │   ├── greedy_best_first.py      # Greedy Best-First Search
│   │   ├── astar.py                  # A* Search
│   │   └── bidirectional_bfs.py      # Bidirectional BFS
│   ├── heuristics/                   # Heuristic functions
│   │   ├── manhattan.py              # Manhattan distance
│   │   ├── euclidean.py              # Euclidean distance
│   │   ├── chebyshev.py              # Chebyshev distance
│   │   ├── octile.py                 # Octile distance
│   │   └── weighted.py               # Weighted heuristics
│   ├── visualization/                # Visualization tools
│   │   ├── grid_plot.py              # Grid plotting
│   │   ├── animation.py              # Animation (TODO)
│   │   └── comparison_plot.py        # Algorithm comparison plots
│   ├── mazes/                        # Maze generation
│   │   ├── generators.py             # Obstacle generators
│   │   └── presets.py                # Preset configurations
│   ├── metrics/                      # Performance metrics
│   │   ├── evaluator.py              # Result evaluation
│   │   └── benchmark.py              # Benchmarking tools
│   ├── ml/                           # ML learned heuristics
│   │   ├── dataset.py                # Training data generation
│   │   ├── features.py               # Feature extraction
│   │   ├── train_heuristic.py        # Model training
│   │   └── learned_heuristic.py      # Learned heuristic function
│   └── ui/                           # Gradio interface
│       ├── gradio_app.py             # Main Gradio app
│       ├── controls.py               # UI controls
│       └── examples.py               # Example configurations
├── tests/                            # Test suite
│   ├── test_grid.py
│   ├── test_bfs.py
│   ├── test_dijkstra.py
│   ├── test_astar.py
│   ├── test_heuristics.py
│   └── test_metrics.py
├── docs/                             # Weekly learning guides
│   ├── week_01_python_project_setup.md
│   ├── week_02_grid_model.md
│   ├── week_03_bfs_dfs.md
│   ├── week_04_dijkstra.md
│   ├── week_05_astar.md
│   ├── week_06_heuristics.md
│   ├── week_07_visualization.md
│   ├── week_08_gradio_ui.md
│   ├── week_09_benchmarking.md
│   ├── week_10_ml_heuristic.md
│   ├── week_11_polishing.md
│   └── week_12_final_project.md
├── exercises/                        # Weekly exercises
│   └── week_XX.md (12 files)
├── solutions/                        # Exercise solutions
│   └── week_XX_solutions.md (12 files)
└── notebooks/                        # Jupyter notebooks
    ├── 01_grid_basics.ipynb
    ├── 02_bfs_dfs.ipynb
    ├── 03_dijkstra_astar.ipynb
    ├── 04_heuristics.ipynb
    ├── 05_algorithm_comparison.ipynb
    ├── 06_learned_heuristics.ipynb
    ├── 07_visualization.ipynb
    ├── 08_gradio_ui.ipynb
    └── 11_polishing_testing.ipynb
```


### End-to-End Learning Pipeline

For a start-to-finish explanation of how the app works, read **[docs/END_TO_END_PIPELINE.md](docs/END_TO_END_PIPELINE.md)**. It connects the weekly lessons into one product flow: setup → grid creation → algorithms → heuristics → visualization → Gradio UI → benchmarking → optional ML heuristic → final polish.

## 🗺️ 12-Week Learning Roadmap

**📖 [Complete Learning Roadmap](LEARNING_ROADMAP.md)** - Your comprehensive guide with direct links to all resources!

### Month 1: Foundations
- **Week 1**: Python project setup, virtual environments, pytest basics
- **Week 2**: Grid model, nodes, obstacles, coordinate systems
- **Week 3**: BFS and DFS algorithms
- **Week 4**: Dijkstra's algorithm and weighted pathfinding

### Month 2: Advanced Algorithms
- **Week 5**: A* Search algorithm
- **Week 6**: Heuristic functions and quality metrics
- **Week 7**: Visualization of paths and visited nodes
- **Week 8**: Building the Gradio interface

### Month 3: Analysis & ML
- **Week 9**: Benchmarking and algorithm comparison
- **Week 10**: Optional learned heuristics with scikit-learn
- **Week 11**: Documentation, testing, and code quality
- **Week 12**: Final integration, deployment, and reflection

**👉 Start here: [Week 1 Documentation](docs/week_01_python_project_setup.md)**

## 🎓 Learning Outcomes

By completing this 12-week program, you will:

✅ Understand fundamental pathfinding algorithms (BFS, DFS, Dijkstra, A*)
✅ Grasp heuristic search concepts and admissibility
✅ Implement and visualize algorithms from scratch
✅ Benchmark and compare algorithm performance
✅ Build interactive web applications with Gradio
✅ Apply machine learning to pathfinding (optional)
✅ Write clean, tested, documented Python code
✅ Gain hands-on experience with AI/ML concepts

## 🔬 Algorithms Included

### Uninformed Search
- **BFS (Breadth-First Search)**: Explores level by level, finds shortest path
- **DFS (Depth-First Search)**: Explores depth-first, does not guarantee shortest path
- **Bidirectional BFS**: Searches from both start and goal simultaneously

### Informed Search
- **Dijkstra's Algorithm**: Finds optimal path with weighted edges
- **Greedy Best-First**: Uses heuristic, fast but not optimal
- **A* Search**: Combines Dijkstra + heuristic, finds optimal path

### Heuristics
- **Manhattan**: Sum of absolute differences (4-directional)
- **Euclidean**: Straight-line distance (8-directional)
- **Chebyshev**: Maximum of absolute differences
- **Octile**: Accounts for diagonal cost difference
- **Weighted**: Adjustable heuristic weight for speed/quality tradeoff

## 🎨 Using the Gradio Interface

1. **Configure Grid**: Set size, obstacle density, random seed
2. **Set Positions**: Define start and goal coordinates
3. **Generate Grid**: Create random maze with obstacles
4. **Select Algorithm**: Choose from 6 pathfinding algorithms
5. **Choose Heuristic**: Pick heuristic for A* and Greedy
6. **Run Algorithm**: Visualize the pathfinding process
7. **Compare All**: Benchmark all algorithms side-by-side

### Visualization Legend
- 🟢 **Green**: Start position
- 🔴 **Red**: Goal position
- ⬛ **Black**: Obstacles
- 🔵 **Light Blue**: Visited nodes
- 🟡 **Yellow**: Final path

## 🤖 Why Gradio?

### Gradio vs Streamlit

We chose **Gradio** for this educational project because:

✅ **Simpler API**: Easier for beginners to learn
✅ **Faster Prototyping**: Quick iterations during learning
✅ **Better for ML Models**: Native support for model inference
✅ **Shareable**: Easy to create public demos
✅ **Interactive Components**: Rich input/output widgets

**Streamlit** is also excellent and more suitable for:
- Dashboard-style applications
- More complex multi-page apps
- Custom layouts and styling

Both are great tools! We prioritize learning simplicity here.

## 🔮 Future Improvements

- [ ] Add step-by-step animation of algorithm execution
- [ ] Implement Jump Point Search (JPS)
- [ ] Add more maze generation algorithms (Prim's, Kruskal's)
- [ ] Support custom obstacle drawing
- [ ] Add path smoothing algorithms
- [ ] Implement multi-agent pathfinding
- [ ] Add 3D visualization option
- [ ] Create video tutorials for each week
- [ ] Add interactive algorithm visualizer
- [ ] Support different cost functions
- [ ] Implement IDA* and other variants

## 📖 Documentation

Each week includes:
- **Learning Guide**: Theory, concepts, and walkthroughs
- **Exercises**: Beginner, intermediate, and advanced challenges
- **Solutions**: Detailed explanations and code
- **Jupyter Notebook**: Interactive exploration

**🚀 Ready to start?**
1. Read the [Complete Learning Roadmap](LEARNING_ROADMAP.md)
2. Begin with [Week 1: Python Project Setup](docs/week_01_python_project_setup.md)

## 🧪 Testing

Run the full test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/pathfinding_lab

# Run specific test file
pytest tests/test_astar.py

# Run with verbose output
pytest -v
```

## 🤝 Contributing

This is an educational project! Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Inspired by classic pathfinding visualization tools and educational resources:
- Red Blob Games pathfinding articles
- Sebastian Lague's A* tutorial
- The AI research community

## 📧 Contact

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check the discussions tab
- Review the weekly guides in `docs/`

---

**Happy Learning! 🚀**

Start your pathfinding journey today with Week 1: Python Project Setup
