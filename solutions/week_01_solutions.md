# Week 1: Solutions

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **📚 [Week 1 Documentation](../docs/week_01_python_project_setup.md)** | **📝 [Week 1 Exercises](../exercises/week_01.md)** | **➡️ [Next: Week 2 Solutions](week_02_solutions.md)**

---

## Beginner Exercise Solution

### Explanation

This exercise confirms that your virtual environment is correctly configured and that every required package is available before you write a single line of pathfinding code. Using `try/except` around each import makes the script resilient: a missing package prints a clear error instead of crashing with an unhelpful traceback.

The pattern `getattr(mod, "__version__", "installed")` is a safe way to read a version string because not every package exposes `__version__` at the top level.

### Code

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

try:
    import pathfinding_lab  # noqa: F401
    print("✓ pathfinding_lab: installed")
except ImportError as e:
    print(f"✗ pathfinding_lab: NOT found — {e}")
    print("  Tip: run  pip install -e .  from the project root")

print(f"\nPython: {sys.version}")
```

**Expected output (versions will vary):**
```
✓ gradio: 4.x.x
✓ numpy: 1.x.x
✓ matplotlib: 3.x.x
✓ pathfinding_lab: installed

Python: 3.x.x ...
```

### Key Concepts

- **Virtual environments**: isolate project dependencies from system Python
- **`try/except ImportError`**: graceful degradation when a package is missing
- **`getattr` with default**: safe attribute access that won't raise `AttributeError`
- **Editable install (`pip install -e .`)**: makes local source changes immediately importable

### Testing Advice

Run this script immediately after cloning the repository and again after any `pip install` step. If any import fails, the fix is almost always one of:
1. You forgot to activate the virtual environment
2. You haven't run `pip install -r requirements.txt` yet
3. You haven't run `pip install -e .` to install the local package

---

## Intermediate Exercise Solution

### Explanation

pytest discovers tests by scanning for files matching `test_*.py` (or `*_test.py`), then collecting functions whose names start with `test_`. Writing tests for the environment itself gives you instant feedback when something in the project breaks — and it teaches you the pytest conventions you'll rely on throughout all 12 weeks.

### Code

```python
# tests/test_environment.py
import pytest


def test_pathfinding_lab_import():
    """Verify the package can be imported without errors."""
    import pathfinding_lab  # noqa: F401


def test_grid_can_be_created():
    """Verify Grid class is accessible and can be instantiated."""
    from pathfinding_lab.core.grid import Grid
    from pathfinding_lab.core.types import MovementMode

    grid = Grid(5, 5, 0.0, MovementMode.FOUR_DIRECTIONAL)
    assert grid is not None


def test_grid_dimensions():
    """Verify Grid stores correct dimensions."""
    from pathfinding_lab.core.grid import Grid
    from pathfinding_lab.core.types import MovementMode

    grid = Grid(5, 8, 0.0, MovementMode.FOUR_DIRECTIONAL)
    assert grid.width == 5
    assert grid.height == 8


def test_grid_empty_has_no_obstacles():
    """Verify a grid created with 0.0 obstacle density has no obstacles."""
    from pathfinding_lab.core.grid import Grid
    from pathfinding_lab.core.types import MovementMode

    grid = Grid(10, 10, 0.0, MovementMode.FOUR_DIRECTIONAL)
    assert len(grid.obstacles) == 0
```

Run with:
```bash
python -m pytest tests/test_environment.py -v
```

**Expected output:**
```
tests/test_environment.py::test_pathfinding_lab_import PASSED
tests/test_environment.py::test_grid_can_be_created PASSED
tests/test_environment.py::test_grid_dimensions PASSED
tests/test_environment.py::test_grid_empty_has_no_obstacles PASSED
```

### Key Concepts

- **Test discovery**: pytest finds `test_*.py` files and `test_*` functions automatically
- **`assert` statements**: the simplest form of test assertion in pytest
- **Local imports inside tests**: importing inside the test function makes the dependency explicit and the failure message clearer
- **`-v` flag**: verbose output shows each test name and its result

### Testing Advice

Always run `python -m pytest -q` (quiet mode) for a quick sanity check after any code change. Use `-v` when a test fails to see the full function name and assertion output.

---

## Advanced Exercise Solution

### Explanation

`pyproject.toml` is the modern, PEP 517-compliant replacement for `setup.py`. Reading it programmatically teaches you that configuration is just structured data — and makes it easy to write automation scripts (CI checks, dependency audits, etc.) that stay in sync with the actual project.

Adding an optional dependency group is a non-breaking change: it does not affect the default install but allows developers to run `pip install -e ".[dev-extras]"` to get the extras.

### Code

```python
# explore_config.py
try:
    import tomllib          # Python 3.11+
except ImportError:
    import tomli as tomllib  # pip install tomli

from pathlib import Path

config_path = Path(__file__).parent / "pyproject.toml"

with open(config_path, "rb") as f:
    config = tomllib.load(f)

project = config["project"]
print(f"Project : {project['name']} v{project['version']}")

print("\nDependencies:")
for dep in project.get("dependencies", []):
    print(f"  - {dep}")

pytest_cfg = config.get("tool", {}).get("pytest", {}).get("ini_options", {})
print(f"\npytest testpaths : {pytest_cfg.get('testpaths', 'not set')}")
```

**pyproject.toml addition** (add after the `[project]` section):

```toml
[project.optional-dependencies]
dev-extras = [
    "ipython>=8.0",
]
```

Verify it works:
```bash
pip install -e ".[dev-extras]"
python -c "import IPython; print(IPython.__version__)"
```

### Key Concepts

- **`tomllib` / `tomli`**: standard way to parse TOML files in Python
- **`[project.optional-dependencies]`**: lets consumers opt into extra packages without affecting the default install
- **Binary mode for TOML**: `open(..., "rb")` is required by the `tomllib` API
- **Editable install**: `pip install -e .` installs the package in "development mode" so source changes are reflected immediately

### Testing Advice

After modifying `pyproject.toml`, always run `pip install -e .` again and then `python -m pytest -q` to confirm nothing is broken. You can also run `pip check` to detect dependency conflicts.

---

## Debugging Challenge Solution

### Bugs Found

**Bug 1: Wrong filename suffix**
- **Location**: `if not filename.endswith("_test.py"):`
- **Problem**: pytest (and this project) uses the `test_*.py` prefix convention, not `*_test.py` suffix. Files like `test_grid.py` would be skipped entirely.
- **Fix**: `if not filename.startswith("test_") or not filename.endswith(".py"):`

**Bug 2: Overwriting instead of accumulating the count**
- **Location**: `total = len(matches)`
- **Problem**: Each iteration replaces `total` with the count from the current file, discarding all previous counts.
- **Fix**: `total += len(matches)`

**Bug 3: No guard for missing directory** (bonus)
- **Location**: `os.listdir(test_dir)` called without checking existence
- **Problem**: If `test_dir` doesn't exist (e.g., wrong working directory), the script raises `FileNotFoundError` with no explanation.
- **Fix**: Add `if not os.path.isdir(test_dir): raise FileNotFoundError(...)` at the start.

### Corrected Code

```python
import os
import re


def count_test_functions(test_dir="tests"):
    """Count all test functions across all test files."""
    if not os.path.isdir(test_dir):
        raise FileNotFoundError(f"Test directory not found: {test_dir!r}")

    total = 0
    test_pattern = re.compile(r"def test_")
    file_count = 0

    for filename in os.listdir(test_dir):
        # Fix 1: pytest discovers files that START with test_
        if not (filename.startswith("test_") and filename.endswith(".py")):
            continue

        filepath = os.path.join(test_dir, filename)
        file_count += 1

        with open(filepath) as f:
            content = f.read()

        matches = test_pattern.findall(content)
        total += len(matches)  # Fix 2: accumulate, not overwrite

    print(f"Found {file_count} test files with {total} test functions total")
    return total


count_test_functions()
```

### What You Should Understand

1. **pytest naming conventions**: files must match `test_*.py` (or `*_test.py` if configured), and functions must start with `test_`. Knowing this prevents hours of confusion wondering why your tests are "not running".

2. **Accumulator pattern**: a very common bug is using `=` when you mean `+=` inside a loop. Always ask: "am I replacing the value or adding to it?"

3. **Defensive programming**: checking that a directory exists before calling `os.listdir()` turns an opaque `FileNotFoundError` into a clear, actionable message.

4. **`re.findall` vs `re.search`**: `findall` returns all matches in the string (useful for counting), while `search` only finds the first match.

---

**📝 [Back to Week 1 Exercises](../exercises/week_01.md)** | **📚 [Week 1 Documentation](../docs/week_01_python_project_setup.md)** | **➡️ [Next: Week 2 Solutions](week_02_solutions.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
