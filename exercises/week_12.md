# Week 12: Final Project Exercises

Welcome to the final week! These exercises integrate everything you've learned throughout the course. You'll build integration tests, implement a custom maze generator, optimize performance, and complete a capstone project.

---

## Exercise 1: Integration Testing (Beginner)

### Task
Write comprehensive integration tests that verify the Gradio UI works correctly end-to-end. Your tests should verify that grid generation, algorithm execution, and visualization all work together seamlessly.

### Requirements

Create a test file `tests/test_integration.py` that includes:

1. **Test Grid Generation Through UI**
   - Verify that `generate_grid()` produces valid grids with correct dimensions
   - Test various parameter combinations (different sizes, densities, movement modes)
   - Ensure start and goal positions are not blocked by obstacles
   - Validate that the returned figure is a valid matplotlib plot

2. **Test Algorithm Routing**
   - Verify all 6 algorithms can be selected and executed
   - Confirm the correct algorithm function is called for each selection
   - Test that invalid algorithm names are handled gracefully
   - Verify heuristic selection works for A* and Greedy Best-First

3. **Test Visualization Output**
   - Ensure `run_algorithm()` returns valid matplotlib figures
   - Verify metrics DataFrame contains expected columns
   - Check that path visualization appears when path is found
   - Confirm visited nodes are displayed correctly

4. **Test All Algorithms End-to-End**
   - Create a test that runs all 6 algorithms through the UI functions
   - Verify each algorithm returns a SearchResult
   - Ensure metrics are calculated correctly
   - Test comparison mode with `compare_algorithms()`

### Starter Code

```python
"""Integration tests for Gradio UI."""

import pytest
import pandas as pd
from matplotlib.figure import Figure

from pathfinding_lab.ui.gradio_app import (
    generate_grid,
    run_algorithm,
    compare_algorithms,
    current_grid,
)


def test_generate_grid_creates_valid_grid():
    """Test that generate_grid produces a valid grid."""
    # Generate a 10x10 grid with 20% obstacle density
    fig, message = generate_grid(
        width=10,
        height=10,
        obstacle_density=0.2,
        seed=42,
        movement_mode="4-directional",
        start_row=0,
        start_col=0,
        goal_row=9,
        goal_col=9
    )

    # TODO: Add assertions
    # - Check that fig is a matplotlib Figure
    # - Verify message contains success text
    # - Check global current_grid is set
    # - Verify grid has correct dimensions
    pass


def test_all_algorithms_can_run():
    """Test that all 6 algorithms can be executed through UI."""
    # First generate a grid
    generate_grid(10, 10, 0.2, 42, "4-directional", 0, 0, 9, 9)

    algorithms = ["BFS", "DFS", "Dijkstra", "Greedy Best-First", "A*", "Bidirectional BFS"]

    for algo in algorithms:
        # TODO: Run algorithm and verify results
        # - Call run_algorithm with algorithm name
        # - Check that result contains valid figure, metrics, and message
        # - Verify metrics DataFrame has expected columns
        pass


# TODO: Add more integration tests
```

### Hints

- Use `pytest.fixture` to set up common test grids
- Import `current_grid` to access the global grid state
- Use `isinstance(fig, Figure)` to verify matplotlib plots
- Check DataFrame columns with `assert 'Algorithm' in df.columns`
- Test both successful paths and blocked scenarios
- Remember to test edge cases (0% obstacles, 50% obstacles, different seeds)

---

## Exercise 2: Custom Maze Generator (Intermediate)

### Task
Implement the **Recursive Division** maze generation algorithm and integrate it into the Gradio UI. This algorithm creates perfect mazes by recursively dividing the grid into chambers and creating passages.

### Algorithm Overview

Recursive Division works as follows:

1. Start with an empty grid (no obstacles)
2. Choose a random orientation (horizontal or vertical)
3. Divide the grid with a wall in that orientation
4. Create a single gap in that wall
5. Recursively apply steps 2-4 to each chamber

This creates a maze with guaranteed solvability (exactly one path between any two points).

### Requirements

1. **Implement the Algorithm**
   - Add `recursive_division_maze()` function to `src/pathfinding_lab/mazes/generators.py`
   - Support both horizontal and vertical divisions
   - Ensure at least one passage through each wall
   - Handle edge cases (chambers too small to divide)

2. **Ensure Solvability**
   - Verify path exists from start to goal
   - Test with various grid sizes
   - Handle edge cases where start/goal are in same chamber

3. **Integrate with UI**
   - Add "Recursive Division" option to maze preset dropdown
   - Update `generate_grid()` to support preset parameter
   - Create new UI control for maze presets

4. **Documentation**
   - Add docstring explaining the algorithm
   - Include complexity analysis (time and space)
   - Provide usage examples

### Starter Code

```python
def recursive_division_maze(
    grid: Grid,
    start: Position,
    goal: Position,
    min_chamber_size: int = 2
) -> None:
    """
    Generate a maze using recursive division algorithm.

    Creates a perfect maze where exactly one path exists between any two cells.

    Algorithm:
    1. Start with empty grid
    2. Recursively divide grid with walls
    3. Create single passage through each wall
    4. Stop when chambers are too small

    Time Complexity: O(width * height)
    Space Complexity: O(log(width) + log(height)) for recursion stack

    Args:
        grid: Grid to generate maze on
        start: Start position (kept clear)
        goal: Goal position (kept clear)
        min_chamber_size: Minimum chamber size before stopping division

    Example:
        >>> grid = Grid(20, 20, 0.0, MovementMode.FOUR_DIRECTIONAL)
        >>> start = (0, 0)
        >>> goal = (19, 19)
        >>> recursive_division_maze(grid, start, goal)
        >>> # Grid now contains a perfect maze
    """
    grid.reset()  # Clear all obstacles

    def divide_chamber(row_start, row_end, col_start, col_end):
        """
        Recursively divide a chamber with a wall and passage.

        Args:
            row_start, row_end: Row bounds of chamber
            col_start, col_end: Column bounds of chamber
        """
        # Calculate chamber dimensions
        chamber_height = row_end - row_start
        chamber_width = col_end - col_start

        # Base case: chamber too small to divide
        if chamber_height < min_chamber_size or chamber_width < min_chamber_size:
            return

        # TODO: Implement recursive division logic
        # 1. Choose orientation (horizontal or vertical)
        # 2. Pick random position for wall
        # 3. Create wall with one gap
        # 4. Recursively divide resulting chambers

        pass

    # Start recursive division on entire grid
    divide_chamber(0, grid.height, 0, grid.width)
```

### Implementation Steps

1. **Choose Orientation**
   ```python
   # Prefer longer dimension for more interesting mazes
   if chamber_width > chamber_height:
       orientation = "vertical"
   elif chamber_height > chamber_width:
       orientation = "horizontal"
   else:
       orientation = random.choice(["horizontal", "vertical"])
   ```

2. **Create Wall with Passage**
   ```python
   if orientation == "horizontal":
       wall_row = random.randint(row_start + 1, row_end - 2)
       passage_col = random.randint(col_start, col_end - 1)

       # Add wall except at passage
       for col in range(col_start, col_end):
           if col != passage_col:
               pos = (wall_row, col)
               if pos != start and pos != goal:
                   grid.add_obstacle(pos)
   ```

3. **Recursive Calls**
   ```python
   # Divide resulting chambers
   divide_chamber(row_start, wall_row + 1, col_start, col_end)  # Top
   divide_chamber(wall_row + 1, row_end, col_start, col_end)    # Bottom
   ```

### Hints

- Use `random.randint()` for selecting wall positions and passages
- Always keep start and goal positions clear
- Test with small grids first (10x10) before scaling up
- Add debug visualization to see division process
- Consider adding orientation bias parameter for different maze styles
- Verify connectivity using BFS from start to goal after generation

### Testing

Write tests to verify:
- Maze generation completes without errors
- Start and goal remain clear
- Path exists from start to goal (use BFS to verify)
- No isolated regions exist
- Walls form connected structure

---

## Exercise 3: Performance Optimization (Advanced)

### Task
Profile the pathfinding application to identify performance bottlenecks, implement optimizations, and measure improvements. This exercise focuses on real-world optimization techniques.

### Requirements

1. **Profile the Application**
   - Use `cProfile` to profile algorithm execution
   - Identify top 10 time-consuming functions
   - Create profile reports for all 6 algorithms
   - Compare performance on different grid sizes (10x10, 50x50, 100x100)

2. **Identify Bottlenecks**
   - Analyze heuristic calculation frequency
   - Examine neighbor generation efficiency
   - Check data structure access patterns
   - Review visualization rendering time

3. **Implement Optimizations**
   - Cache heuristic calculations for repeated positions
   - Optimize neighbor generation with pre-computed offsets
   - Use more efficient data structures (consider `heapq` optimizations)
   - Profile again and measure improvement

4. **Document Results**
   - Create before/after comparison report
   - Include profiling output and analysis
   - Provide optimization recommendations
   - Calculate speedup ratios

### Profiling Starter Code

```python
"""Performance profiling and optimization."""

import cProfile
import pstats
from io import StringIO
from typing import Dict, Any

from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.core.types import MovementMode
from pathfinding_lab.heuristics.manhattan import manhattan_distance


def profile_algorithm(algorithm_func, grid, start, goal, **kwargs):
    """
    Profile an algorithm and return statistics.

    Args:
        algorithm_func: Algorithm function to profile
        grid: Grid to run on
        start: Start position
        goal: Goal position
        **kwargs: Additional arguments for algorithm

    Returns:
        Dictionary with profiling stats
    """
    profiler = cProfile.Profile()

    # Run with profiling
    profiler.enable()
    result = algorithm_func(grid, start, goal, **kwargs)
    profiler.disable()

    # Extract stats
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions

    return {
        'result': result,
        'profile_output': stream.getvalue(),
        'stats': stats
    }


def benchmark_grid_sizes():
    """
    Benchmark A* on different grid sizes.

    Returns:
        Dictionary mapping grid size to profiling results
    """
    results = {}

    for size in [10, 20, 50, 100]:
        print(f"\n{'='*60}")
        print(f"Profiling A* on {size}x{size} grid")
        print('='*60)

        grid = Grid(size, size, 0.2, MovementMode.FOUR_DIRECTIONAL, random_seed=42)
        start = (0, 0)
        goal = (size-1, size-1)

        profile_data = profile_algorithm(astar, grid, start, goal, heuristic=manhattan_distance)
        results[size] = profile_data

        print(profile_data['profile_output'])
        print(f"\nAlgorithm Result:")
        print(f"  Success: {profile_data['result'].success}")
        print(f"  Runtime: {profile_data['result'].runtime_ms:.2f}ms")
        print(f"  Nodes Visited: {profile_data['result'].nodes_visited}")

    return results


# TODO: Run profiling
if __name__ == "__main__":
    results = benchmark_grid_sizes()

    # TODO: Analyze results and identify optimization opportunities
```

### Optimization Techniques

#### 1. Heuristic Caching

```python
from functools import lru_cache

@lru_cache(maxsize=10000)
def cached_manhattan_distance(p1, p2):
    """Manhattan distance with LRU cache."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
```

#### 2. Optimized Neighbor Generation

```python
# Before: Creating tuples each time
def get_neighbors(pos):
    neighbors = []
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        neighbors.append((pos[0] + dr, pos[1] + dc))
    return neighbors

# After: Pre-computed offsets, vectorized
FOUR_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def get_neighbors_optimized(pos):
    return [(pos[0] + dr, pos[1] + dc) for dr, dc in FOUR_DIRECTIONS]
```

#### 3. Efficient Data Structures

```python
# Consider using deque instead of list for BFS queue
from collections import deque

# Use set for O(1) membership testing
visited = set()  # Instead of list
```

### Analysis Tasks

1. **Compare Function Call Counts**
   - Which functions are called most frequently?
   - Are there unnecessary repeated calculations?
   - Can any function calls be eliminated?

2. **Measure Memory Usage**
   ```python
   import tracemalloc

   tracemalloc.start()
   result = astar(grid, start, goal, manhattan_distance)
   current, peak = tracemalloc.get_traced_memory()
   tracemalloc.stop()

   print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
   print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
   ```

3. **Create Performance Report**
   - Document baseline performance
   - List implemented optimizations
   - Show before/after metrics
   - Calculate speedup percentage

### Deliverables

Create `docs/performance_optimization_report.md` with:
- Profiling methodology
- Bottleneck analysis
- Optimization implementations
- Performance improvements (tables and charts)
- Recommendations for further optimization

### Hints

- Focus on hot paths (functions called thousands of times)
- Heuristic calculations are often the biggest bottleneck
- Grid boundary checks can be optimized
- Visualization rendering is separate from algorithm performance
- Use `timeit` for micro-benchmarks of specific functions
- Test optimizations don't break correctness (run existing tests)

---

## Exercise 4: Capstone Project

### Overview

Choose ONE of the following six capstone projects. Each project represents a substantial extension to the pathfinding laboratory and should demonstrate mastery of course concepts.

### Project Timeline

- **Week 1**: Planning and design (architecture, API design)
- **Week 2**: Core implementation
- **Week 3**: Testing and refinement
- **Week 4**: Documentation and polish

---

### Option 1: Real-Time Animation System

**Difficulty**: Medium

**Description**: Implement a real-time step-by-step animation system that shows algorithm execution in progress.

**Requirements**:
1. Animate algorithm execution step-by-step
2. Add play/pause/step controls
3. Adjustable animation speed
4. Display current node being explored
5. Show frontier and visited sets dynamically
6. Export animation as GIF or video

**Technical Specifications**:
- Use Gradio's `gr.State` for animation state
- Implement generator-based algorithm stepping
- Create reusable animation framework
- Support all 6 algorithms

**Deliverables**:
- `src/pathfinding_lab/animation/realtime.py` - Animation engine
- `src/pathfinding_lab/animation/controls.py` - UI controls
- Updated Gradio interface with animation tab
- Documentation and examples
- Test suite for animation system

**Starter Code**:
```python
def astar_generator(grid, start, goal, heuristic):
    """Generator version of A* that yields each step."""
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        current = heapq.heappop(open_set)[1]

        # Yield current state
        yield {
            'current': current,
            'open_set': [node for _, node in open_set],
            'visited': set(came_from.keys()),
            'path': reconstruct_path(came_from, current)
        }

        if current == goal:
            return

        # ... rest of algorithm
```

---

### Option 2: Interactive Grid Editor

**Difficulty**: Medium

**Description**: Create an interactive grid editor where users can draw obstacles, move start/goal, and see results in real-time.

**Requirements**:
1. Click-and-drag obstacle drawing
2. Brush size and pattern selection
3. Eraser mode for removing obstacles
4. Movable start and goal markers
5. Real-time algorithm execution on changes
6. Save/load grid configurations

**Technical Specifications**:
- Use Gradio's interactive plot events
- Implement efficient grid update system
- Support undo/redo functionality
- Add grid templates library

**Deliverables**:
- `src/pathfinding_lab/ui/grid_editor.py` - Editor component
- `src/pathfinding_lab/ui/drawing_tools.py` - Drawing utilities
- Grid save/load functionality (JSON format)
- Updated Gradio interface
- User guide with screenshots

**Key Features**:
- Paint mode, erase mode, move mode
- Symmetry tools (mirror, rotate)
- Import/export grid as JSON or image
- Preset patterns (walls, rooms, mazes)

---

### Option 3: PDF Report Generator

**Difficulty**: Easy-Medium

**Description**: Generate comprehensive PDF reports with algorithm comparison, visualizations, and performance metrics.

**Requirements**:
1. Multi-page PDF with cover page
2. Embedded matplotlib visualizations
3. Tables with algorithm metrics
4. Grid configuration details
5. Performance charts and graphs
6. Customizable report templates

**Technical Specifications**:
- Use `reportlab` or `matplotlib.backends.backend_pdf`
- Create reusable report templates
- Support batch report generation
- Include statistical analysis

**Deliverables**:
- `src/pathfinding_lab/reporting/pdf_generator.py`
- `src/pathfinding_lab/reporting/templates.py`
- Sample reports (examples/)
- Gradio UI integration
- Documentation

**Report Sections**:
1. Executive Summary
2. Grid Configuration
3. Algorithm Comparison (table and charts)
4. Individual Algorithm Details
5. Performance Analysis
6. Recommendations

---

### Option 4: Path Smoothing with Splines

**Difficulty**: Hard

**Description**: Implement path smoothing using Catmull-Rom splines or B-splines to create natural-looking curved paths.

**Requirements**:
1. Smooth jagged pathfinding results
2. Maintain obstacle avoidance
3. Adjustable smoothing parameters
4. Compare original vs smoothed path cost
5. Support different spline types
6. Real-time smoothing preview

**Technical Specifications**:
- Implement Catmull-Rom spline interpolation
- Add collision detection for smoothed paths
- Calculate smoothed path cost
- Visualize control points and curves

**Deliverables**:
- `src/pathfinding_lab/smoothing/splines.py`
- `src/pathfinding_lab/smoothing/collision.py`
- Visual comparison tool
- Performance benchmarks
- Mathematical documentation

**Algorithm Outline**:
```python
def smooth_path_catmull_rom(path, grid, tension=0.5, segments=10):
    """
    Smooth path using Catmull-Rom splines.

    Args:
        path: List of waypoints
        grid: Grid for collision detection
        tension: Spline tension (0 = loose, 1 = tight)
        segments: Number of segments between waypoints

    Returns:
        Smoothed path as list of positions
    """
    # TODO: Implement spline interpolation
    # 1. For each path segment, compute control points
    # 2. Generate spline curve
    # 3. Check for collisions with obstacles
    # 4. Adjust curve if collision detected
    pass
```

---

### Option 5: Jump Point Search Optimization

**Difficulty**: Hard

**Description**: Implement Jump Point Search (JPS), an optimization for A* that dramatically reduces nodes expanded on uniform-cost grids.

**Requirements**:
1. Implement core JPS algorithm
2. Support 4-directional and 8-directional movement
3. Compare performance vs A* (nodes expanded)
4. Handle weighted grids
5. Visualize jump points and pruned nodes
6. Comprehensive testing

**Technical Specifications**:
- Implement jump point detection
- Add forced neighbor identification
- Optimize straight-line jumping
- Integrate with existing algorithm framework

**Deliverables**:
- `src/pathfinding_lab/algorithms/jps.py`
- `src/pathfinding_lab/algorithms/jump_points.py` - Jump detection
- Performance comparison analysis
- Visualization of pruned search space
- Algorithm explanation document

**Key Concepts**:
- Jump points: Points where direction changes are necessary
- Forced neighbors: Neighbors that can't be pruned
- Straight-line jumping: Skip intermediate nodes
- Diagonal jumping: Handle diagonal movement

**Expected Performance**:
- 10x fewer nodes expanded vs A* on open grids
- Same path cost (optimal paths)
- Faster execution time on large grids

---

### Option 6: Multi-Agent Pathfinding

**Difficulty**: Very Hard

**Description**: Extend the system to handle multiple agents finding paths simultaneously while avoiding collisions.

**Requirements**:
1. Support 2-10 agents with different start/goal pairs
2. Implement collision avoidance (agents can't occupy same cell)
3. Solve using Conflict-Based Search (CBS) or similar
4. Visualize all agents and their paths
5. Handle dynamic re-planning
6. Measure solution quality (makespan, total cost)

**Technical Specifications**:
- Implement CBS algorithm
- Add conflict detection
- Create agent priority system
- Support time-expanded state space

**Deliverables**:
- `src/pathfinding_lab/multi_agent/cbs.py` - CBS algorithm
- `src/pathfinding_lab/multi_agent/conflict.py` - Conflict detection
- `src/pathfinding_lab/multi_agent/agent.py` - Agent class
- Multi-agent visualization
- Gradio interface for multi-agent scenarios

**Algorithm Overview**:
```python
def conflict_based_search(grid, agents):
    """
    Find paths for multiple agents without collisions.

    Args:
        grid: Shared grid
        agents: List of (start, goal) tuples

    Returns:
        Dictionary mapping agent ID to path
    """
    # High-level search:
    # 1. Find initial paths for all agents (independent A*)
    # 2. Detect conflicts (same cell, same time)
    # 3. Split into branches: constrain one agent
    # 4. Recursively solve sub-problems
    # 5. Return first complete solution
    pass
```

**Challenges**:
- Exponential branching in worst case
- Need efficient conflict detection
- Priority ordering affects performance
- Visualization complexity

---

### General Capstone Requirements

All capstone projects must include:

1. **Code Quality**
   - Type hints on all functions
   - Comprehensive docstrings
   - Follows existing code style
   - No lint errors

2. **Testing**
   - Unit tests for core functionality
   - Integration tests with existing system
   - Edge case coverage
   - Test coverage > 80%

3. **Documentation**
   - Algorithm explanation (if applicable)
   - API documentation
   - Usage examples
   - Performance characteristics

4. **Integration**
   - Works with existing Gradio UI
   - Follows project structure
   - Compatible with all existing features
   - No breaking changes

5. **Presentation**
   - Project README
   - Demo video or screenshots
   - Performance analysis
   - Future work section

### Evaluation Criteria

Projects will be evaluated on:
- **Functionality** (40%): Does it work correctly?
- **Code Quality** (20%): Clean, maintainable code?
- **Testing** (15%): Comprehensive test coverage?
- **Documentation** (15%): Clear and complete?
- **Innovation** (10%): Creative solutions and extras?

---

## Submission Guidelines

For all exercises:

1. Create a new branch: `git checkout -b week-12-solutions`
2. Commit your work with clear messages
3. Update relevant documentation
4. Ensure all tests pass: `pytest`
5. Create a summary document: `docs/week_12_summary.md`

### Week 12 Summary Document

Include:
- Exercise 1: Test coverage report and key findings
- Exercise 2: Maze generation examples and analysis
- Exercise 3: Performance optimization results (before/after)
- Exercise 4: Capstone project overview and demo
- Challenges faced and solutions
- Total time spent
- Key learnings

---

**See solutions/week_12_solutions.md for reference implementations**

**Good luck with your final project!**
