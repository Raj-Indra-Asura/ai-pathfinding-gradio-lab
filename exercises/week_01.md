# Week 1: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **📚 [Week 1 Documentation](../docs/week_01_python_project_setup.md)** | **✅ [Week 1 Solutions](../solutions/week_01_solutions.md)** | **➡️ [Next: Week 2 Exercises](week_02.md)**

---

## Beginner Exercise

### Task: Verify Your Environment

Set up the project and confirm every component is correctly installed by writing a small verification script.

### Requirements
- Create a file called `verify_setup.py` at the project root
- Import `gradio`, `numpy`, `matplotlib`, and `pathfinding_lab` and print each package version
- Use a `try/except` block so that a missing package prints a helpful error message instead of crashing
- Run the script and confirm all four imports succeed

### Hints
- Access a package version with `package.__version__`
- `pathfinding_lab` does not expose `__version__` directly; just confirm the import works
- Activate your virtual environment first: `source venv/bin/activate`

### Starter Code
```python
# verify_setup.py
import sys

packages = {
    "gradio": None,
    "numpy": None,
    "matplotlib": None,
}

for name in packages:
    try:
        mod = __import__(name)
        packages[name] = getattr(mod, "__version__", "installed (no __version__)")
        print(f"✓ {name}: {packages[name]}")
    except ImportError as e:
        print(f"✗ {name}: NOT found — {e}")

# Check pathfinding_lab separately
try:
    import pathfinding_lab  # noqa: F401
    print("✓ pathfinding_lab: installed")
except ImportError as e:
    print(f"✗ pathfinding_lab: NOT found — {e}")

print(f"\nPython: {sys.version}")
```

---

## Intermediate Exercise

### Task: Write Your First pytest Tests

Create a test file `tests/test_environment.py` that checks your environment and basic project utilities programmatically.

### Requirements
- Write at least **four** test functions using `pytest`
- Test 1: verify that `pathfinding_lab` can be imported without errors
- Test 2: verify that `Grid` can be instantiated with default parameters
- Test 3: verify that `Grid(5, 5, 0.0)` has `width == 5` and `height == 5`
- Test 4: verify that running `pytest` on the existing test suite passes (use `subprocess` or simply assert True as a placeholder if subprocess is unavailable)
- All tests must pass when you run `python -m pytest tests/test_environment.py -v`

### Hints
- Import `Grid` from `pathfinding_lab.core.grid`
- `Grid` signature is `Grid(rows, cols, obstacle_density, movement_mode?, random_seed?)`
- Use `from pathfinding_lab.core.types import MovementMode` for the movement mode
- A test function name must start with `test_`

### Starter Code
```python
# tests/test_environment.py
import pytest


def test_pathfinding_lab_import():
    """Verify the package can be imported."""
    # Your code here
    pass


def test_grid_can_be_created():
    """Verify Grid class is accessible and instantiable."""
    # Your code here
    pass


def test_grid_dimensions():
    """Verify Grid stores correct dimensions."""
    # Your code here — Grid has .width and .height attributes
    pass


def test_grid_empty_has_no_obstacles():
    """Verify a grid created with 0.0 obstacle density has no obstacles."""
    # Your code here
    pass
```

---

## Advanced Exercise

### Task: Understand and Extend pyproject.toml

Read the project's `pyproject.toml` and answer the following questions in comments inside a script, then implement one small extension.

### Requirements
- Open `pyproject.toml` and locate the `[project]` and `[tool.pytest.ini_options]` sections
- Write a Python script `explore_config.py` that reads `pyproject.toml` with the `tomllib` / `tomli` standard library module and prints:
  - The project name and version
  - All direct runtime dependencies (the `dependencies` list)
  - The pytest `testpaths` setting
- Add a new optional dependency group `[project.optional-dependencies]` called `dev-extras` with `ipython>=8.0` to `pyproject.toml`
- Verify the addition does not break `pip install -e .` (re-run the install and confirm it succeeds)

### Hints
- Python 3.11+ ships `tomllib`; for older versions use `pip install tomli` and `import tomli as tomllib`
- Open the file in binary mode: `open("pyproject.toml", "rb")`
- Adding a new optional-dependency group requires only a new `[project.optional-dependencies]` table; it does not affect existing dependencies

### Starter Code
```python
# explore_config.py
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # pip install tomli

from pathlib import Path

config_path = Path(__file__).parent / "pyproject.toml"

with open(config_path, "rb") as f:
    config = tomllib.load(f)

project = config["project"]
print(f"Project: {project['name']} v{project['version']}")

print("\nDependencies:")
for dep in project.get("dependencies", []):
    print(f"  - {dep}")

pytest_cfg = config.get("tool", {}).get("pytest", {}).get("ini_options", {})
print(f"\npytest testpaths: {pytest_cfg.get('testpaths', 'not set')}")
```

---

## Debugging Challenge

### Buggy Code

The following script is supposed to discover and count all test functions in the `tests/` directory, but it contains several bugs. Find and fix them.

```python
import os
import re

def count_test_functions(test_dir="tests"):
    """Count all test functions across all test files."""
    total = 0
    test_pattern = re.compile(r"def test_")  # Bug: should use re.compile once — this is fine actually
    file_count = 0

    for filename in os.listdir(test_dir):
        if not filename.endswith("_test.py"):  # Bug: pytest files start with test_, not end
            continue

        filepath = os.path.join(test_dir, filename)
        file_count += 1

        with open(filepath) as f:
            content = f.read()

        matches = test_pattern.findall(content)
        total = len(matches)  # Bug: should use += not =

    print(f"Found {file_count} test files with {total} test functions total")
    return total

count_test_functions()
```

### Expected Behavior

The function should:
1. Find all `test_*.py` files in the `tests/` directory
2. Count every function whose name starts with `test_` across all files
3. Print and return the correct total count

### Hints
- Check how pytest discovers test files (prefix vs suffix)
- Look at how the running total is updated inside the loop
- Consider what happens if `test_dir` does not exist — is that handled?

---

**✅ [See Solutions](../solutions/week_01_solutions.md)** | **📚 [Back to Week 1 Docs](../docs/week_01_python_project_setup.md)** | **➡️ [Next: Week 2 Exercises](week_02.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
