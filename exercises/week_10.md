# Week 10: Exercises

**📖 [Back to Learning Roadmap](../LEARNING_ROADMAP.md)** | **⬅️ [Previous: Week 9 Exercises](week_09.md)** | **📚 [Week 10 Documentation](../docs/week_10_ml_heuristic.md)** | **✅ [Week 10 Solutions](../solutions/week_10_solutions.md)** | **➡️ [Next: Week 11 Exercises](week_11.md)**

---

**🔑 Concepts/links you'll need:** scikit-learn (`train_test_split`, `RandomForestRegressor`) — [getting started](https://scikit-learn.org/stable/getting_started.html); a heuristic is a `Callable` ([Week 0 §7](../docs/week_00_python_prerequisites.md#prereq-typehints)); `pickle` to save/load models — [docs](https://docs.python.org/3/library/pickle.html).

## Warm-up Exercise (Trivial)

### Task: See One Training Example (Features → True Distance)

Machine learning trains on `(features → answer)` pairs. Print *one* such pair so the rest of the
week isn't abstract: the **features** of a cell and the **true** distance Dijkstra computes for it
(the label the model will try to predict).

```python
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.ml.dataset import extract_features
from pathfinding_lab.algorithms.dijkstra import dijkstra

grid = Grid(15, 15, obstacle_density=0.2, random_seed=42)
start, goal = (0, 0), (14, 14)
grid.generate_obstacles(start, goal)

features = extract_features(grid, start, goal)
true_distance = dijkstra(grid, start, goal).path_cost

print("features (model input):", features)
print("true distance (label to predict):", round(true_distance, 2))
```

**You're done when** you can name what each feature roughly measures and explain why the true
distance is the "answer" the model is trying to learn. *(Unsure what *feature*, *training set*, or
*R²* mean? Re-read the primer at the top of [Week 10 docs](../docs/week_10_ml_heuristic.md).)*

---

## Exercise 1: Generate Training Data (Beginner)

**Goal**: Create a dataset of pathfinding problems with ground truth distances for training machine learning models.

**Task**: Write a script that:
1. Generates 500 random grids of varying sizes (15x15 to 25x25)
2. Uses varying obstacle densities (10% to 30%)
3. Selects random start and goal positions for each grid
4. Runs BFS to compute true shortest path distances
5. Extracts features from each problem (Manhattan distance, Euclidean distance, obstacle count, etc.)
6. Saves all data to a CSV file with features and labels

**Requirements**:
- Generate exactly 500 training examples
- Include grids of different sizes: 15x15, 20x20, and 25x25
- Use obstacle densities: 0.1, 0.15, 0.2, 0.25, and 0.3
- Extract at least 6 features per example
- Only include examples where a path exists
- Save to `training_data.csv` with proper column headers

**Starter Code**:

```python
import numpy as np
import pandas as pd
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs

def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def euclidean_distance(pos1, pos2):
    """Calculate Euclidean distance between two positions."""
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def extract_features(grid, start, goal):
    """
    Extract features from a pathfinding problem.

    Args:
        grid: The Grid object
        start: Start position (x, y)
        goal: Goal position (x, y)

    Returns:
        Dictionary of features
    """
    # TODO: Calculate Manhattan distance
    manhattan_dist = 0

    # TODO: Calculate Euclidean distance
    euclidean_dist = 0.0

    # TODO: Count obstacles in grid
    obstacle_count = 0

    # TODO: Calculate obstacle density
    total_cells = grid.width * grid.height
    obstacle_density = 0.0

    # TODO: Count obstacles in a straight line from start to goal
    line_obstacles = 0

    # TODO: Calculate distance to nearest obstacle from start
    min_dist_to_obstacle = float('inf')

    return {
        'manhattan_distance': manhattan_dist,
        'euclidean_distance': euclidean_dist,
        'obstacle_count': obstacle_count,
        'obstacle_density': obstacle_density,
        'line_obstacles': line_obstacles,
        'min_obstacle_distance': min_dist_to_obstacle,
    }

def generate_training_data(num_examples=500):
    """
    Generate training data for ML heuristic.

    Args:
        num_examples: Number of training examples to generate

    Returns:
        DataFrame with features and true distances
    """
    print(f"Generating {num_examples} training examples...")

    # Grid sizes and obstacle densities to sample from
    grid_sizes = [15, 20, 25]
    obstacle_densities = [0.1, 0.15, 0.2, 0.25, 0.3]

    data = []
    examples_generated = 0

    while examples_generated < num_examples:
        # TODO: Randomly select grid size and obstacle density
        size = np.random.choice(grid_sizes)
        density = np.random.choice(obstacle_densities)

        # TODO: Create grid
        grid = None

        # TODO: Select random start and goal positions
        start = (0, 0)
        goal = (size - 1, size - 1)

        # TODO: Generate obstacles

        # TODO: Run BFS to get true distance
        result = None

        # TODO: Check if path was found
        if True:  # Replace with actual check
            # TODO: Extract features
            features = extract_features(grid, start, goal)

            # TODO: Add true distance as label
            features['true_distance'] = 0  # Replace with actual distance
            features['grid_size'] = size

            # TODO: Append to data list
            data.append(features)
            examples_generated += 1

            if examples_generated % 50 == 0:
                print(f"  Generated {examples_generated}/{num_examples} examples...")

    # TODO: Create DataFrame
    df = pd.DataFrame(data)

    # TODO: Save to CSV
    df.to_csv('training_data.csv', index=False)
    print(f"\nTraining data saved to training_data.csv")
    print(f"Dataset shape: {df.shape}")
    print(f"\nFeature statistics:")
    print(df.describe())

    return df

if __name__ == "__main__":
    df = generate_training_data(500)
    print("\nFirst 5 examples:")
    print(df.head())
```

**Expected Output**:
```
Generating 500 training examples...
  Generated 50/500 examples...
  Generated 100/500 examples...
  ...
  Generated 500/500 examples...

Training data saved to training_data.csv
Dataset shape: (500, 8)

Feature statistics:
       manhattan_distance  euclidean_distance  obstacle_count  ...
count              500.00              500.00          500.00  ...
mean                26.34               20.17           82.45  ...
std                  6.21                5.03           34.28  ...
min                 14.00               12.73           15.00  ...
max                 48.00               36.84          187.00  ...

First 5 examples:
   manhattan_distance  euclidean_distance  obstacle_count  obstacle_density  ...  true_distance  grid_size
0                  28               19.80              45              0.20  ...             34         15
1                  38               26.87              80              0.20  ...             46         20
2                  24               16.97              75              0.30  ...             32         15
3                  48               33.94             150              0.24  ...             58         25
4                  34               24.04              96              0.24  ...             41         20
```

**Testing**:
1. Verify that exactly 500 examples are generated
2. Check that `training_data.csv` is created and contains 8 columns
3. Confirm all true_distance values are greater than or equal to Manhattan distance
4. Verify obstacle counts match grid obstacle densities
5. Load the CSV file and ensure all data is properly formatted

---

## Exercise 2: Train a Simple Model (Intermediate)

**Goal**: Train a Random Forest regressor to predict shortest path distances and evaluate its performance.

**Task**: Build a machine learning pipeline that:
1. Loads the training data from Exercise 1
2. Splits data into train (80%) and test (20%) sets
3. Trains a Random Forest regressor on the training set
4. Evaluates the model on the test set
5. Compares predictions against true distances
6. Calculates evaluation metrics (MAE, RMSE, R²)
7. Visualizes prediction accuracy
8. Saves the trained model to disk

**Requirements**:
- Use `sklearn.ensemble.RandomForestRegressor`
- Split data with `random_state=42` for reproducibility
- Train with at least 100 estimators
- Calculate Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R² score
- Create a scatter plot of predicted vs true distances
- Save the model using `joblib`
- Report feature importance scores

**Starter Code**:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

def load_and_prepare_data(filepath='training_data.csv'):
    """
    Load training data and prepare features/labels.

    Args:
        filepath: Path to training data CSV

    Returns:
        X: Feature matrix
        y: Target vector (true distances)
    """
    # TODO: Load CSV
    df = pd.read_csv(filepath)

    # TODO: Select feature columns (exclude true_distance and grid_size)
    feature_cols = [
        'manhattan_distance',
        'euclidean_distance',
        'obstacle_count',
        'obstacle_density',
        'line_obstacles',
        'min_obstacle_distance',
    ]

    # TODO: Extract features and labels
    X = None
    y = None

    print(f"Loaded {len(df)} examples")
    print(f"Features: {feature_cols}")

    return X, y, feature_cols

def train_model(X_train, y_train, n_estimators=100):
    """
    Train a Random Forest regressor.

    Args:
        X_train: Training features
        y_train: Training labels
        n_estimators: Number of trees in the forest

    Returns:
        Trained model
    """
    print(f"\nTraining Random Forest with {n_estimators} estimators...")

    # TODO: Create Random Forest regressor
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=42,
        n_jobs=-1,  # Use all CPU cores
    )

    # TODO: Train model

    print("Training complete!")
    return model

def evaluate_model(model, X_test, y_test, feature_names):
    """
    Evaluate model performance on test set.

    Args:
        model: Trained model
        X_test: Test features
        y_test: True test labels
        feature_names: Names of features

    Returns:
        Dictionary of metrics
    """
    print("\nEvaluating model...")

    # TODO: Make predictions
    y_pred = None

    # TODO: Calculate metrics
    mae = 0.0
    rmse = 0.0
    r2 = 0.0

    metrics = {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
    }

    # TODO: Print results
    print(f"\nTest Set Performance:")
    print(f"  Mean Absolute Error:  {mae:.2f}")
    print(f"  Root Mean Squared Error: {rmse:.2f}")
    print(f"  R² Score: {r2:.4f}")

    # TODO: Calculate and display feature importance
    feature_importance = model.feature_importances_
    print(f"\nFeature Importance:")
    for name, importance in zip(feature_names, feature_importance):
        print(f"  {name:25s}: {importance:.4f}")

    return metrics, y_pred

def plot_predictions(y_test, y_pred, metrics):
    """
    Create visualization of predictions vs true values.

    Args:
        y_test: True test labels
        y_pred: Predicted labels
        metrics: Dictionary of evaluation metrics
    """
    plt.figure(figsize=(10, 6))

    # TODO: Create scatter plot
    plt.scatter(y_test, y_pred, alpha=0.5, edgecolors='k', linewidth=0.5)

    # TODO: Plot perfect prediction line (y=x)
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')

    # TODO: Add labels and title
    plt.xlabel('True Distance', fontsize=12)
    plt.ylabel('Predicted Distance', fontsize=12)
    plt.title(f'ML Heuristic: Predicted vs True Distances\nMAE: {metrics["mae"]:.2f}, RMSE: {metrics["rmse"]:.2f}, R²: {metrics["r2"]:.4f}', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)

    # TODO: Save figure
    plt.savefig('prediction_accuracy.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved to prediction_accuracy.png")
    plt.close()

def check_admissibility(y_test, y_pred):
    """
    Check if predictions are admissible (don't overestimate).

    Args:
        y_test: True distances
        y_pred: Predicted distances
    """
    # TODO: Count how many predictions overestimate
    overestimates = np.sum(y_pred > y_test)
    percentage = (overestimates / len(y_test)) * 100

    print(f"\nAdmissibility Check:")
    print(f"  Overestimates: {overestimates}/{len(y_test)} ({percentage:.1f}%)")

    if percentage > 10:
        print(f"  WARNING: Model overestimates in {percentage:.1f}% of cases!")
        print(f"  This heuristic may not be admissible for A*.")
    else:
        print(f"  Model is relatively admissible (overestimates in <10% of cases)")

def main():
    """Main training pipeline."""
    # TODO: Load data
    X, y, feature_names = load_and_prepare_data('training_data.csv')

    # TODO: Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training set: {len(X_train)} examples")
    print(f"Test set: {len(X_test)} examples")

    # TODO: Train model
    model = train_model(X_train, y_train, n_estimators=100)

    # TODO: Evaluate model
    metrics, y_pred = evaluate_model(model, X_test, y_test, feature_names)

    # TODO: Plot results
    plot_predictions(y_test, y_pred, metrics)

    # TODO: Check admissibility
    check_admissibility(y_test, y_pred)

    # TODO: Save model
    model_filename = 'heuristic_model.pkl'
    joblib.dump(model, model_filename)
    print(f"\nModel saved to {model_filename}")

if __name__ == "__main__":
    main()
```

**Expected Output**:
```
Loaded 500 examples
Features: ['manhattan_distance', 'euclidean_distance', 'obstacle_count', 'obstacle_density', 'line_obstacles', 'min_obstacle_distance']
Training set: 400 examples
Test set: 100 examples

Training Random Forest with 100 estimators...
Training complete!

Evaluating model...

Test Set Performance:
  Mean Absolute Error:  2.34
  Root Mean Squared Error: 3.12
  R² Score: 0.9156

Feature Importance:
  manhattan_distance       : 0.4521
  euclidean_distance       : 0.2834
  obstacle_count           : 0.0923
  obstacle_density         : 0.0812
  line_obstacles           : 0.0634
  min_obstacle_distance    : 0.0276

Admissibility Check:
  Overestimates: 8/100 (8.0%)
  Model is relatively admissible (overestimates in <10% of cases)

Plot saved to prediction_accuracy.png
Model saved to heuristic_model.pkl
```

**Testing**:
1. Verify that the model trains without errors
2. Check that R² score is above 0.85 (good fit)
3. Confirm MAE is reasonable (within 3-4 units)
4. Verify prediction plot shows points clustered around the diagonal
5. Check that the model file `heuristic_model.pkl` is created
6. Reload the saved model and verify it can make predictions

---

## Exercise 3: A* with Learned Heuristic (Advanced)

**Goal**: Integrate the learned ML heuristic into A* search and compare its performance against traditional heuristics.

**Task**: Create a comprehensive comparison that:
1. Implements an A* variant that uses the trained ML model as a heuristic
2. Tests three versions of A*: with Manhattan distance, Euclidean distance, and ML heuristic
3. Evaluates on 10 new test grids (not in training data)
4. Compares runtime, nodes visited, and path optimality
5. Checks if the ML heuristic maintains admissibility in practice
6. Creates visualizations comparing all three approaches
7. Generates a detailed performance report

**Requirements**:
- Load the trained model from Exercise 2
- Create 10 new test grids with varied characteristics
- Test all three heuristic types on each grid
- Record runtime, nodes visited, path length, and success rate
- Calculate speedup and node reduction percentages
- Create comparison plots for each metric
- Export results to CSV
- Handle cases where ML heuristic may not be admissible

**Starter Code**:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.astar import astar
from pathfinding_lab.heuristics.manhattan import manhattan_distance
from pathfinding_lab.heuristics.euclidean import euclidean_distance

class MLHeuristic:
    """ML-based heuristic for A* search."""

    def __init__(self, model_path='heuristic_model.pkl'):
        """
        Initialize ML heuristic.

        Args:
            model_path: Path to trained model file
        """
        # TODO: Load trained model
        self.model = joblib.load(model_path)
        print(f"Loaded ML heuristic from {model_path}")

    def __call__(self, current, goal, grid=None):
        """
        Compute ML-based heuristic estimate.

        Args:
            current: Current position (x, y)
            goal: Goal position (x, y)
            grid: Grid object (optional, needed for obstacle features)

        Returns:
            Estimated distance to goal
        """
        # TODO: Extract features for this position
        features = self._extract_features(current, goal, grid)

        # TODO: Make prediction
        # Note: Model expects 2D array
        prediction = 0.0

        return max(0.0, prediction)  # Ensure non-negative

    def _extract_features(self, current, goal, grid):
        """Extract features for ML model."""
        # TODO: Calculate Manhattan distance
        manhattan_dist = abs(current[0] - goal[0]) + abs(current[1] - goal[1])

        # TODO: Calculate Euclidean distance
        euclidean_dist = np.sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2)

        # TODO: Extract grid-based features
        if grid is not None:
            obstacle_count = 0  # Count total obstacles
            obstacle_density = 0.0
            line_obstacles = 0  # Obstacles in straight line to goal
            min_obstacle_distance = float('inf')
        else:
            # Use default values if grid not provided
            obstacle_count = 0
            obstacle_density = 0.0
            line_obstacles = 0
            min_obstacle_distance = 0.0

        # TODO: Return feature array matching training data format
        return np.array([[
            manhattan_dist,
            euclidean_dist,
            obstacle_count,
            obstacle_density,
            line_obstacles,
            min_obstacle_distance,
        ]])

def create_test_grid(size, obstacle_density, seed):
    """
    Create a test grid with specified parameters.

    Args:
        size: Grid size (width and height)
        obstacle_density: Density of obstacles (0.0 to 1.0)
        seed: Random seed for reproducibility

    Returns:
        grid, start, goal
    """
    np.random.seed(seed)

    # TODO: Create grid
    grid = Grid(width=size, height=size, obstacle_density=obstacle_density)

    # TODO: Define start and goal
    start = (0, 0)
    goal = (size - 1, size - 1)

    # TODO: Generate obstacles
    grid.generate_obstacles(start, goal)

    return grid, start, goal

def run_comparison(grid, start, goal, ml_heuristic):
    """
    Run A* with three different heuristics and compare.

    Args:
        grid: Grid to search
        start: Start position
        goal: Goal position
        ml_heuristic: ML heuristic instance

    Returns:
        Dictionary of results for each heuristic
    """
    results = {}

    # Define heuristics to test
    heuristics = [
        ('Manhattan', manhattan_distance),
        ('Euclidean', euclidean_distance),
        ('ML Heuristic', ml_heuristic),
    ]

    for name, heuristic in heuristics:
        try:
            # TODO: Run A* with this heuristic
            if name == 'ML Heuristic':
                # ML heuristic needs grid for feature extraction
                result = None  # TODO: Implement
            else:
                result = astar(grid, start, goal, heuristic)

            # TODO: Store results
            if result.success:
                results[name] = {
                    'runtime_ms': result.runtime_ms,
                    'nodes_visited': result.nodes_visited,
                    'path_length': result.path_length,
                    'success': True,
                }
            else:
                results[name] = {'success': False}

        except Exception as e:
            print(f"  {name} failed: {e}")
            results[name] = {'success': False}

    return results

def run_full_benchmark():
    """Run comprehensive benchmark on test grids."""
    print("="*70)
    print("A* with ML Heuristic - Comprehensive Benchmark")
    print("="*70)

    # TODO: Load ML heuristic
    ml_heuristic = MLHeuristic('heuristic_model.pkl')

    # Define test scenarios
    test_scenarios = [
        # (size, obstacle_density, seed)
        (20, 0.15, 100),
        (20, 0.20, 101),
        (20, 0.25, 102),
        (25, 0.15, 103),
        (25, 0.20, 104),
        (25, 0.25, 105),
        (30, 0.15, 106),
        (30, 0.20, 107),
        (30, 0.25, 108),
        (30, 0.30, 109),
    ]

    all_results = []

    for i, (size, density, seed) in enumerate(test_scenarios, 1):
        print(f"\nTest {i}/10: Grid {size}x{size}, {density:.0%} obstacles")

        # TODO: Create test grid
        grid, start, goal = create_test_grid(size, density, seed)

        # TODO: Run comparison
        results = run_comparison(grid, start, goal, ml_heuristic)

        # TODO: Print results for this test
        print(f"  Results:")
        for heuristic_name, metrics in results.items():
            if metrics['success']:
                print(f"    {heuristic_name:15s}: {metrics['runtime_ms']:6.2f} ms, "
                      f"{metrics['nodes_visited']:4d} nodes, "
                      f"path length {metrics['path_length']}")
            else:
                print(f"    {heuristic_name:15s}: Failed")

        # TODO: Store results
        for heuristic_name, metrics in results.items():
            if metrics['success']:
                all_results.append({
                    'test_id': i,
                    'grid_size': size,
                    'obstacle_density': density,
                    'heuristic': heuristic_name,
                    'runtime_ms': metrics['runtime_ms'],
                    'nodes_visited': metrics['nodes_visited'],
                    'path_length': metrics['path_length'],
                })

    # TODO: Create DataFrame
    df = pd.DataFrame(all_results)

    # TODO: Calculate summary statistics
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)

    summary = df.groupby('heuristic').agg({
        'runtime_ms': ['mean', 'std'],
        'nodes_visited': ['mean', 'std'],
        'path_length': ['mean', 'std'],
    }).round(2)

    print(summary)

    # TODO: Calculate relative performance
    print("\n" + "="*70)
    print("RELATIVE PERFORMANCE (vs Manhattan)")
    print("="*70)

    manhattan_avg = df[df['heuristic'] == 'Manhattan']['runtime_ms'].mean()
    manhattan_nodes = df[df['heuristic'] == 'Manhattan']['nodes_visited'].mean()

    for heuristic in ['Euclidean', 'ML Heuristic']:
        heuristic_data = df[df['heuristic'] == heuristic]
        avg_runtime = heuristic_data['runtime_ms'].mean()
        avg_nodes = heuristic_data['nodes_visited'].mean()

        speedup = manhattan_avg / avg_runtime
        node_reduction = (1 - avg_nodes / manhattan_nodes) * 100

        print(f"\n{heuristic}:")
        print(f"  Speedup: {speedup:.2f}x")
        print(f"  Node reduction: {node_reduction:.1f}%")

    # TODO: Check path optimality
    print("\n" + "="*70)
    print("PATH OPTIMALITY")
    print("="*70)

    for test_id in df['test_id'].unique():
        test_data = df[df['test_id'] == test_id]
        path_lengths = test_data.groupby('heuristic')['path_length'].first()

        if len(path_lengths) == 3:  # All heuristics succeeded
            all_equal = len(path_lengths.unique()) == 1
            if not all_equal:
                print(f"Test {test_id}: Path lengths differ! {path_lengths.to_dict()}")

    # TODO: Save results
    df.to_csv('ml_heuristic_comparison.csv', index=False)
    print("\nDetailed results saved to ml_heuristic_comparison.csv")

    # TODO: Create visualizations
    create_comparison_plots(df)

    return df

def create_comparison_plots(df):
    """Create comparison plots for all metrics."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    heuristics = ['Manhattan', 'Euclidean', 'ML Heuristic']
    colors = ['#3498db', '#e74c3c', '#2ecc71']

    # TODO: Plot 1 - Average Runtime
    avg_runtimes = [df[df['heuristic'] == h]['runtime_ms'].mean() for h in heuristics]
    axes[0].bar(heuristics, avg_runtimes, color=colors)
    axes[0].set_ylabel('Average Runtime (ms)')
    axes[0].set_title('Runtime Comparison')
    axes[0].tick_params(axis='x', rotation=15)

    # TODO: Plot 2 - Average Nodes Visited
    avg_nodes = [df[df['heuristic'] == h]['nodes_visited'].mean() for h in heuristics]
    axes[1].bar(heuristics, avg_nodes, color=colors)
    axes[1].set_ylabel('Average Nodes Visited')
    axes[1].set_title('Nodes Visited Comparison')
    axes[1].tick_params(axis='x', rotation=15)

    # TODO: Plot 3 - Average Path Length
    avg_paths = [df[df['heuristic'] == h]['path_length'].mean() for h in heuristics]
    axes[2].bar(heuristics, avg_paths, color=colors)
    axes[2].set_ylabel('Average Path Length')
    axes[2].set_title('Path Length Comparison')
    axes[2].tick_params(axis='x', rotation=15)

    plt.suptitle('A* Performance: ML Heuristic vs Traditional Heuristics', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('ml_heuristic_comparison.png', dpi=300, bbox_inches='tight')
    print("Comparison plots saved to ml_heuristic_comparison.png")
    plt.close()

if __name__ == "__main__":
    df = run_full_benchmark()
```

**Expected Output**:
```
======================================================================
A* with ML Heuristic - Comprehensive Benchmark
======================================================================
Loaded ML heuristic from heuristic_model.pkl

Test 1/10: Grid 20x20, 15% obstacles
  Results:
    Manhattan      :   1.23 ms,   42 nodes, path length 28
    Euclidean      :   1.18 ms,   39 nodes, path length 28
    ML Heuristic   :   0.94 ms,   31 nodes, path length 28

[... results for tests 2-10 ...]

======================================================================
SUMMARY STATISTICS
======================================================================
                runtime_ms      nodes_visited      path_length
                      mean  std          mean  std        mean  std
heuristic
Euclidean             1.34 0.21         44.30 8.12       32.40 4.23
ML Heuristic          1.12 0.18         36.70 7.45       32.50 4.19
Manhattan             1.45 0.23         48.20 8.89       32.40 4.23

======================================================================
RELATIVE PERFORMANCE (vs Manhattan)
======================================================================

Euclidean:
  Speedup: 1.08x
  Node reduction: 8.1%

ML Heuristic:
  Speedup: 1.29x
  Node reduction: 23.9%

======================================================================
PATH OPTIMALITY
======================================================================

Detailed results saved to ml_heuristic_comparison.csv
Comparison plots saved to ml_heuristic_comparison.png
```

**Testing**:
1. Verify ML heuristic loads correctly from saved model
2. Check that all 10 test scenarios complete successfully
3. Confirm ML heuristic visits fewer nodes than Manhattan distance
4. Verify path lengths are equal or very similar across all heuristics
5. Check that visualizations are generated correctly
6. Try with different test grid configurations

---

## Exercise 4: Debugging Challenge - Flawed ML Heuristic

**Goal**: Fix multiple critical bugs in an ML heuristic implementation that make it unreliable and non-admissible.

**Background**: A team implemented an ML-based heuristic for A*, but their code has several serious issues. The model trains successfully but produces poor results and doesn't maintain admissibility. Your task is to identify and fix all the bugs.

**Given Code** (with bugs):

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs

# Bug 1: Not normalizing features - features have very different scales
def extract_features(grid, start, goal):
    """Extract features without normalization."""
    manhattan = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    euclidean = np.sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2)

    # Obstacle count is in range [0, 1000+]
    obstacle_count = sum(sum(row) for row in grid.grid)

    # Density is in range [0, 1]
    density = obstacle_count / (grid.width * grid.height)

    return [manhattan, euclidean, obstacle_count, density]

# Bug 2: Wrong feature extraction - using different features in training vs prediction
def generate_training_data():
    """Generate training data."""
    data = []

    for _ in range(500):
        size = np.random.choice([15, 20, 25])
        density = np.random.choice([0.1, 0.2, 0.3])

        grid = Grid(width=size, height=size, obstacle_density=density)
        start = (0, 0)
        goal = (size - 1, size - 1)
        grid.generate_obstacles(start, goal)

        result = bfs(grid, start, goal)

        if result.success:
            # Using DIFFERENT feature extraction than in prediction!
            features = [
                abs(start[0] - goal[0]) + abs(start[1] - goal[1]),  # Manhattan
                np.sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2),  # Euclidean
                density,  # Just density, not obstacle_count!
                size,  # Grid size, not in predict function!
            ]
            features.append(result.path_length)
            data.append(features)

    df = pd.DataFrame(data, columns=['manhattan', 'euclidean', 'density', 'size', 'distance'])
    return df

# Bug 3: Data leakage - using test data in training
def train_model():
    """Train model with data leakage."""
    df = generate_training_data()

    # Split data
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    # Bug: Using ENTIRE dataset for training, not just train_df!
    X = df[['manhattan', 'euclidean', 'density', 'size']].values
    y = df['distance'].values

    model = RandomForestRegressor(n_estimators=10, random_state=42)  # Too few estimators
    model.fit(X, y)

    # Evaluate on test set (but trained on test data too!)
    X_test = test_df[['manhattan', 'euclidean', 'density', 'size']].values
    y_test = test_df['distance'].values

    predictions = model.predict(X_test)
    mae = np.mean(np.abs(predictions - y_test))

    print(f"Test MAE: {mae:.2f}")  # Will look artificially good!

    return model

# Bug 4: Not checking for admissibility - predictions can overestimate
class MLHeuristic:
    """Buggy ML Heuristic."""

    def __init__(self, model):
        self.model = model

    def __call__(self, current, goal, grid=None):
        """Compute heuristic - no admissibility guarantee!"""
        # Using wrong features (different from training)
        features = extract_features(grid, current, goal)

        # Bug: Features mismatch - training expects 4 features [manhattan, euclidean, density, size]
        # but extract_features returns [manhattan, euclidean, obstacle_count, density]

        prediction = self.model.predict([features])[0]

        # Bug: Not ensuring admissibility!
        # Should cap prediction at Manhattan distance at minimum
        return prediction  # Can overestimate!

# Bug 5: Incorrect train/test split - testing on same grid characteristics
def create_test_grids():
    """Create test grids that are too similar to training data."""
    test_grids = []

    # Using exact same sizes and densities as training data!
    for size in [15, 20, 25]:
        for density in [0.1, 0.2, 0.3]:
            grid = Grid(width=size, height=size, obstacle_density=density)
            start = (0, 0)
            goal = (size - 1, size - 1)
            grid.generate_obstacles(start, goal)
            test_grids.append((grid, start, goal))

    return test_grids

# Bug 6: Not handling edge cases
def predict_distance(model, grid, start, goal):
    """Predict distance without error handling."""
    heuristic = MLHeuristic(model)

    # Bug: What if start == goal?
    # Bug: What if grid is None?
    # Bug: What if features extraction fails?

    prediction = heuristic(start, goal, grid)
    return prediction

# Bug 7: Overfitting - using default hyperparameters
def train_better_model():
    """Train with default parameters - will overfit!"""
    df = generate_training_data()

    X_train, X_test, y_train, y_test = train_test_split(
        df[['manhattan', 'euclidean', 'density', 'size']].values,
        df['distance'].values,
        test_size=0.2,
        random_state=42
    )

    # Using default parameters - no cross-validation, no regularization
    model = RandomForestRegressor(
        n_estimators=1000,  # Too many trees
        max_depth=None,  # No depth limit - will overfit!
        min_samples_split=2,  # Default - allows overfitting
        random_state=42
    )

    model.fit(X_train, y_train)
    return model

# Main execution
if __name__ == "__main__":
    print("Training buggy ML heuristic...")
    model = train_model()

    print("\nTesting on new grids...")
    test_grids = create_test_grids()

    for i, (grid, start, goal) in enumerate(test_grids[:3]):
        try:
            prediction = predict_distance(model, grid, start, goal)
            print(f"Test {i+1}: Predicted distance = {prediction:.1f}")
        except Exception as e:
            print(f"Test {i+1}: Error - {e}")
```

**Your Task**:
1. Identify all bugs in the code above (at least 7 major issues)
2. Explain why each bug is problematic for ML heuristics
3. Fix all bugs and create a corrected version
4. Add proper validation and admissibility checks
5. Test the fixed version to ensure it works correctly

**List of Bugs to Find**:
- [ ] Bug 1: Features not normalized (different scales cause poor training)
- [ ] Bug 2: Feature mismatch between training and prediction
- [ ] Bug 3: Data leakage (training on test data)
- [ ] Bug 4: No admissibility guarantee (can overestimate distances)
- [ ] Bug 5: Test data too similar to training data
- [ ] Bug 6: No error handling for edge cases
- [ ] Bug 7: Overfitting due to poor hyperparameters and no cross-validation

**Expected Behavior**:
After fixing all bugs, the code should:
- Normalize features consistently during training and prediction
- Use identical feature extraction in both training and prediction
- Properly split data without leakage
- Ensure predictions never exceed true distances (admissibility)
- Test on diverse grids different from training data
- Handle edge cases gracefully (start == goal, empty grids, etc.)
- Use proper cross-validation and regularization to prevent overfitting

**Hints**:
- Use `sklearn.preprocessing.StandardScaler` for feature normalization
- Always use the same feature extraction function for training and prediction
- Only train on `X_train`, never on the full dataset
- Cap predictions at Manhattan distance to ensure admissibility
- Create test grids with different sizes and densities than training
- Add try-except blocks and validate inputs
- Use cross-validation and tune hyperparameters (max_depth, min_samples_split)
- Consider using `max_samples` to prevent overfitting on small datasets

---

## Bonus Challenge: Learned Heuristic with Neural Networks

**Goal**: Replace the Random Forest with a neural network and compare performance.

**Task**:
1. Implement a neural network heuristic using PyTorch or TensorFlow
2. Use at least 2 hidden layers with appropriate activation functions
3. Add dropout for regularization
4. Train with early stopping to prevent overfitting
5. Compare neural network vs Random Forest on test grids
6. Analyze which features each model considers most important
7. Experiment with different architectures and report findings

**Requirements**:
- Use the same training data from Exercise 1
- Implement proper train/validation/test split
- Use learning rate scheduling
- Add batch normalization
- Compare training time, prediction time, and accuracy
- Create learning curves showing training/validation loss
- Ensure admissibility through post-processing

This challenge requires knowledge of deep learning frameworks!

---

## Submission Checklist

For each exercise, ensure:
- [ ] Code runs without errors
- [ ] Training data is generated correctly with valid examples
- [ ] Model trains successfully and achieves reasonable accuracy (R² > 0.85)
- [ ] ML heuristic integrates properly with A* search
- [ ] Performance comparisons show meaningful results
- [ ] All bugs are identified and fixed in Exercise 4
- [ ] Admissibility is checked and enforced
- [ ] Results are exported to CSV files
- [ ] Visualizations are created and saved
- [ ] Code includes proper error handling
- [ ] Features are normalized consistently
- [ ] No data leakage between train and test sets
- [ ] Code includes helpful comments explaining key steps

---

---

**✅ [See Solutions](../solutions/week_10_solutions.md)** | **📚 [Back to Week 10 Docs](../docs/week_10_ml_heuristic.md)** | **➡️ [Next: Week 11 Exercises](week_11.md)** | **📖 [Learning Roadmap](../LEARNING_ROADMAP.md)**
