# Week 1: Python Project Setup

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **📝 [Week 1 Exercises](../exercises/week_01.md)** | **✅ [Week 1 Solutions](../solutions/week_01_solutions.md)** | **➡️ [Next: Week 2](week_02_grid_model.md)**

---

## Learning Goals

By the end of this week, you will:
- Set up a proper Python project structure
- Understand virtual environments and package management
- Learn basic pytest usage
- Understand the repository layout
- Run your first tests

## Theory: Python Project Structure

### Why Project Structure Matters

A well-organized project makes code:
- **Maintainable**: Easy to find and modify code
- **Testable**: Clear separation of concerns
- **Scalable**: Easy to add new features
- **Professional**: Follows community standards

### Standard Python Project Layout

```
project/
├── src/                    # Source code
│   └── package_name/       # Main package
├── tests/                  # Test files
├── docs/                   # Documentation
├── pyproject.toml          # Project metadata
├── requirements.txt        # Dependencies
└── README.md               # Project overview
```

### Virtual Environments

Virtual environments isolate project dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Code Walkthrough

### 1. Understanding pyproject.toml

```toml
[project]
name = "pathfinding-lab"
version = "0.1.0"
dependencies = [
    "gradio>=4.0.0",
    "numpy>=1.24.0",
    # ... more dependencies
]
```

This file defines:
- Project metadata
- Required dependencies
- Development tools configuration

### 2. Understanding requirements.txt

Lists all Python packages needed:
```
gradio>=4.0.0
numpy>=1.24.0
matplotlib>=3.7.0
```

### 3. Basic Test Structure

```python
# tests/test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_string_concat():
    assert "hello" + " world" == "hello world"
```

Run with: `pytest`

## Common Mistakes

### 1. Not Using Virtual Environments
**Problem**: Global package conflicts
**Solution**: Always use `python -m venv venv`

### 2. Forgetting to Activate venv
**Problem**: Installing to wrong Python
**Solution**: Check with `which python` (should show venv path)

### 3. Wrong Import Paths
**Problem**: `ModuleNotFoundError`
**Solution**: Understand relative vs absolute imports

### 4. Not Installing in Editable Mode
**Problem**: Changes not reflected
**Solution**: `pip install -e .`

## Mini Project Task

### Task: Set Up Your Development Environment

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd ai-pathfinding-gradio-lab
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**
   ```bash
   pytest
   ```

5. **Verify installation**
   ```bash
   python -c "import gradio; print(gradio.__version__)"
   ```

### Success Criteria
- ✅ Virtual environment activated
- ✅ All dependencies installed
- ✅ Tests pass
- ✅ Can import pathfinding_lab modules

## Reflection Questions

1. Why do we separate source code (`src/`) from tests (`tests/`)?
2. What are the benefits of using a virtual environment?
3. What happens if you install packages without activating venv?
4. How does pytest discover test files?
5. What is the purpose of `__init__.py` files?

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Virtual Environments Explained](https://realpython.com/python-virtual-environments-a-primer/)

## Next Week Preview

Next week, we'll dive into the grid model - the foundation of our pathfinding system. You'll learn about:
- 2D grid representation
- Node and cell concepts
- Obstacle handling
- Neighbor generation

---

## 📚 Additional Learning Resources

### Week 1 Materials:
- **📝 [Week 1 Exercises](../exercises/week_01.md)** - Practice problems
- **✅ [Week 1 Solutions](../solutions/week_01_solutions.md)** - Detailed solutions
- **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)** - Full 12-week guide

### External Resources:
- [Python Packaging User Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Virtual Environments Explained](https://realpython.com/python-virtual-environments-a-primer/)

---

**➡️ [Continue to Week 2: Grid Model](week_02_grid_model.md)** | **📖 [Back to Roadmap](../LEARNING_ROADMAP.md)**

---

## End-to-End Pipeline Connection

This week is not just about installing packages. It is the week where you make the whole learning pipeline possible.

By the end of setup, you should be able to move through this first product loop:

```text
Open terminal → activate environment → install package → run tests → import code → launch app.py
```

That loop proves that later weeks can focus on pathfinding instead of fighting the environment.

### What Week 1 Enables

- `src/pathfinding_lab/` can be imported from tests, notebooks, and the app.
- `pytest` can verify that grid and algorithm behavior stays correct as the project grows.
- `app.py` can find the Gradio UI code and launch the product.
- Development dependencies such as Ruff and pytest are available for Week 11 quality work.

### First Full-System Smoke Test

After installing the project, check three layers:

1. **Package layer**: import `pathfinding_lab` without an error.
2. **Test layer**: run the test suite and confirm pytest discovers tests.
3. **Application layer**: start `python app.py` and verify the Gradio server launches.

If all three work, you have a healthy foundation for every later week.

### How to Think About the Repository

The repository is arranged like a product, not like a single script:

- `core/` defines shared data structures.
- `algorithms/` searches the grid.
- `heuristics/` helps informed algorithms make better choices.
- `visualization/` explains results visually.
- `metrics/` compares behavior objectively.
- `ui/` connects everything to Gradio.
- `tests/` protects the behavior while you improve the code.

When you get lost, ask: "Which layer am I working in, and which layer consumes its output?"

### Common Setup Problems That Break Later Weeks

- If imports fail, later algorithm files cannot be tested.
- If dependencies install globally instead of in the virtual environment, the app may work on one machine but fail on another.
- If tests are not run from the repository root, pytest may not find the package correctly.
- If editable install is skipped, local source changes may not appear during experimentation.

### Week 1 Build Checkpoint

You are ready for Week 2 when you can explain the difference between source code, tests, docs, and the app entry point, and when you can run the project from a clean terminal without guessing commands.
