# Week 1: Python Project Setup

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

**Continue to Week 2: Grid Model →**
