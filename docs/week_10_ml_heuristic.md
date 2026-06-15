# Week 10: Machine Learning Heuristics

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 9](week_09_benchmarking.md)** | **📝 [Week 10 Exercises](../exercises/week_10.md)** | **✅ [Week 10 Solutions](../solutions/week_10_solutions.md)** | **🔬 [Notebook](../notebooks/06_learned_heuristics.ipynb)** | **➡️ [Next: Week 11](week_11_polishing.md)**

---

## 📋 Before You Start

> **🧭 Pipeline:** This week adds **box 10** to the [end-to-end pipeline](END_TO_END_PIPELINE.md) — an optional learned (ML) heuristic experiment.

**What you should already know** (each links to where to learn or revisit it):

- scikit-learn basics (fit / predict, `train_test_split`, `RandomForestRegressor`) — [scikit-learn getting started](https://scikit-learn.org/stable/getting_started.html).
- A* + heuristics (what the model replaces) — [Week 5](week_05_astar.md).
- A heuristic is a *function* (`Callable`) — [Week 0 §7](week_00_python_prerequisites.md#prereq-typehints).
- What `pickle` does (save/load a model) — [pickle docs](https://docs.python.org/3/library/pickle.html).

---

## Learning Goals

By the end of this week, you will understand:
- The concept of learned heuristics and how they differ from classical heuristics
- How to train ML models to predict distance-to-goal using scikit-learn
- Feature engineering for pathfinding problems
- How to evaluate heuristic quality and admissibility
- The trade-offs between learned and classical heuristics
- Practical limitations and when to use ML heuristics

## Theory

### What are Learned Heuristics?

A **learned heuristic** is a heuristic function that uses machine learning to predict the distance from a given position to the goal, rather than using a mathematical formula like Manhattan or Euclidean distance.

**Classical Heuristic (Manhattan Distance)**:
```python
def manhattan_distance(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
```

**Learned Heuristic**:
```python
def learned_heuristic(current, goal):
    features = extract_features(grid, current, goal)
    return ml_model.predict(features)  # Trained ML model
```

### Why Use Machine Learning for Heuristics?

#### Potential Benefits

1. **Adapt to Specific Environments**: A learned heuristic can capture patterns specific to your domain. For example:
   - Games with recurring obstacle patterns
   - Navigation in environments with known structure (buildings, road networks)
   - Scenarios where obstacles affect travel time in complex ways

2. **Learn Complex Patterns**: ML models can learn non-linear relationships between position, obstacles, and actual distance.

3. **Environment-Specific Optimization**: Train on your specific grid layouts to get heuristics tailored to your use case.

#### Important Reality Check

**In practice, learned heuristics are often NOT better than classical heuristics for general grid pathfinding.** Manhattan and Euclidean distances are:
- Simple and computationally cheap
- Provably admissible (guarantee optimal paths)
- Work well across all grid types
- Require no training data or preprocessing

**This week is educational** - understanding why ML heuristics have limitations is as valuable as understanding how they work.

### Trade-offs and Limitations

#### Computational Cost

**Classical heuristic evaluation**:
```python
# Manhattan: ~10 nanoseconds
h = abs(x1 - x2) + abs(y1 - y2)
```

**Learned heuristic evaluation**:
```python
# Random Forest: ~100-1000 microseconds
features = extract_features(grid, current, goal)  # Feature computation
h = model.predict(features)[0]  # Model inference
```

Learned heuristics can be **100-1000x slower per evaluation**. Since A* evaluates the heuristic for every explored node, this overhead adds up quickly.

#### Admissibility Concerns

**Admissible heuristic**: Never overestimates the true cost to goal (h(n) ≤ h*(n))
- Guarantees A* finds optimal paths
- Classical heuristics (Manhattan, Euclidean) are provably admissible

**ML heuristics are generally NOT admissible**:
- May overestimate or underestimate
- If overestimating → A* may not find optimal path
- If underestimating → A* explores more nodes (slower)

**Why ML heuristics are inadmissible**:
1. Training data is finite - model generalizes imperfectly
2. Model may not have seen similar configurations
3. Regression models try to predict average, not lower bound
4. No mathematical guarantee of underestimation

#### Training Data Requirements

To train a good learned heuristic, you need:
1. **Thousands of training samples**: Each sample requires running Dijkstra to get true distances
2. **Diverse grid configurations**: Must cover the range of scenarios you'll encounter
3. **Quality labels**: True optimal distances from Dijkstra
4. **Representative features**: Features that capture relevant information

This upfront cost can be significant.

### When ML Heuristics Are Useful

ML heuristics make sense when:

1. **Highly Structured, Recurring Environments**
   - Same map used repeatedly (e.g., game levels)
   - Patterns that ML can exploit
   - Worth the upfront training cost

2. **Complex Cost Functions**
   - When simple geometric distance doesn't capture reality
   - Terrain with varying movement costs
   - Real-world navigation with traffic patterns

3. **Domain-Specific Knowledge**
   - Can encode expert knowledge as features
   - Historical data about typical paths
   - Environment has learnable regularities

4. **Research and Experimentation**
   - Exploring new approaches
   - Combining with other ML techniques
   - Academic investigation

### When Classical Heuristics Are Better

Stick with Manhattan/Euclidean when:

1. **General Purpose Pathfinding**: No specific recurring patterns
2. **Optimality Required**: Must guarantee shortest path
3. **Real-Time Performance Critical**: Can't afford ML overhead
4. **Unknown Environments**: No training data available
5. **Simple Grid Worlds**: Classical heuristics already work well

## Code Walkthrough

Our ML module consists of four key files that implement the complete pipeline from data generation to using a trained model.

### 1. Dataset Generation (`src/pathfinding_lab/ml/dataset.py`)

This module generates training data by creating random grids and computing true distances.

#### `generate_training_data()` Function

```python
def generate_training_data(
    num_samples: int = 1000,
    grid_size: int = 20,
    obstacle_density: float = 0.2,
    random_seed: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate training data for learned heuristic.

    Returns: (features, labels) where labels are true optimal distances
    """
```

**How it works**:
1. Create a random grid with obstacles
2. Pick random start and goal positions
3. Run **Dijkstra** to compute the true optimal distance (ground truth)
4. Extract features from the grid state
5. Store (features, true_distance) as a training sample
6. Repeat for `num_samples` samples

**Key point**: We use Dijkstra (not A*) because we need the TRUE optimal distance as the label. Dijkstra always finds the optimal path since it doesn't use a heuristic.

**Why this works**: The ML model learns to predict what Dijkstra would compute, but faster (we hope).

#### Feature Extraction

```python
def extract_features(grid: Grid, start: Position, goal: Position) -> List[float]:
    """
    Extract features from a grid state.

    Features:
    - Manhattan distance
    - Euclidean distance
    - Straight-line obstacle count
    - Local obstacle density around start
    - Local obstacle density around goal
    """
```

**Feature Engineering** is crucial for ML performance. Our features capture:

1. **Manhattan Distance**: Basic lower bound on distance
2. **Euclidean Distance**: Geometric straight-line distance
3. **Obstacles in Line**: Count of obstacles between start and goal
   - If many obstacles block the path, actual distance > Manhattan
4. **Local Obstacle Density (Start)**: How "cluttered" the area around start is
   - High density might mean difficult to leave start area
5. **Local Obstacle Density (Goal)**: How cluttered the area around goal is
   - High density might mean difficult to reach goal

**Why these features?**
- Manhattan and Euclidean provide a baseline estimate
- Obstacle counts help model learn when path must detour
- Local density captures whether areas are open or maze-like

**What features could be added?**
- Distance to nearest obstacle
- Grid size (if training on multiple sizes)
- Number of free neighbors at start/goal
- More sophisticated obstacle patterns
- Historical path statistics

#### Helper Functions

```python
def count_obstacles_in_line(grid: Grid, start: Position, goal: Position) -> int:
    """Count obstacles in approximate straight line between start and goal."""
    # Uses linear interpolation to sample points along line
```

```python
def get_local_obstacle_density(grid: Grid, position: Position, radius: int = 2) -> float:
    """Calculate obstacle density in local neighborhood."""
    # Counts obstacles in radius-2 square around position
    # Returns percentage: 0.0 (open) to 1.0 (all obstacles)
```

### 2. Feature Module (`src/pathfinding_lab/ml/features.py`)

Simple wrapper that formats features for the model:

```python
def extract_features(grid: Grid, current: Position, goal: Position) -> np.ndarray:
    """Extract features for heuristic prediction."""
    features = base_extract_features(grid, current, goal)
    return np.array(features).reshape(1, -1)  # Shape (1, 5) for single prediction
```

**Key point**: Scikit-learn models expect 2D arrays even for single predictions, hence `reshape(1, -1)`.

### 3. Training Module (`src/pathfinding_lab/ml/train_heuristic.py`)

This module trains a Random Forest model to predict distances.

```python
def train_heuristic_model(
    num_samples: int = 1000,
    grid_size: int = 20,
    model_path: str = "learned_heuristic_model.pkl"
) -> RandomForestRegressor:
    """Train a Random Forest model to predict distance to goal."""
```

**Training Pipeline**:

1. **Generate Data**: Create 1000+ samples using `generate_training_data()`
   ```python
   X, y = generate_training_data(num_samples, grid_size)
   # X: (num_samples, 5) feature matrix
   # y: (num_samples,) true distances
   ```

2. **Split Data**: 80% training, 20% testing
   ```python
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42
   )
   ```

3. **Train Random Forest**:
   ```python
   model = RandomForestRegressor(
       n_estimators=100,    # 100 decision trees
       random_state=42,
       max_depth=20         # Limit depth to prevent overfitting
   )
   model.fit(X_train, y_train)
   ```

4. **Evaluate**:
   ```python
   train_score = model.score(X_train, y_train)  # R² score
   test_score = model.score(X_test, y_test)
   ```

5. **Save Model**: Pickle the trained model to disk
   ```python
   with open(model_path, 'wb') as f:
       pickle.dump(model, f)
   ```

**Why Random Forest?**
- Handles non-linear relationships well
- Robust to overfitting with proper parameters
- Fast training on small datasets
- Works well with mixed feature types
- No need for feature scaling

**Alternative models to try**:
- Gradient Boosting (XGBoost, LightGBM)
- Neural Networks (for very large datasets)
- K-Nearest Neighbors (simple baseline)

**Evaluation metric (R² Score)**:
- R² = 1.0: Perfect predictions
- R² = 0.0: Model no better than predicting mean
- R² < 0.0: Model worse than predicting mean

Typical results:
- Train R²: 0.85-0.95 (good fit)
- Test R²: 0.75-0.85 (decent generalization)

### 4. Learned Heuristic Module (`src/pathfinding_lab/ml/learned_heuristic.py`)

This module loads the trained model and uses it as a heuristic function.

#### `LearnedHeuristic` Class

```python
class LearnedHeuristic:
    """
    Learned heuristic using a trained ML model.

    WARNING: Learned heuristics are NOT guaranteed to be admissible,
    which means A* with this heuristic may not find optimal paths.
    """

    def __init__(self, model_path: str = "learned_heuristic_model.pkl"):
        """Load the trained model."""
        self.model = None
        self.model_path = model_path
        self._load_model()

    def __call__(self, grid: Grid, current: Position, goal: Position) -> float:
        """Predict distance from current to goal."""
        if self.model is None:
            # Fallback to Manhattan if model not found
            r1, c1 = current
            r2, c2 = goal
            return abs(r1 - r2) + abs(c1 - c2)

        features = extract_features(grid, current, goal)
        prediction = self.model.predict(features)[0]

        # Ensure non-negative (distances can't be negative)
        return max(0.0, prediction)
```

**Key design decisions**:

1. **Fallback to Manhattan**: If model file doesn't exist, use classical heuristic
   - Prevents crashes when model isn't trained yet
   - Provides reasonable default behavior

2. **Non-negative Constraint**: Clamp predictions to [0, ∞)
   - Distances can't be negative
   - Models might occasionally predict negative values

3. **Warning in Docstring**: Explicitly warn about inadmissibility
   - Users should know this may not give optimal paths
   - Educational transparency

#### Creating Heuristic Functions

```python
def create_learned_heuristic_function(
    grid: Grid,
    model_path: str = "learned_heuristic_model.pkl"
):
    """
    Create a learned heuristic function for use with pathfinding algorithms.

    Returns:
        Heuristic function that takes (current, goal) and returns distance estimate
    """
    learned_h = LearnedHeuristic(model_path)

    def heuristic(current: Position, goal: Position) -> float:
        return learned_h(grid, current, goal)

    return heuristic
```

**Why this wrapper?**
- Our A* implementation expects `heuristic(current, goal)` signature
- The learned heuristic needs access to the grid for feature extraction
- This closure captures the grid in the function scope

**Usage example**:
```python
# Train the model (once)
from pathfinding_lab.ml.train_heuristic import train_heuristic_model
train_heuristic_model(num_samples=1000)

# Use the learned heuristic with A*
from pathfinding_lab.ml.learned_heuristic import create_learned_heuristic_function
learned_h = create_learned_heuristic_function(grid)

result = astar(grid, start, goal, learned_h)
```

## Common Mistakes

### 1. Not Checking Admissibility

**Problem**: Using learned heuristics without verifying they don't overestimate, leading to suboptimal paths.

```python
# BAD: Blindly using ML heuristic
learned_h = create_learned_heuristic_function(grid)
result = astar(grid, start, goal, learned_h)
# Might not find optimal path!
```

**Solution**: Compare path costs with Dijkstra to verify optimality.

```python
# GOOD: Verify optimality
learned_result = astar(grid, start, goal, learned_h)
optimal_result = dijkstra(grid, start, goal)

if learned_result.path_cost > optimal_result.path_cost:
    print(f"WARNING: ML heuristic found suboptimal path!")
    print(f"ML path cost: {learned_result.path_cost}")
    print(f"Optimal cost: {optimal_result.path_cost}")
```

**Best practice**: Always provide a classical heuristic fallback or use ML heuristic only when optimality isn't critical.

### 2. Training on Too Few or Non-Diverse Samples

**Problem**: Model only sees limited scenarios and fails to generalize.

```python
# BAD: Only 50 samples, all similar grids
X, y = generate_training_data(num_samples=50, grid_size=10, obstacle_density=0.2)
# Model won't generalize to different grid sizes or densities
```

**Solution**: Train on diverse scenarios.

```python
# GOOD: Generate diverse training data
all_features = []
all_labels = []

for obstacle_density in [0.1, 0.2, 0.3, 0.4]:
    for grid_size in [10, 15, 20, 25]:
        X, y = generate_training_data(
            num_samples=250,
            grid_size=grid_size,
            obstacle_density=obstacle_density
        )
        all_features.append(X)
        all_labels.append(y)

X = np.vstack(all_features)
y = np.concatenate(all_labels)
# Now have 4000 diverse samples
```

### 3. Not Normalizing Features

**Problem**: Features have different scales, which can hurt model performance.

```python
# Example features (not normalized):
# Manhattan: 28
# Euclidean: 19.8
# Obstacles in line: 3
# Start density: 0.15
# Goal density: 0.23
```

Some ML models (especially neural networks) perform poorly when features have vastly different ranges.

**Solution**: Normalize features during training.

```python
from sklearn.preprocessing import StandardScaler

# During training
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model.fit(X_train_scaled, y_train)

# Save both model and scaler
with open('model.pkl', 'wb') as f:
    pickle.dump((model, scaler), f)

# During inference
with open('model.pkl', 'rb') as f:
    model, scaler = pickle.load(f)

features_scaled = scaler.transform(features)
prediction = model.predict(features_scaled)
```

**Note**: Random Forests are relatively insensitive to feature scaling, but it's good practice for other models.

### 4. Using ML Heuristic Without Classical Fallback

**Problem**: If model file is missing or corrupted, application crashes.

```python
# BAD: No fallback
model = pickle.load(open('model.pkl', 'rb'))  # Crashes if file missing
prediction = model.predict(features)
```

**Solution**: Always provide a fallback.

```python
# GOOD: Graceful degradation
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Warning: ML model not found, using Manhattan distance")
    model = None

def heuristic(current, goal):
    if model is not None:
        return ml_predict(model, current, goal)
    else:
        # Fallback to Manhattan
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
```

### 5. Assuming ML is Always Better

**Problem**: Expecting ML heuristic to outperform Manhattan distance in all scenarios.

**Reality**:
- Manhattan distance: ~10 nanoseconds per evaluation
- ML heuristic: ~100-1000 microseconds per evaluation
- ML is 10,000x slower per evaluation!

Even if ML heuristic reduces nodes visited by 20%, the overhead usually makes it slower overall.

**Solution**: Benchmark thoroughly and be realistic about trade-offs.

```python
# Compare both approaches
manhattan_result = astar(grid, start, goal, manhattan_distance)
learned_result = astar(grid, start, goal, learned_heuristic)

print(f"Manhattan: {manhattan_result.runtime_ms:.2f}ms, "
      f"{manhattan_result.nodes_visited} nodes")
print(f"Learned: {learned_result.runtime_ms:.2f}ms, "
      f"{learned_result.nodes_visited} nodes")
```

Typical result: Manhattan is faster despite visiting more nodes.

### 6. Not Saving Feature Extraction Logic

**Problem**: Model is trained with certain features but inference code uses different features.

**Solution**: Version control your feature extraction and keep training/inference consistent.

```python
# Save feature extractor version with model
metadata = {
    'model': model,
    'feature_version': '1.0',
    'feature_names': ['manhattan', 'euclidean', 'obstacles', 'start_density', 'goal_density'],
    'training_date': '2024-01-15'
}

with open('model_v1.pkl', 'wb') as f:
    pickle.dump(metadata, f)
```

## Mini Project Task

### This Week's Challenge: Train and Evaluate a Learned Heuristic

Train a learned heuristic model and rigorously compare it against classical heuristics to understand when ML approaches are beneficial.

### Steps

1. **Generate Training Data**
   ```python
   from pathfinding_lab.ml.dataset import generate_training_data

   X, y = generate_training_data(
       num_samples=1000,
       grid_size=20,
       obstacle_density=0.2
   )
   print(f"Generated {len(X)} training samples")
   ```

2. **Train the Model**
   ```python
   from pathfinding_lab.ml.train_heuristic import train_heuristic_model

   model = train_heuristic_model(
       num_samples=1000,
       grid_size=20,
       model_path='my_heuristic_model.pkl'
   )
   ```

3. **Create Test Grids**
   - Create 10 test grids with varying obstacle densities (10%, 20%, 30%)
   - Use different random seeds than training data
   - Mix of open grids and maze-like grids

4. **Compare Heuristics**
   For each test grid:
   - Run A* with Manhattan distance
   - Run A* with learned heuristic
   - Run Dijkstra (ground truth)

   Compare:
   - Path costs (is ML path optimal?)
   - Runtime (is ML faster?)
   - Nodes visited (does ML explore less?)

5. **Analyze Results**
   - Calculate percentage of times ML heuristic finds optimal path
   - Compare average runtime: ML vs Manhattan
   - Compare average nodes visited
   - Identify scenarios where ML is better/worse

6. **Create Visualizations**
   - Bar chart: Nodes visited (ML vs Manhattan)
   - Bar chart: Runtime comparison
   - Scatter plot: ML prediction vs true distance
   - Table: Path optimality results

### Success Criteria

- ✅ Model trained on 1000+ samples with R² > 0.7 on test set
- ✅ Tested on at least 10 diverse test grids
- ✅ Complete comparison table with all metrics
- ✅ Analysis of when ML heuristic finds optimal vs suboptimal paths
- ✅ Runtime comparison showing ML overhead
- ✅ Visualization of prediction accuracy
- ✅ Written summary of findings with recommendations

### Example Analysis Template

```
ML Heuristic Evaluation Report
=============================

Training Results:
- Training samples: 1000
- Training R² score: 0.89
- Test R² score: 0.78

Test Grid Performance (10 grids, 20x20, 20% obstacles):
-------------------------------------------------------
                 Manhattan    Learned     Dijkstra
Avg Runtime:     1.23ms       4.67ms      2.45ms
Avg Nodes:       187          165         321
Optimal Paths:   10/10        8/10        10/10

Findings:
1. Learned heuristic reduced nodes visited by 12%
2. However, runtime was 3.8x slower due to ML overhead
3. Found suboptimal paths on 2/10 grids (inadmissible)
4. Overestimation cases: highly complex obstacle patterns

Conclusion:
For these grid sizes, Manhattan distance is superior due to:
- Guaranteed optimality
- Much faster evaluation
- Simpler implementation

ML heuristic might be useful for:
- Very large grids (>100x100) where node reduction matters more
- Specific recurring environments with learnable patterns
- When optimality isn't critical
```

## Reflection Questions

1. **Why might ML heuristics be inadmissible?**
   - Consider: How regression models make predictions, training data limitations, generalization errors, no mathematical guarantee of underestimation

2. **What features would you add to improve predictions?**
   - Consider: Distance to nearest obstacle, connectivity measures, grid topology, historical path data, domain-specific patterns

3. **When would you use ML heuristics in practice?**
   - Consider: Trade-offs between accuracy and speed, training cost vs benefit, optimality requirements, environment characteristics

4. **Why is feature engineering so important for learned heuristics?**
   - Consider: Model can only learn from provided features, garbage in = garbage out, need features that correlate with true distance

5. **How would you make a learned heuristic more likely to be admissible?**
   - Consider: Training objective (minimize maximum error vs mean error), post-processing (scale down predictions), ensemble with Manhattan

6. **What happens if you train on 20x20 grids but test on 50x50 grids?**
   - Consider: Generalization to different scales, feature meaning at different sizes, absolute vs relative features

7. **Could you combine classical and learned heuristics?**
   - Consider: Using max(manhattan, learned * 0.9) to stay admissible, weighted average, learning correction factors

8. **Why is Random Forest a good choice for this problem?**
   - Consider: Non-linear relationships, robustness, no feature scaling needed, interpretability, performance on small datasets

## Additional Resources

### Machine Learning for Heuristics

- [Learning Heuristics for A* (Stanford)](https://ai.stanford.edu/~latombe/cs326/2007/class19.pdf) - Academic perspective on learned heuristics
- [Neural A*: Learning Heuristics](https://arxiv.org/abs/2009.07476) - Recent research on neural network heuristics
- [Combining Learning and Search](https://www.ijcai.org/Proceedings/2018/0773.pdf) - Hybrid approaches

### Scikit-learn Resources

- [Scikit-learn Documentation](https://scikit-learn.org/stable/) - Official documentation
- [Random Forest Regressor Guide](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
- [Feature Engineering Guide](https://machinelearningmastery.com/discover-feature-engineering-how-to-engineer-features-and-how-to-get-good-at-it/)

### Pathfinding + ML

- [Machine Learning for Pathfinding](https://www.gamedeveloper.com/programming/machine-learning-for-pathfinding) - Practical game dev perspective
- [DeepMind on Learning to Search](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go) - How AlphaZero learns search heuristics
- [Heuristic Learning for Path Planning](https://www.aaai.org/Papers/AAAI/2006/AAAI06-170.pdf) - Classic AAAI paper

### Related Topics

- [Introduction to Random Forests](https://www.youtube.com/watch?v=J4Wdy0Wc_xQ) - StatQuest video explanation
- [Regression Metrics Explained](https://towardsdatascience.com/metrics-to-evaluate-your-machine-learning-algorithm-f10ba6e38234)
- [Admissible Heuristics Theory](https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) - Deep dive on heuristic properties

## Next Week Preview

Congratulations! You've completed the core pathfinding curriculum. You now understand:
- Classical search algorithms (BFS, DFS, Dijkstra, A*)
- Heuristic design (Manhattan, Euclidean, learned)
- Performance analysis and benchmarking
- Advanced topics (bidirectional search, ML heuristics)

**Possible next steps**:

1. **Jump Point Search**: Advanced grid optimization
2. **Dynamic Pathfinding**: Handling moving obstacles
3. **Multi-Agent Pathfinding**: Coordinating multiple agents
4. **3D Pathfinding**: Extending to three dimensions
5. **Real-World Applications**: Implementing in games or robotics

Keep exploring and building!

---

**End of Week 10**

---

## End-to-End Pipeline Connection

The learned heuristic is an optional experiment layered on top of the classical pipeline:

```text
generate training grids → compute target distances → extract features → train model → load model → estimate heuristic → run A*
```

This week is not replacing A*. It is teaching how ML can supply one piece of A*: the estimate of remaining cost.

### End-to-End ML Pipeline

A learned heuristic needs more steps than a hand-written distance formula:

1. Generate many grid examples.
2. Compute reliable target values, often using an optimal algorithm.
3. Extract numeric features from positions, goals, and grid context.
4. Train a model to predict distance or cost-to-go.
5. Save the trained model.
6. Load the model in the application.
7. Wrap prediction in the same callable shape as other heuristics.
8. Pass that callable into A*.
9. Compare quality and speed against classical heuristics.

Every step must be correct before the learned heuristic is meaningful.

### Feature Engineering Mindset

Features are the information the model can see. If the model only sees start and goal coordinates, it may learn geometric distance but not obstacle difficulty. If it sees local obstacle density or map structure, it may learn more useful estimates but inference can become slower.

The product trade-off is:

```text
more features → potentially smarter estimates → more computation and more complexity
```

### UI Integration Pattern

A UI can expose the learned heuristic as an advanced option. The callback should handle missing model files gracefully and fall back to a classical heuristic with a clear message.

Learners should understand whether they are using Manhattan, Octile, Weighted, or a model-based estimate.

### Evaluating a Learned Heuristic

Compare it with classical heuristics using Week 9 metrics:

- Does it reduce visited nodes?
- Does it preserve path quality?
- Is prediction overhead larger than the search savings?
- Does it generalize to maps different from the training set?

### Week 10 Build Checkpoint

You are ready for Week 11 when you can explain the difference between training-time work, saved model artifacts, and runtime heuristic inference inside A*.
