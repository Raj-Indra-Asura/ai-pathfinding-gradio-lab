# Week 0: The Python You'll Need

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **🧭 [End-to-End Pipeline](END_TO_END_PIPELINE.md)** | **🔬 [Notebook](../notebooks/00_python_prerequisites.ipynb)** | **➡️ [Next: Week 1](week_01_python_project_setup.md)**

---

> **How to use this page.** This is a *reference you read once and revisit* — **open it
> whenever a later week uses a symbol you don't recognize.** Every concept below is taught
> by pointing at this project's own code, so it never feels abstract. You only need **basic
> Python (variables, functions, loops, `if`) and basic data structures (lists, dictionaries)**
> to start. Each section ends with a plain-English *"why we use this here."*

## Prerequisites

You should already be comfortable with:
- Running Python from a terminal and importing modules.
- Variables, `if`/`else`, `for`/`while` loops, and writing simple functions.
- Lists (`[...]`) and dictionaries (`{key: value}`).

Everything else — tuples, sets, classes, dataclasses, dunder methods, enums, type hints,
`deque`, `heapq`, `float('inf')`, and `try/except` — is explained below.

## Learning Goals

By the end of this page, you will be able to **read** (not necessarily write from scratch):
- Tuple unpacking and the `Position = (row, col)` convention used everywhere in this project.
- Why this project stores obstacles in a **set** and what "O(1) lookup" means.
- Just enough about **classes and `self`** to read `Grid`.
- **Dataclasses** like `Node` and `SearchResult`.
- **Dunder methods** (`__lt__`, `__eq__`, `__hash__`) and why a priority queue needs them.
- **Enums** like `MovementMode` and why we don't just use strings.
- How to **read type hints** such as `Position`, `Callable[[Position, Position], float]`.
- `collections.deque`, `heapq`, and `float('inf')` — and why each is the right tool.
- `try/except` basics used in the Week 1 exercise.

## Theory: The Python You'll Need

<a id="prereq-tuples"></a>
### 1. Tuples and Tuple Unpacking

A **tuple** is an ordered, *fixed* collection written with parentheses: `(2, 5)`. Unlike a
list, you don't change it after creating it — which makes it perfect for a coordinate.

**Tuple unpacking** assigns each element to its own variable in one line:

```python
position = (2, 5)
row, col = position   # row == 2, col == 5
```

This project represents every grid cell as a `(row, col)` tuple and gives it a name:

```python
# src/pathfinding_lab/core/types.py
Position = Tuple[int, int]   # "a Position is a (row, col) pair of ints"
```

You will see `row, col = position` constantly — for example inside `Grid.is_valid`:

```python
# src/pathfinding_lab/core/grid.py
def is_valid(self, position: Position) -> bool:
    row, col = position
    return 0 <= row < self.height and 0 <= col < self.width
```

> **Why we use this here:** coordinates never change once created, so a tuple is the natural
> choice. Tuples can also be dictionary keys and set members (lists cannot), which is exactly
> what the algorithms need when they store `cost_so_far[(row, col)]`.

<a id="prereq-collections"></a>
### 2. Sets vs Lists vs Dicts — and Big-O in Plain Words

These three built-in containers look similar but are good at different things.

| Container | Looks like | Good at | Keeps order? | Duplicates? |
| --- | --- | --- | --- | --- |
| **list** | `[a, b, c]` | keeping a sequence in order | yes | yes |
| **set** | `{a, b, c}` | "is this item present?" checks | no | no |
| **dict** | `{k: v}` | looking up a value *by key* | yes (insertion) | keys unique |

<a id="prereq-bigo"></a>
**Big-O in plain words (read this once, reuse the vocabulary all course).**
Big-O describes *how the work grows as the data grows*. We care about two cases here:

- **O(1) — "constant time / fast lookup":** the work stays the same no matter how big the
  container is. Checking `pos in my_set` is O(1): Python jumps straight to the answer.
- **O(n) — "linear time":** the work grows in step with the number of items `n`. Checking
  `pos in my_list` is O(n): Python may have to scan every item.

On a 100×100 grid (10,000 cells), an O(1) check is effectively instant, while repeating an
O(n) scan thousands of times inside a search loop becomes painfully slow.

That is exactly why this project stores obstacles in a **set**:

```python
# src/pathfinding_lab/core/grid.py
self.obstacles: Set[Position] = set()

def is_obstacle(self, position: Position) -> bool:
    return position in self.obstacles   # O(1) fast lookup
```

> **Why we use this here:** algorithms ask "is this cell blocked?" and "have I visited this
> cell?" millions of times. A **set** (or a **dict** keyed by position, like
> `cost_so_far`) answers in O(1). A list would answer the same question in O(n) and make the
> whole search slow. Later weeks reuse the words *O(1)* and *O(n)* — they mean exactly this.

<a id="prereq-classes"></a>
### 3. Classes and `self` (Just Enough to Read `Grid`)

A **class** bundles data together with the functions that operate on it. An **instance** is
one concrete object made from the class. Inside the class, `self` means "this particular
instance."

```python
# src/pathfinding_lab/core/grid.py (trimmed)
class Grid:
    def __init__(self, width, height, ...):
        self.width = width      # store data ON this instance
        self.height = height

    def is_valid(self, position):
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width
```

- `__init__` is the **constructor** — it runs when you write `Grid(20, 20)`.
- `self.width = width` saves a value *on the instance* so other methods can read it later.
- A **method** is just a function defined inside the class whose first parameter is `self`.
- You call a method with `grid.is_valid((3, 4))` — Python passes `grid` in as `self` for you.

> **Why we use this here:** the grid owns lots of related state (size, obstacles, movement
> mode) and behavior (neighbor lookup, validity checks). A class keeps them together so every
> algorithm can share one consistent `Grid` object instead of passing loose variables around.

<a id="prereq-dataclasses"></a>
### 4. Dataclasses (`@dataclass`, default fields)

A **dataclass** is a shortcut for a class that mostly just holds fields. The `@dataclass`
decorator writes the boilerplate `__init__` for you. You list each field with a type and an
optional **default value**.

```python
# src/pathfinding_lab/core/node.py (trimmed)
from dataclasses import dataclass, field

@dataclass
class Node:
    position: Position
    g_cost: float = float('inf')   # default: "not reached yet"
    h_cost: float = 0.0
    parent: Optional['Node'] = None
    is_obstacle: bool = False
```

For fields whose default is a *mutable* object (like a list), you must use
`field(default_factory=list)` instead of `= []`, as `SearchResult` does:

```python
# src/pathfinding_lab/core/result.py (trimmed)
@dataclass
class SearchResult:
    algorithm_name: str
    success: bool
    path: List[Position] = field(default_factory=list)   # new empty list each time
    nodes_visited: int = 0
```

> **Why we use this here:** `Node` and `SearchResult` are pure data holders. Dataclasses give
> us a clean constructor, sensible defaults, and a readable `repr` for free, so the code stays
> short and the fields are self-documenting.

<a id="prereq-dunder"></a>
### 5. Dunder Methods (`__lt__`, `__eq__`, `__hash__`)

"Dunder" = **d**ouble **under**score. These specially named methods let *your* objects work
with Python's built-in operators and containers.

- `__eq__(self, other)` defines what `==` means for your object.
- `__hash__(self)` returns an int so the object can go in a **set** or be a **dict** key.
- `__lt__(self, other)` defines `<`, which is what `heapq` uses to decide ordering.

```python
# src/pathfinding_lab/core/node.py (trimmed)
def __lt__(self, other):                # used by a priority queue
    return self.f_cost < other.f_cost
def __eq__(self, other):                # two nodes are "equal" if same cell
    return self.position == other.position
def __hash__(self):                     # so a Node can live in a set
    return hash(self.position)
```

**Why a priority queue needs ordering:** a priority queue (see `heapq` below) must always hand
back the *smallest* item first. To compare two items it evaluates `a < b`, i.e. `a.__lt__(b)`.
If your objects don't define `__lt__`, Python raises `TypeError: '<' not supported`. By making
`Node` compare on `f_cost`, the queue always pops the most promising node next.

> **Why we use this here:** A* and Dijkstra repeatedly ask "which option is cheapest?" Defining
> `__lt__` lets the priority queue answer that automatically. (In practice the algorithms in
> this repo push plain `(cost, position)` tuples — Python already knows how to order tuples —
> but `Node` shows the same idea explicitly.)

<a id="prereq-enums"></a>
### 6. Enums (`MovementMode`) — Why Not Just Strings

An **enum** is a fixed set of named choices. Instead of passing around magic strings like
`"4-dir"`, you pass a named member that the editor and Python can check.

```python
# src/pathfinding_lab/core/types.py
from enum import Enum

class MovementMode(Enum):
    FOUR_DIRECTIONAL = 4
    EIGHT_DIRECTIONAL = 8
```

```python
# usage
grid = Grid(10, 10, movement_mode=MovementMode.EIGHT_DIRECTIONAL)
```

> **Why we use this here:** there are exactly two movement modes. An enum makes the valid
> options explicit and typo-proof. With a plain string, `"8-directional"` vs `"8-dir"` vs
> `"eight"` would all be different and you'd only find the mistake at runtime. With an enum,
> the wrong name is caught immediately.

<a id="prereq-typehints"></a>
### 7. Type Hints — How to *Read* Them

Type hints annotate what a value is *expected* to be. They don't change how the code runs;
they document intent and let tools catch mistakes. You mostly need to **read** them, not write
them. Here's the vocabulary you'll meet in this project:

| You see... | Read it as... |
| --- | --- |
| `position: Position` | "`position` is a `(row, col)` tuple of ints" |
| `-> bool` | "this function returns `True`/`False`" |
| `-> SearchResult` | "this function returns a `SearchResult` object" |
| `Optional[Node]` | "a `Node`, or `None`" |
| `List[Position]` | "a list of positions" |
| `Dict[Position, float]` | "a dict mapping a position to a number" |
| `Callable[[Position, Position], float]` | "a *function* taking two positions and returning a number" — i.e. a heuristic |

For example, A* declares the heuristic it accepts like this:

```python
# src/pathfinding_lab/algorithms/astar.py
def astar(grid: Grid, start: Position, goal: Position,
          heuristic: Callable[[Position, Position], float]) -> SearchResult:
```

> **Why we use this here:** type hints turn the function signature into documentation. Reading
> `Callable[[Position, Position], float]` instantly tells you A* wants *a function* (like
> `manhattan_distance`) — not a number — without digging through the body.

<a id="prereq-deque-heapq-inf"></a>
### 8. `collections.deque`, `heapq`, and `float('inf')`

Three tools from the standard library show up across the algorithm weeks. Each is the *right*
tool for a specific job.

**`collections.deque` — a fast double-ended queue (used by BFS, Week 3).**
BFS must take cells in *first-in, first-out* order. A `deque` adds to one end and removes from
the other in O(1). (A plain list's `pop(0)` is O(n), which would make BFS slow.)

```python
from collections import deque
frontier = deque([start])
frontier.append(neighbor)   # add to the back   – O(1)
current = frontier.popleft()  # remove from front – O(1)
```

**`heapq` — a priority queue / min-heap (used by Dijkstra and A*, Weeks 4–5).**
A heap always lets you pop the *smallest* item efficiently (O(log n)). Dijkstra and A* push
`(cost, position)` tuples and always expand the cheapest option next.

```python
import heapq
pq = [(0.0, start)]
heapq.heappush(pq, (new_cost, neighbor))  # add        – O(log n)
cost, current = heapq.heappop(pq)         # pop cheapest – O(log n)
```

**`float('inf')` — positive infinity.**
`float('inf')` is a number larger than every real number. The project uses it as the starting
cost for "not reached yet": any real path cost is smaller, so the *first* path found always
wins the `new_cost < best_so_far` comparison.

```python
# "we haven't found any path to `neighbor` yet, so its best cost is infinity"
if new_cost < cost_so_far.get(neighbor, float('inf')):
    cost_so_far[neighbor] = new_cost
```

> **Why we use this here:** the data structure must match the search order. *FIFO* search →
> `deque`. *Cheapest-first* search → `heapq`. *"No cost known yet"* → `float('inf')` so the
> first real cost always replaces it.

<a id="prereq-tryexcept"></a>
### 9. `try/except` Basics

Some operations can fail at runtime — bad input, a missing file, a division by zero. `try/except`
lets you *attempt* something and *handle* the failure instead of crashing.

```python
try:
    value = int(user_text)        # might fail if user_text isn't a number
except ValueError:
    print("That wasn't a valid number, please try again.")
```

- The code under `try:` runs first.
- If it raises the named exception (`ValueError` here), the `except` block runs.
- If no error occurs, the `except` block is skipped.

> **Why we use this here:** the Week 1 exercise validates user input and catches errors so a
> typo produces a friendly message rather than a stack trace. The Gradio UI (Week 8) uses the
> same idea to keep the app from crashing on invalid coordinates.

## Code Walkthrough: One Cell Through the Whole Vocabulary

Watch how a single cell `(2, 5)` touches almost every concept above:

1. It's a **tuple** named by the `Position` alias (**§1**, **§7**).
2. `Grid.is_obstacle((2, 5))` checks membership in a **set** in O(1) (**§2**).
3. `Grid.is_valid` unpacks it with `row, col = position` (**§1**) inside a **method** that
   reads `self.height` (**§3**).
4. A search may wrap it in a **dataclass** `Node` whose **dunder** `__lt__` lets a **heapq**
   priority queue order it (**§4**, **§5**, **§8**).
5. Its cost starts at `float('inf')` until a path reaches it (**§8**).
6. The chosen `MovementMode` **enum** decides whether `(2, 5)` has 4 or 8 neighbors (**§6**).

If you can follow those six steps, you can read every algorithm file in this repository.

## Common Mistakes

1. **Skipping `pip install -e .`** → `ModuleNotFoundError: No module named 'pathfinding_lab'`.
   See [Week 1](week_01_python_project_setup.md). The `src/` layout needs the editable install.
2. **Using a list where a set belongs.** `pos in big_list` is O(n); `pos in big_set` is O(1).
   For "is it present?" checks inside a loop, reach for a set or dict.
3. **Writing `= []` as a dataclass default.** Mutable defaults are shared between instances —
   use `field(default_factory=list)` (as `SearchResult` does).
4. **Confusing a tuple with a list.** `(row, col)` can be a dict key or set member; `[row, col]`
   cannot, because lists are mutable and unhashable.
5. **Passing a string where an enum is expected.** Use `MovementMode.EIGHT_DIRECTIONAL`, not
   `"8-directional"`.
6. **Reading `Callable[...]` as a value.** It means the function wants *another function*
   (a heuristic), not a number.

## Mini Project Task

### Task: Read the Code, Don't Run It (Yet)

Open `src/pathfinding_lab/core/` and, **using only this page as your decoder**, answer in your
own words:

1. In `types.py`, what is `Position`, and what does `MovementMode` replace? (**§1**, **§6**)
2. In `node.py`, name three dataclass fields and their default values, then explain what
   `__lt__` compares and why a priority queue needs it. (**§4**, **§5**)
3. In `result.py`, why does `path` use `field(default_factory=list)` instead of `= []`? (**§4**)
4. In `grid.py`, find one example of tuple unpacking and one O(1) set lookup. (**§1**, **§2**)
5. In `algorithms/astar.py`, read the signature: what *type* of thing is `heuristic`? (**§7**)

### Success Criteria
- ✅ You can point to a real line for tuples, sets, classes, dataclasses, dunders, enums, and
  type hints.
- ✅ You can explain "O(1)" and "O(n)" in one sentence each.
- ✅ When a later week uses one of these symbols, you know which section to revisit.

## Reflection Questions

1. Why is a **tuple** (not a list) the right type for a grid coordinate?
2. In one sentence, what does **O(1)** mean, and why does it matter inside a search loop?
3. What problem would you hit if `Node` defined `__eq__` but not `__hash__`?
4. Why does a priority queue need `__lt__` (or orderable tuples) to work at all?
5. How do you *read* `Callable[[Position, Position], float]` out loud?
6. When would you choose a `deque` over a `heapq`, and vice versa?

## Additional Resources

- [Python Tutorial: Data Structures (lists, tuples, sets, dicts)](https://docs.python.org/3/tutorial/datastructures.html)
- [`dataclasses` — Data Classes](https://docs.python.org/3/library/dataclasses.html)
- [`enum` — Support for enumerations](https://docs.python.org/3/library/enum.html)
- [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) and [`heapq`](https://docs.python.org/3/library/heapq.html)
- [Big-O in plain English (Stack Overflow)](https://stackoverflow.com/questions/487258/what-is-a-plain-english-explanation-of-big-o-notation)
- [Python type hints — `typing`](https://docs.python.org/3/library/typing.html)

---

**➡️ [Continue to Week 1: Python Project Setup](week_01_python_project_setup.md)** | **🧭 [End-to-End Pipeline](END_TO_END_PIPELINE.md)** | **📖 [Back to Roadmap](../LEARNING_ROADMAP.md)**
