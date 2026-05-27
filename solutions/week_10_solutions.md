# Week 10 Solutions: ML-Based Heuristics

## Exercise 1 Solution: Generate Training Data (Beginner)

### Explanation

This solution generates a comprehensive training dataset for machine learning heuristics by creating diverse pathfinding problems and computing ground truth distances. The key principles are:

1. **Ground Truth Collection**: Using BFS (or Dijkstra) to compute the true optimal distance for each problem. This serves as our training label.
2. **Feature Engineering**: Extracting meaningful features that correlate with actual path distance, including geometric distances, obstacle patterns, and local density.
3. **Diverse Sampling**: Creating grids with varying sizes and obstacle densities ensures the model generalizes well to different scenarios.
4. **Data Quality**: Only including solvable problems (where a path exists) prevents the model from learning nonsensical patterns.
5. **Consistent Format**: Saving to CSV with proper headers makes the data easy to load and use in downstream tasks.

The features we extract include:
- **Manhattan Distance**: Theoretical minimum distance (no obstacles)
- **Euclidean Distance**: Straight-line geometric distance
- **Obstacle Count**: Total obstacles in the grid (indicates overall difficulty)
- **Obstacle Density**: Percentage of cells that are obstacles
- **Line Obstacles**: Obstacles directly between start and goal (indicates detours needed)
- **Min Obstacle Distance**: Distance from start to nearest obstacle (indicates immediate difficulty)

### Code

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

def count_line_obstacles(grid, start, goal):
    """
    Count obstacles in approximate straight line from start to goal.
    Uses linear interpolation to sample points along the line.
    """
    x0, y0 = start
    x1, y1 = goal

    # Number of points to sample along the line
    num_samples = max(abs(x1 - x0), abs(y1 - y0)) + 1

    obstacle_count = 0
    for i in range(num_samples):
        t = i / max(1, num_samples - 1)  # Parameter from 0 to 1

        # Linear interpolation
        x = int(x0 + t * (x1 - x0))
        y = int(y0 + t * (y1 - y0))

        # Check if this point is an obstacle
        if (x, y) in grid.obstacles:
            obstacle_count += 1

    return obstacle_count

def min_distance_to_obstacle(grid, position):
    """Find minimum distance from position to any obstacle."""
    if not grid.obstacles:
        return float('inf')

    min_dist = float('inf')
    for obstacle in grid.obstacles:
        dist = manhattan_distance(position, obstacle)
        min_dist = min(min_dist, dist)

    return min_dist

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
    # Calculate Manhattan distance
    manhattan_dist = manhattan_distance(start, goal)

    # Calculate Euclidean distance
    euclidean_dist = euclidean_distance(start, goal)

    # Count total obstacles in grid
    obstacle_count = len(grid.obstacles)

    # Calculate obstacle density
    total_cells = grid.width * grid.height
    obstacle_density = obstacle_count / total_cells if total_cells > 0 else 0.0

    # Count obstacles in straight line from start to goal
    line_obstacles = count_line_obstacles(grid, start, goal)

    # Calculate distance to nearest obstacle from start
    min_dist_to_obstacle = min_distance_to_obstacle(grid, start)

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
    attempts = 0
    max_attempts = num_examples * 3  # Prevent infinite loops

    while examples_generated < num_examples and attempts < max_attempts:
        attempts += 1

        # Randomly select grid size and obstacle density
        size = np.random.choice(grid_sizes)
        density = np.random.choice(obstacle_densities)

        # Create grid
        grid = Grid(width=size, height=size, obstacle_density=density)

        # Select random start and goal positions
        start = (
            np.random.randint(0, size),
            np.random.randint(0, size)
        )
        goal = (
            np.random.randint(0, size),
            np.random.randint(0, size)
        )

        # Ensure start and goal are different
        if start == goal:
            continue

        # Generate obstacles (avoiding start and goal)
        grid.generate_obstacles(start, goal)

        # Run BFS to get true distance
        result = bfs(grid, start, goal)

        # Only include if path was found
        if result.success:
            # Extract features
            features = extract_features(grid, start, goal)

            # Add true distance as label
            features['true_distance'] = result.path_length
            features['grid_size'] = size

            # Append to data list
            data.append(features)
            examples_generated += 1

            if examples_generated % 50 == 0:
                print(f"  Generated {examples_generated}/{num_examples} examples...")

    if examples_generated < num_examples:
        print(f"Warning: Only generated {examples_generated} examples after {attempts} attempts")

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
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

    # Additional validation checks
    print("\n" + "="*50)
    print("Data Quality Checks")
    print("="*50)

    # Check 1: All true distances should be >= Manhattan distance (admissibility check)
    manhattan_violations = (df['true_distance'] < df['manhattan_distance']).sum()
    print(f"True distance < Manhattan distance: {manhattan_violations} cases (should be 0)")

    # Check 2: No NaN values
    nan_count = df.isnull().sum().sum()
    print(f"NaN values: {nan_count} (should be 0)")

    # Check 3: Feature distributions look reasonable
    print(f"\nFeature ranges:")
    print(f"  Manhattan distance: [{df['manhattan_distance'].min():.0f}, {df['manhattan_distance'].max():.0f}]")
    print(f"  True distance: [{df['true_distance'].min():.0f}, {df['true_distance'].max():.0f}]")
    print(f"  Obstacle density: [{df['obstacle_density'].min():.2f}, {df['obstacle_density'].max():.2f}]")

    # Check 4: Distribution across grid sizes
    print(f"\nGrid size distribution:")
    print(df['grid_size'].value_counts().sort_index())
```

### Key Concepts

- **Ground Truth Collection**: Using BFS ensures we have the true optimal distance as our training label. This is crucial for supervised learning.
- **Feature Engineering**: Good features are the foundation of ML success. Our features capture both geometric properties (Manhattan, Euclidean) and obstacle-related patterns (density, line obstacles).
- **Data Diversity**: Sampling from multiple grid sizes and obstacle densities ensures the model can generalize to different scenarios.
- **Data Quality**: Only including solvable problems prevents the model from learning patterns from impossible situations.
- **Validation**: Checking that true distance >= Manhattan distance verifies data integrity (true distance should never be less than the theoretical minimum).
- **Reproducibility**: While we use randomness, saving the data to CSV allows others to use the exact same dataset.

### Testing Advice

1. **Verify Dataset Size**: Confirm exactly 500 examples are generated (or close to it - some randomness is okay).

2. **Check CSV Structure**:
   ```python
   df = pd.read_csv('training_data.csv')
   print(f"Columns: {list(df.columns)}")
   print(f"Shape: {df.shape}")
   # Should have 8 columns: 6 features + true_distance + grid_size
   ```

3. **Validate Feature Distributions**:
   ```python
   # Manhattan distance should be reasonable for grid sizes (15-25)
   assert df['manhattan_distance'].min() >= 0
   assert df['manhattan_distance'].max() <= 48  # Max for 25x25 grid

   # Obstacle density should match our specified densities
   assert df['obstacle_density'].min() >= 0.05  # Allow some variance
   assert df['obstacle_density'].max() <= 0.35
   ```

4. **Admissibility Check**: The most important validation is that true distance >= Manhattan distance for all examples:
   ```python
   violations = df[df['true_distance'] < df['manhattan_distance']]
   assert len(violations) == 0, f"Found {len(violations)} violations!"
   ```

5. **Check for Missing Data**:
   ```python
   assert df.isnull().sum().sum() == 0, "Found NaN values!"
   ```

6. **Visualize Feature Relationships**:
   ```python
   import matplotlib.pyplot as plt

   plt.scatter(df['manhattan_distance'], df['true_distance'], alpha=0.3)
   plt.plot([0, 50], [0, 50], 'r--', label='Perfect correlation')
   plt.xlabel('Manhattan Distance')
   plt.ylabel('True Distance')
   plt.legend()
   plt.show()
   # True distance should be >= Manhattan (points above red line)
   ```

---

## Exercise 2 Solution: Train a Simple Model (Intermediate)

### Explanation

This solution builds a complete machine learning pipeline for training a Random Forest regressor to predict shortest path distances. The key components are:

1. **Data Loading and Preparation**: Loading the CSV from Exercise 1 and separating features from labels.
2. **Train/Test Split**: 80/20 split ensures we can evaluate generalization performance on unseen data.
3. **Model Selection**: Random Forest is ideal for this problem because it:
   - Handles non-linear relationships between features and distance
   - Doesn't require feature normalization
   - Provides feature importance scores
   - Is relatively fast to train and predict
4. **Evaluation Metrics**:
   - **MAE (Mean Absolute Error)**: Average prediction error in distance units
   - **RMSE (Root Mean Squared Error)**: Penalizes large errors more heavily
   - **R² Score**: How well the model explains variance (1.0 = perfect)
5. **Admissibility Checking**: Crucial for heuristics - we check how often predictions overestimate true distances (which would make A* suboptimal).
6. **Feature Importance**: Understanding which features matter most helps validate our feature engineering.

The solution demonstrates that while ML models can achieve good R² scores (0.85-0.95), they often overestimate distances in 5-15% of cases, making them inadmissible heuristics.

### Code

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
        feature_cols: List of feature column names
    """
    # Load CSV
    df = pd.read_csv(filepath)

    # Select feature columns (exclude true_distance and grid_size)
    feature_cols = [
        'manhattan_distance',
        'euclidean_distance',
        'obstacle_count',
        'obstacle_density',
        'line_obstacles',
        'min_obstacle_distance',
    ]

    # Extract features and labels
    X = df[feature_cols].values
    y = df['true_distance'].values

    print(f"Loaded {len(df)} examples")
    print(f"Features: {feature_cols}")
    print(f"Feature matrix shape: {X.shape}")
    print(f"Label vector shape: {y.shape}")

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

    # Create Random Forest regressor
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=20,           # Limit depth to prevent overfitting
        min_samples_split=5,    # Require at least 5 samples to split
        min_samples_leaf=2,     # Require at least 2 samples in leaf nodes
        random_state=42,
        n_jobs=-1,              # Use all CPU cores
        verbose=0
    )

    # Train model
    model.fit(X_train, y_train)

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
        metrics: Dictionary of metrics
        y_pred: Predictions on test set
    """
    print("\nEvaluating model...")

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
    }

    # Print results
    print(f"\nTest Set Performance:")
    print(f"  Mean Absolute Error:     {mae:.2f} units")
    print(f"  Root Mean Squared Error: {rmse:.2f} units")
    print(f"  R² Score:                {r2:.4f}")

    # Interpretation
    if r2 > 0.90:
        print(f"  → Excellent fit! Model explains {r2*100:.1f}% of variance.")
    elif r2 > 0.80:
        print(f"  → Good fit! Model explains {r2*100:.1f}% of variance.")
    elif r2 > 0.70:
        print(f"  → Decent fit. Model explains {r2*100:.1f}% of variance.")
    else:
        print(f"  → Poor fit. Model only explains {r2*100:.1f}% of variance.")

    # Calculate and display feature importance
    feature_importance = model.feature_importances_
    print(f"\nFeature Importance:")

    # Sort by importance
    importance_pairs = list(zip(feature_names, feature_importance))
    importance_pairs.sort(key=lambda x: x[1], reverse=True)

    for name, importance in importance_pairs:
        bar = '█' * int(importance * 50)
        print(f"  {name:25s}: {importance:.4f} {bar}")

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

    # Create scatter plot
    plt.scatter(y_test, y_pred, alpha=0.5, edgecolors='k', linewidth=0.5)

    # Plot perfect prediction line (y=x)
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')

    # Add labels and title
    plt.xlabel('True Distance', fontsize=12)
    plt.ylabel('Predicted Distance', fontsize=12)
    title = f'ML Heuristic: Predicted vs True Distances\n'
    title += f'MAE: {metrics["mae"]:.2f}, RMSE: {metrics["rmse"]:.2f}, R²: {metrics["r2"]:.4f}'
    plt.title(title, fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Save figure
    plt.savefig('prediction_accuracy.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved to prediction_accuracy.png")
    plt.close()

def check_admissibility(y_test, y_pred):
    """
    Check if predictions are admissible (don't overestimate).

    An admissible heuristic never overestimates the true cost.
    For A* to guarantee optimal paths, h(n) <= h*(n) must hold.

    Args:
        y_test: True distances
        y_pred: Predicted distances
    """
    # Count how many predictions overestimate
    overestimates = np.sum(y_pred > y_test)
    percentage = (overestimates / len(y_test)) * 100

    # Calculate how much we overestimate on average
    overestimate_amounts = y_pred[y_pred > y_test] - y_test[y_pred > y_test]
    avg_overestimate = overestimate_amounts.mean() if len(overestimate_amounts) > 0 else 0
    max_overestimate = overestimate_amounts.max() if len(overestimate_amounts) > 0 else 0

    print(f"\n" + "="*60)
    print(f"Admissibility Check")
    print(f"="*60)
    print(f"Overestimates: {overestimates}/{len(y_test)} ({percentage:.1f}%)")

    if overestimates > 0:
        print(f"Average overestimate: {avg_overestimate:.2f} units")
        print(f"Maximum overestimate: {max_overestimate:.2f} units")

    print()
    if percentage > 10:
        print(f"⚠️  WARNING: Model overestimates in {percentage:.1f}% of cases!")
        print(f"    This heuristic is NOT admissible for A*.")
        print(f"    A* with this heuristic may find suboptimal paths.")
    elif percentage > 0:
        print(f"⚠️  CAUTION: Model overestimates in {percentage:.1f}% of cases.")
        print(f"    While relatively low, this still violates admissibility.")
        print(f"    Use with care if optimality is required.")
    else:
        print(f"✅  EXCELLENT: Model never overestimates!")
        print(f"    This heuristic appears to be admissible.")

    # Also check underestimation statistics
    underestimates = np.sum(y_pred < y_test)
    underestimate_percentage = (underestimates / len(y_test)) * 100
    underestimate_amounts = y_test[y_pred < y_test] - y_pred[y_pred < y_test]
    avg_underestimate = underestimate_amounts.mean() if len(underestimate_amounts) > 0 else 0

    print(f"\nUnderestimates: {underestimates}/{len(y_test)} ({underestimate_percentage:.1f}%)")
    if underestimates > 0:
        print(f"Average underestimate: {avg_underestimate:.2f} units")
        print(f"(Underestimation is OK for admissibility, but reduces A* efficiency)")
    print("="*60)

def main():
    """Main training pipeline."""
    print("="*60)
    print("ML Heuristic Training Pipeline")
    print("="*60)

    # Load data
    X, y, feature_names = load_and_prepare_data('training_data.csv')

    # Split into train and test sets (80/20 split)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"\nData Split:")
    print(f"  Training set: {len(X_train)} examples ({len(X_train)/len(X)*100:.0f}%)")
    print(f"  Test set:     {len(X_test)} examples ({len(X_test)/len(X)*100:.0f}%)")

    # Train model
    model = train_model(X_train, y_train, n_estimators=100)

    # Evaluate on training set (check for overfitting)
    print("\n" + "-"*60)
    print("Training Set Performance:")
    print("-"*60)
    y_train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, y_train_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    print(f"  R² Score: {train_r2:.4f}")
    print(f"  MAE:      {train_mae:.2f}")

    # Evaluate on test set
    print("\n" + "-"*60)
    print("Test Set Performance:")
    print("-"*60)
    metrics, y_pred = evaluate_model(model, X_test, y_test, feature_names)

    # Check for overfitting
    print("\n" + "-"*60)
    print("Overfitting Check:")
    print("-"*60)
    r2_gap = train_r2 - metrics['r2']
    print(f"  Training R²: {train_r2:.4f}")
    print(f"  Test R²:     {metrics['r2']:.4f}")
    print(f"  Gap:         {r2_gap:.4f}")

    if r2_gap < 0.05:
        print(f"  ✅ Minimal overfitting (gap < 0.05)")
    elif r2_gap < 0.10:
        print(f"  ⚠️  Slight overfitting (gap < 0.10)")
    else:
        print(f"  ❌ Significant overfitting (gap >= 0.10)")
        print(f"     Consider: reducing max_depth, increasing min_samples_split")

    # Plot results
    plot_predictions(y_test, y_pred, metrics)

    # Check admissibility
    check_admissibility(y_test, y_pred)

    # Save model
    model_filename = 'heuristic_model.pkl'
    joblib.dump(model, model_filename)
    print(f"\n✅ Model saved to {model_filename}")

    # Save feature names for later use
    feature_metadata = {
        'feature_names': feature_names,
        'feature_count': len(feature_names),
        'model_type': 'RandomForestRegressor',
        'n_estimators': 100,
    }
    joblib.dump(feature_metadata, 'model_metadata.pkl')
    print(f"✅ Metadata saved to model_metadata.pkl")

    # Final summary
    print("\n" + "="*60)
    print("Training Summary")
    print("="*60)
    print(f"✓ Trained on {len(X_train)} examples")
    print(f"✓ Test MAE: {metrics['mae']:.2f} units")
    print(f"✓ Test R²:  {metrics['r2']:.4f}")
    print(f"✓ Model saved successfully")
    print(f"\nNext steps:")
    print(f"  1. Review prediction_accuracy.png")
    print(f"  2. Check admissibility results above")
    print(f"  3. Proceed to Exercise 3 to test with A*")
    print("="*60)

if __name__ == "__main__":
    main()
```

### Key Concepts

- **Supervised Learning**: We learn from labeled data (features → true distance) to make predictions on new data.
- **Train/Test Split**: Essential for evaluating generalization. Never evaluate on training data alone!
- **Overfitting Prevention**: Using `max_depth`, `min_samples_split`, and `min_samples_leaf` prevents the model from memorizing training data.
- **Feature Importance**: Random Forests naturally provide feature importance scores, showing which features contribute most to predictions.
- **Admissibility**: A critical property for A* heuristics. If h(n) > h*(n) (overestimation), A* may not find optimal paths.
- **Evaluation Metrics**:
  - **MAE**: Easy to interpret (average error in distance units)
  - **RMSE**: Penalizes large errors more (useful for detecting outliers)
  - **R²**: Overall model quality (how much variance is explained)

### Testing Advice

1. **Verify Model Training**:
   ```python
   # Model should train without errors
   # Check that R² > 0.80 on test set
   assert metrics['r2'] > 0.80, "Model fit is poor!"
   ```

2. **Check Overfitting**:
   ```python
   # Training R² should not be much higher than test R²
   # Gap > 0.10 indicates overfitting
   assert (train_r2 - test_r2) < 0.10, "Model is overfitting!"
   ```

3. **Validate Predictions**:
   ```python
   # Predictions should be in reasonable range
   assert y_pred.min() >= 0, "Negative predictions!"
   assert y_pred.max() < 100, "Unreasonably large predictions!"
   ```

4. **Test Model Persistence**:
   ```python
   # Load saved model and verify it works
   loaded_model = joblib.load('heuristic_model.pkl')
   test_features = X_test[0:1]
   prediction = loaded_model.predict(test_features)
   assert prediction.shape == (1,), "Model loading failed!"
   ```

5. **Admissibility Reality Check**:
   - Expect 5-15% overestimation rate (typical for regression models)
   - If 0% overestimation, you might be lucky or have very simple data
   - If >20% overestimation, consider:
     - More training data
     - Better features
     - Different model architecture
     - Post-processing to cap predictions

6. **Feature Importance Validation**:
   - Manhattan and Euclidean distance should be top features (40-60% importance)
   - If obstacle features dominate, your grids may be very complex
   - If importance is evenly distributed, features may be redundant

---

## Exercise 3 Solution: A* with Learned Heuristic (Advanced)

### Explanation

This solution integrates the trained ML model into A* search and comprehensively compares it against traditional heuristics. The key insights are:

1. **ML Heuristic Integration**: The `MLHeuristic` class wraps the trained model and extracts features on-the-fly during search.
2. **Performance Overhead**: ML heuristics are typically 100-1000x slower per evaluation than Manhattan distance due to:
   - Feature extraction (counting obstacles, checking neighbors)
   - Model inference (traversing 100 decision trees)
   - Memory overhead
3. **Node Reduction vs Runtime**: While ML heuristics often visit 10-30% fewer nodes, the overhead usually makes them slower overall.
4. **Admissibility in Practice**: Even if the model performs well on test data, real-world A* usage may reveal admissibility violations.
5. **Scenario Dependence**: ML heuristics perform relatively better on:
   - Very large grids (where node reduction matters more)
   - Complex mazes (where geometric heuristics are weak)
   - Recurring environments (where training data is representative)

The solution demonstrates that **for typical grid pathfinding, classical heuristics are superior** due to their speed, simplicity, and guaranteed admissibility. ML heuristics are educational and may be useful in specialized scenarios, but are not a universal improvement.

### Code

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import time
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
        try:
            self.model = joblib.load(model_path)
            print(f"✅ Loaded ML heuristic from {model_path}")
        except FileNotFoundError:
            print(f"❌ Error: Model file '{model_path}' not found!")
            print(f"   Please run Exercise 2 first to train the model.")
            self.model = None

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
        # Fallback to Manhattan if model not loaded
        if self.model is None:
            return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

        # Extract features for this position
        features = self._extract_features(current, goal, grid)

        # Make prediction (model expects 2D array)
        prediction = self.model.predict(features)[0]

        # Ensure non-negative
        return max(0.0, prediction)

    def _extract_features(self, current, goal, grid):
        """Extract features for ML model."""
        # Calculate Manhattan distance
        manhattan_dist = abs(current[0] - goal[0]) + abs(current[1] - goal[1])

        # Calculate Euclidean distance
        euclidean_dist = np.sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2)

        # Extract grid-based features if grid is provided
        if grid is not None:
            # Count total obstacles
            obstacle_count = len(grid.obstacles)

            # Calculate obstacle density
            total_cells = grid.width * grid.height
            obstacle_density = obstacle_count / total_cells if total_cells > 0 else 0.0

            # Count obstacles in approximate line to goal
            line_obstacles = self._count_line_obstacles(grid, current, goal)

            # Find minimum distance to any obstacle from current position
            min_obstacle_distance = self._min_distance_to_obstacle(grid, current)
        else:
            # Use default values if grid not provided
            obstacle_count = 0
            obstacle_density = 0.0
            line_obstacles = 0
            min_obstacle_distance = 0.0

        # Return feature array matching training data format
        return np.array([[
            manhattan_dist,
            euclidean_dist,
            obstacle_count,
            obstacle_density,
            line_obstacles,
            min_obstacle_distance,
        ]])

    def _count_line_obstacles(self, grid, start, goal):
        """Count obstacles in approximate straight line from start to goal."""
        x0, y0 = start
        x1, y1 = goal

        num_samples = max(abs(x1 - x0), abs(y1 - y0)) + 1
        obstacle_count = 0

        for i in range(num_samples):
            t = i / max(1, num_samples - 1)
            x = int(x0 + t * (x1 - x0))
            y = int(y0 + t * (y1 - y0))

            if (x, y) in grid.obstacles:
                obstacle_count += 1

        return obstacle_count

    def _min_distance_to_obstacle(self, grid, position):
        """Find minimum Manhattan distance to any obstacle."""
        if not grid.obstacles:
            return float('inf')

        min_dist = float('inf')
        for obstacle in grid.obstacles:
            dist = abs(position[0] - obstacle[0]) + abs(position[1] - obstacle[1])
            min_dist = min(min_dist, dist)

        return min_dist if min_dist != float('inf') else 0.0

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

    # Create grid
    grid = Grid(width=size, height=size, obstacle_density=obstacle_density)

    # Define start and goal (opposite corners)
    start = (0, 0)
    goal = (size - 1, size - 1)

    # Generate obstacles
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
        ('ML Heuristic', lambda curr, g: ml_heuristic(curr, g, grid)),
    ]

    for name, heuristic in heuristics:
        try:
            # Run A* with this heuristic
            result = astar(grid, start, goal, heuristic)

            # Store results
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
            print(f"  ❌ {name} failed: {e}")
            results[name] = {'success': False}

    return results

def run_full_benchmark():
    """Run comprehensive benchmark on test grids."""
    print("="*70)
    print("A* with ML Heuristic - Comprehensive Benchmark")
    print("="*70)

    # Load ML heuristic
    ml_heuristic = MLHeuristic('heuristic_model.pkl')

    if ml_heuristic.model is None:
        print("\n❌ Cannot proceed without trained model.")
        print("   Please run Exercise 2 first to train heuristic_model.pkl")
        return None

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
        print(f"\nTest {i}/10: Grid {size}x{size}, {density:.0%} obstacles (seed={seed})")

        # Create test grid
        grid, start, goal = create_test_grid(size, density, seed)
        print(f"  Generated {len(grid.obstacles)} obstacles")

        # Run comparison
        results = run_comparison(grid, start, goal, ml_heuristic)

        # Print results for this test
        print(f"  Results:")
        for heuristic_name, metrics in results.items():
            if metrics['success']:
                print(f"    {heuristic_name:15s}: {metrics['runtime_ms']:7.2f} ms, "
                      f"{metrics['nodes_visited']:4d} nodes, "
                      f"path length {metrics['path_length']:2d}")
            else:
                print(f"    {heuristic_name:15s}: ❌ Failed")

        # Store results
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

    # Create DataFrame
    df = pd.DataFrame(all_results)

    # Calculate summary statistics
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)

    summary = df.groupby('heuristic').agg({
        'runtime_ms': ['mean', 'std', 'min', 'max'],
        'nodes_visited': ['mean', 'std', 'min', 'max'],
        'path_length': ['mean', 'std'],
    }).round(2)

    print(summary)

    # Calculate relative performance vs Manhattan
    print("\n" + "="*70)
    print("RELATIVE PERFORMANCE (vs Manhattan)")
    print("="*70)

    manhattan_avg_runtime = df[df['heuristic'] == 'Manhattan']['runtime_ms'].mean()
    manhattan_avg_nodes = df[df['heuristic'] == 'Manhattan']['nodes_visited'].mean()

    for heuristic in ['Euclidean', 'ML Heuristic']:
        heuristic_data = df[df['heuristic'] == heuristic]
        if len(heuristic_data) == 0:
            continue

        avg_runtime = heuristic_data['runtime_ms'].mean()
        avg_nodes = heuristic_data['nodes_visited'].mean()

        speedup = manhattan_avg_runtime / avg_runtime
        node_reduction = (1 - avg_nodes / manhattan_avg_nodes) * 100

        print(f"\n{heuristic}:")
        print(f"  Average runtime:  {avg_runtime:.2f} ms")
        print(f"  Average nodes:    {avg_nodes:.1f}")

        if speedup > 1.0:
            print(f"  Speedup:          {speedup:.2f}x FASTER ✅")
        else:
            print(f"  Speedup:          {1/speedup:.2f}x SLOWER ❌")

        if node_reduction > 0:
            print(f"  Node reduction:   {node_reduction:.1f}% fewer nodes ✅")
        else:
            print(f"  Node reduction:   {-node_reduction:.1f}% more nodes ❌")

    # Check path optimality
    print("\n" + "="*70)
    print("PATH OPTIMALITY")
    print("="*70)

    non_optimal_count = 0
    for test_id in df['test_id'].unique():
        test_data = df[df['test_id'] == test_id]
        path_lengths = test_data.groupby('heuristic')['path_length'].first()

        if len(path_lengths) >= 2:  # At least 2 heuristics succeeded
            min_length = path_lengths.min()
            max_length = path_lengths.max()

            if min_length != max_length:
                non_optimal_count += 1
                print(f"Test {test_id}: ⚠️  Path lengths differ!")
                for h in path_lengths.index:
                    marker = "✅" if path_lengths[h] == min_length else "❌"
                    print(f"  {h:15s}: {path_lengths[h]:2d} {marker}")

    if non_optimal_count == 0:
        print("✅ All heuristics found optimal paths on all test grids!")
    else:
        print(f"\n⚠️  {non_optimal_count} test(s) had suboptimal paths")
        print(f"   This indicates admissibility violations in ML heuristic")

    # Save results
    df.to_csv('ml_heuristic_comparison.csv', index=False)
    print("\n✅ Detailed results saved to ml_heuristic_comparison.csv")

    # Create visualizations
    create_comparison_plots(df)

    # Final insights
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)

    ml_data = df[df['heuristic'] == 'ML Heuristic']
    manhattan_data = df[df['heuristic'] == 'Manhattan']

    if len(ml_data) > 0 and len(manhattan_data) > 0:
        ml_avg_runtime = ml_data['runtime_ms'].mean()
        manhattan_avg_runtime = manhattan_data['runtime_ms'].mean()
        ml_avg_nodes = ml_data['nodes_visited'].mean()
        manhattan_avg_nodes = manhattan_data['nodes_visited'].mean()

        node_reduction_pct = (1 - ml_avg_nodes / manhattan_avg_nodes) * 100
        runtime_overhead = (ml_avg_runtime / manhattan_avg_runtime - 1) * 100

        print(f"\n1. Node Exploration:")
        print(f"   ML heuristic visited {node_reduction_pct:.1f}% fewer nodes")
        if node_reduction_pct > 20:
            print(f"   → Significant improvement in search efficiency!")
        elif node_reduction_pct > 10:
            print(f"   → Moderate improvement in search efficiency")
        else:
            print(f"   → Minimal improvement in search efficiency")

        print(f"\n2. Runtime Performance:")
        print(f"   ML heuristic had {runtime_overhead:.1f}% runtime overhead")
        if runtime_overhead > 50:
            print(f"   → Despite fewer nodes, ML overhead makes it SLOWER overall ❌")
        elif runtime_overhead > 0:
            print(f"   → ML overhead slightly increases runtime ⚠️")
        else:
            print(f"   → ML heuristic is actually faster! ✅")

        print(f"\n3. Practical Recommendation:")
        if runtime_overhead > 50:
            print(f"   For these scenarios, Manhattan distance is CLEARLY SUPERIOR:")
            print(f"   • Simpler implementation")
            print(f"   • Guaranteed admissibility")
            print(f"   • Much faster evaluation")
            print(f"   • No training required")
        elif runtime_overhead > 0:
            print(f"   Manhattan distance is still recommended:")
            print(f"   • Slight runtime advantage")
            print(f"   • Guaranteed admissibility")
            print(f"   • Simpler implementation")
        else:
            print(f"   ML heuristic shows promise for these scenarios!")
            print(f"   However, verify admissibility for production use.")

    print("="*70)

    return df

def create_comparison_plots(df):
    """Create comparison plots for all metrics."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    heuristics = ['Manhattan', 'Euclidean', 'ML Heuristic']
    colors = ['#3498db', '#e74c3c', '#2ecc71']

    # Filter to only heuristics that have data
    heuristics = [h for h in heuristics if h in df['heuristic'].values]
    colors = colors[:len(heuristics)]

    # Plot 1 - Average Runtime
    avg_runtimes = [df[df['heuristic'] == h]['runtime_ms'].mean() for h in heuristics]
    axes[0].bar(heuristics, avg_runtimes, color=colors)
    axes[0].set_ylabel('Average Runtime (ms)', fontsize=11)
    axes[0].set_title('Runtime Comparison', fontsize=12, fontweight='bold')
    axes[0].tick_params(axis='x', rotation=15)
    axes[0].grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, v in enumerate(avg_runtimes):
        axes[0].text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontsize=9)

    # Plot 2 - Average Nodes Visited
    avg_nodes = [df[df['heuristic'] == h]['nodes_visited'].mean() for h in heuristics]
    axes[1].bar(heuristics, avg_nodes, color=colors)
    axes[1].set_ylabel('Average Nodes Visited', fontsize=11)
    axes[1].set_title('Nodes Visited Comparison', fontsize=12, fontweight='bold')
    axes[1].tick_params(axis='x', rotation=15)
    axes[1].grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, v in enumerate(avg_nodes):
        axes[1].text(i, v + 1, f'{v:.0f}', ha='center', va='bottom', fontsize=9)

    # Plot 3 - Average Path Length
    avg_paths = [df[df['heuristic'] == h]['path_length'].mean() for h in heuristics]
    axes[2].bar(heuristics, avg_paths, color=colors)
    axes[2].set_ylabel('Average Path Length', fontsize=11)
    axes[2].set_title('Path Length Comparison', fontsize=12, fontweight='bold')
    axes[2].tick_params(axis='x', rotation=15)
    axes[2].grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, v in enumerate(avg_paths):
        axes[2].text(i, v + 0.2, f'{v:.1f}', ha='center', va='bottom', fontsize=9)

    plt.suptitle('A* Performance: ML Heuristic vs Traditional Heuristics',
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('ml_heuristic_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Comparison plots saved to ml_heuristic_comparison.png")
    plt.close()

if __name__ == "__main__":
    df = run_full_benchmark()

    if df is not None:
        print("\n" + "="*70)
        print("Benchmark complete! Check these files:")
        print("  📊 ml_heuristic_comparison.csv  - Raw data")
        print("  📈 ml_heuristic_comparison.png  - Visualizations")
        print("="*70)
```

### Key Concepts

- **Feature Extraction Overhead**: Extracting features during search (counting obstacles, etc.) adds significant overhead compared to simple distance calculations.
- **Model Inference Cost**: Even Random Forests (relatively fast ML models) require traversing many decision trees, which is much slower than computing Manhattan distance.
- **Node Reduction vs Runtime**: Visiting fewer nodes doesn't guarantee faster runtime if each node evaluation is expensive.
- **Admissibility Testing**: Comparing path lengths across heuristics reveals when ML predictions overestimate true distances.
- **Scenario Dependence**: ML heuristics may perform better on some grid types (large, complex) than others (small, open).
- **Practical Trade-offs**: For production systems, simplicity, reliability, and guaranteed optimality often outweigh marginal performance gains.

### Testing Advice

1. **Verify ML Model Loading**:
   ```python
   ml_h = MLHeuristic('heuristic_model.pkl')
   assert ml_h.model is not None, "Model failed to load!"
   ```

2. **Test Feature Extraction**:
   ```python
   grid, start, goal = create_test_grid(20, 0.2, 42)
   features = ml_h._extract_features(start, goal, grid)
   assert features.shape == (1, 6), "Wrong feature shape!"
   assert not np.isnan(features).any(), "NaN in features!"
   ```

3. **Compare Results Across Heuristics**:
   ```python
   # All heuristics should find paths (maybe different lengths)
   for h_name, result in results.items():
       assert result['success'], f"{h_name} failed!"

   # ML should visit fewer nodes than Manhattan (typically)
   ml_nodes = results['ML Heuristic']['nodes_visited']
   manhattan_nodes = results['Manhattan']['nodes_visited']
   print(f"Node reduction: {(1 - ml_nodes/manhattan_nodes)*100:.1f}%")
   ```

4. **Check Path Optimality**:
   ```python
   # Collect all path lengths for this grid
   lengths = [r['path_length'] for r in results.values() if r['success']]

   # If ML finds longer path, it's inadmissible
   if results['ML Heuristic']['path_length'] > min(lengths):
       print("⚠️  ML heuristic found suboptimal path!")
   ```

5. **Runtime Analysis**:
   ```python
   # Typically expect ML to be 2-5x slower despite fewer nodes
   ml_time = results['ML Heuristic']['runtime_ms']
   manhattan_time = results['Manhattan']['runtime_ms']
   overhead = ml_time / manhattan_time
   print(f"ML overhead: {overhead:.2f}x")
   ```

6. **Test on Different Grid Sizes**:
   - Small grids (10x10): ML overhead dominates, Manhattan usually wins
   - Medium grids (20-30x30): Close race, depends on complexity
   - Large grids (50x50+): ML node reduction may start to matter

---

## Exercise 4 Solution: Debugging Challenge - Flawed ML Heuristic

### Explanation

This exercise tests your understanding of ML best practices by asking you to identify and fix common bugs in ML pipeline code. The bugs span several categories:

1. **Feature Engineering Issues**: Inconsistent features between training and prediction
2. **Data Leakage**: Using test data during training, inflating performance metrics
3. **Admissibility Violations**: Not ensuring predictions don't overestimate distances
4. **Overfitting**: Poor hyperparameter choices and lack of regularization
5. **Error Handling**: Missing validation for edge cases
6. **Feature Scaling**: Not normalizing features with different magnitudes

These bugs are realistic - they mirror mistakes commonly made when applying ML to new domains. Understanding them deepens your intuition about what can go wrong and how to prevent it.

### Bugs Found

#### Bug 1: Feature Mismatch Between Training and Prediction

**Location**: `extract_features()` vs `generate_training_data()`

**Problem**:
- Training uses: `[manhattan, euclidean, density, size]`
- Prediction uses: `[manhattan, euclidean, obstacle_count, density]`

**Why it's problematic**: The model learns relationships between specific features and distance. If you provide different features at prediction time, the model receives out-of-distribution data and makes poor predictions.

**Fix**: Use identical feature extraction in both places:

```python
def extract_features_correct(grid, start, goal):
    """Extract features consistently."""
    manhattan = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    euclidean = np.sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2)

    obstacle_count = len(grid.obstacles)
    density = obstacle_count / (grid.width * grid.height)

    # Return features in SAME order as training
    return [manhattan, euclidean, obstacle_count, density]
```

#### Bug 2: Data Leakage - Training on Test Data

**Location**: `train_model()`

**Problem**:
```python
# WRONG: Using entire dataset for training
X = df[['manhattan', 'euclidean', 'density', 'size']].values
y = df['distance'].values
model.fit(X, y)  # Training on ALL data, including test set!
```

**Why it's problematic**: Model sees test data during training, so test performance metrics are artificially inflated. This gives false confidence in the model's generalization ability.

**Fix**: Only use train split for training:

```python
# CORRECT: Only train on training split
X_train = train_df[['manhattan', 'euclidean', 'obstacle_count', 'density']].values
y_train = train_df['distance'].values
model.fit(X_train, y_train)
```

#### Bug 3: No Admissibility Guarantee

**Location**: `MLHeuristic.__call__()`

**Problem**: Predictions can overestimate true distances, making A* suboptimal.

**Why it's problematic**: If h(n) > h*(n), A* may expand fewer nodes but miss the optimal path entirely.

**Fix**: Cap predictions at Manhattan distance (guaranteed lower bound):

```python
def __call__(self, current, goal, grid=None):
    """Compute heuristic with admissibility guarantee."""
    features = extract_features(grid, current, goal)
    prediction = self.model.predict([features])[0]

    # Cap at Manhattan distance to ensure admissibility
    manhattan = abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    # Return minimum of prediction and Manhattan
    # This guarantees we never overestimate
    return max(0.0, min(prediction, manhattan))
```

#### Bug 4: Not Normalizing Features

**Location**: Feature extraction throughout

**Problem**: Features have vastly different scales:
- Manhattan distance: 5-50
- Obstacle count: 50-500
- Density: 0.0-1.0

**Why it's problematic**: Some models (especially neural networks and regularized models) perform poorly with unscaled features. Even Random Forests can benefit from normalization.

**Fix**: Use StandardScaler:

```python
from sklearn.preprocessing import StandardScaler

# During training
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model.fit(X_train_scaled, y_train)

# Save scaler with model
joblib.dump({'model': model, 'scaler': scaler}, 'model_bundle.pkl')

# During prediction
bundle = joblib.load('model_bundle.pkl')
model = bundle['model']
scaler = bundle['scaler']

features_scaled = scaler.transform([features])
prediction = model.predict(features_scaled)[0]
```

#### Bug 5: Test Data Too Similar to Training Data

**Location**: `create_test_grids()`

**Problem**: Using exact same grid sizes and densities as training data.

**Why it's problematic**: Doesn't test generalization to unseen scenarios. Performance may degrade on different grid characteristics.

**Fix**: Create diverse test grids:

```python
def create_test_grids_correct():
    """Create diverse test grids different from training data."""
    test_grids = []

    # Use different sizes and densities than training
    # Training used: [15, 20, 25] and [0.1, 0.2, 0.3]
    # Testing uses: intermediate values and extremes
    configs = [
        (18, 0.12),  # Intermediate values
        (22, 0.18),
        (27, 0.28),  # Slightly larger
        (20, 0.05),  # Sparse
        (20, 0.35),  # Dense
    ]

    for size, density in configs:
        grid = Grid(width=size, height=size, obstacle_density=density)
        start = (0, 0)
        goal = (size - 1, size - 1)
        grid.generate_obstacles(start, goal)
        test_grids.append((grid, start, goal))

    return test_grids
```

#### Bug 6: No Error Handling for Edge Cases

**Location**: `predict_distance()`

**Problem**: No checks for:
- Start == goal (distance should be 0)
- Grid is None
- Feature extraction failures

**Why it's problematic**: Production code will crash on edge cases.

**Fix**: Add comprehensive error handling:

```python
def predict_distance_correct(model, grid, start, goal):
    """Predict distance with error handling."""
    # Edge case 1: Start equals goal
    if start == goal:
        return 0.0

    # Edge case 2: Grid is None
    if grid is None:
        # Fallback to Manhattan distance
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    # Edge case 3: Model not loaded
    if model is None:
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    try:
        heuristic = MLHeuristic(model)
        prediction = heuristic(start, goal, grid)
        return prediction
    except Exception as e:
        print(f"Warning: Prediction failed ({e}), using Manhattan distance")
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
```

#### Bug 7: Overfitting Due to Poor Hyperparameters

**Location**: `train_better_model()`

**Problem**:
```python
model = RandomForestRegressor(
    n_estimators=1000,  # Too many trees for small dataset
    max_depth=None,     # No depth limit - memorizes training data
    min_samples_split=2 # Default allows overfitting
)
```

**Why it's problematic**: Model memorizes training data instead of learning generalizable patterns. Test performance will be much worse than training performance.

**Fix**: Use proper regularization:

```python
model = RandomForestRegressor(
    n_estimators=100,         # Sufficient trees
    max_depth=20,             # Limit tree depth
    min_samples_split=10,     # Require more samples to split
    min_samples_leaf=5,       # Require more samples in leaves
    max_features='sqrt',      # Limit features per tree
    random_state=42,
    n_jobs=-1
)

# Use cross-validation to tune hyperparameters
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X_train, y_train, cv=5,
                         scoring='neg_mean_absolute_error')
print(f"Cross-validation MAE: {-scores.mean():.2f} ± {scores.std():.2f}")
```

### Corrected Code

Here's the fully corrected version with all bugs fixed:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from pathfinding_lab.core.grid import Grid
from pathfinding_lab.algorithms.bfs import bfs

# ============================================================================
# FIXED: Consistent feature extraction used everywhere
# ============================================================================

def extract_features_fixed(grid, start, goal):
    """
    Extract features consistently for both training and prediction.
    Returns features in a fixed order.
    """
    manhattan = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    euclidean = np.sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2)

    # Use obstacle_count (not density) for consistency
    obstacle_count = len(grid.obstacles)

    # Calculate density
    total_cells = grid.width * grid.height
    density = obstacle_count / total_cells if total_cells > 0 else 0.0

    # Include grid size as feature
    grid_size = grid.width  # Assuming square grid

    # Also include min distance to obstacle
    min_obstacle_dist = float('inf')
    for obstacle in grid.obstacles:
        dist = abs(start[0] - obstacle[0]) + abs(start[1] - obstacle[1])
        min_obstacle_dist = min(min_obstacle_dist, dist)

    if min_obstacle_dist == float('inf'):
        min_obstacle_dist = 0.0

    # Return features in CONSISTENT order
    return [manhattan, euclidean, obstacle_count, density, grid_size, min_obstacle_dist]

# ============================================================================
# FIXED: Generate training data with consistent features
# ============================================================================

def generate_training_data_fixed():
    """Generate training data with proper feature extraction."""
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
            # Use SAME feature extraction function
            features = extract_features_fixed(grid, start, goal)
            features.append(result.path_length)  # Add label
            data.append(features)

    df = pd.DataFrame(data, columns=[
        'manhattan', 'euclidean', 'obstacle_count', 'density',
        'grid_size', 'min_obstacle_dist', 'distance'
    ])
    return df

# ============================================================================
# FIXED: Train model without data leakage, with proper regularization
# ============================================================================

def train_model_fixed():
    """Train model with proper data splitting and regularization."""
    df = generate_training_data_fixed()

    # Split data properly
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    # FIXED: Only use training data for fitting
    feature_cols = ['manhattan', 'euclidean', 'obstacle_count', 'density',
                    'grid_size', 'min_obstacle_dist']

    X_train = train_df[feature_cols].values
    y_train = train_df['distance'].values

    X_test = test_df[feature_cols].values
    y_test = test_df['distance'].values

    # FIXED: Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # FIXED: Use proper regularization parameters
    model = RandomForestRegressor(
        n_estimators=100,        # Reasonable number of trees
        max_depth=20,            # Limit depth
        min_samples_split=10,    # Prevent overfitting
        min_samples_leaf=5,      # Require minimum samples in leaves
        max_features='sqrt',     # Limit features per tree
        random_state=42,
        n_jobs=-1
    )

    # Perform cross-validation
    cv_scores = cross_val_score(
        model, X_train_scaled, y_train,
        cv=5, scoring='neg_mean_absolute_error'
    )
    print(f"Cross-validation MAE: {-cv_scores.mean():.2f} ± {cv_scores.std():.2f}")

    # Train on full training set
    model.fit(X_train_scaled, y_train)

    # Evaluate on test set (proper evaluation now)
    predictions = model.predict(X_test_scaled)
    test_mae = np.mean(np.abs(predictions - y_test))

    print(f"Test MAE: {test_mae:.2f}")

    # Check for overfitting
    train_predictions = model.predict(X_train_scaled)
    train_mae = np.mean(np.abs(train_predictions - y_train))
    print(f"Train MAE: {train_mae:.2f}")

    if train_mae < test_mae * 0.7:
        print("Warning: Model may be overfitting (train MAE << test MAE)")

    # FIXED: Save both model and scaler
    joblib.dump({
        'model': model,
        'scaler': scaler,
        'feature_names': feature_cols
    }, 'fixed_model.pkl')

    return model, scaler

# ============================================================================
# FIXED: ML Heuristic with admissibility guarantee and error handling
# ============================================================================

class MLHeuristicFixed:
    """Fixed ML Heuristic with proper admissibility and error handling."""

    def __init__(self, model_path='fixed_model.pkl'):
        try:
            bundle = joblib.load(model_path)
            self.model = bundle['model']
            self.scaler = bundle['scaler']
            self.feature_names = bundle['feature_names']
        except FileNotFoundError:
            print(f"Warning: Model file not found, using Manhattan distance")
            self.model = None
            self.scaler = None

    def __call__(self, current, goal, grid=None):
        """Compute heuristic with admissibility guarantee."""
        # Calculate Manhattan distance (always needed for fallback/capping)
        manhattan = abs(current[0] - goal[0]) + abs(current[1] - goal[1])

        # Edge case: start equals goal
        if manhattan == 0:
            return 0.0

        # Fallback if model not loaded or grid is None
        if self.model is None or grid is None:
            return manhattan

        try:
            # Extract features using same function as training
            features = extract_features_fixed(grid, current, goal)

            # Normalize features
            features_scaled = self.scaler.transform([features])

            # Make prediction
            prediction = self.model.predict(features_scaled)[0]

            # FIXED: Ensure admissibility by capping at Manhattan distance
            # This guarantees h(n) <= h*(n) since Manhattan <= true distance
            prediction = max(0.0, min(prediction, manhattan))

            return prediction

        except Exception as e:
            print(f"Warning: Prediction failed ({e}), using Manhattan distance")
            return manhattan

# ============================================================================
# FIXED: Create diverse test grids
# ============================================================================

def create_test_grids_fixed():
    """Create test grids with different characteristics than training data."""
    test_grids = []

    # Use grid sizes and densities NOT in training set
    # Training used: [15, 20, 25] and [0.1, 0.2, 0.3]
    configs = [
        (18, 0.12),  # Intermediate values
        (18, 0.25),
        (22, 0.15),
        (22, 0.28),
        (27, 0.18),  # Larger grid
        (30, 0.22),  # Even larger
        (20, 0.05),  # Very sparse
        (20, 0.35),  # Very dense
    ]

    for i, (size, density) in enumerate(configs):
        grid = Grid(width=size, height=size, obstacle_density=density)
        start = (0, 0)
        goal = (size - 1, size - 1)
        grid.generate_obstacles(start, goal, seed=1000 + i)
        test_grids.append((grid, start, goal))

    return test_grids

# ============================================================================
# FIXED: Prediction function with error handling
# ============================================================================

def predict_distance_fixed(model, grid, start, goal):
    """Predict distance with comprehensive error handling."""
    # Edge case 1: start equals goal
    if start == goal:
        return 0.0

    # Edge case 2: grid is None
    if grid is None:
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    # Edge case 3: model not provided
    if model is None:
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    try:
        # Use fixed heuristic with admissibility guarantee
        if hasattr(model, '__call__'):
            # It's already a heuristic object
            return model(start, goal, grid)
        else:
            # It's a raw model, wrap it
            heuristic = MLHeuristicFixed(model)
            return heuristic(start, goal, grid)

    except Exception as e:
        print(f"Error in prediction: {e}")
        # Fallback to Manhattan
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

# ============================================================================
# Main execution with all fixes applied
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("Training FIXED ML Heuristic")
    print("="*70)

    # Train with all fixes applied
    model, scaler = train_model_fixed()

    print("\n" + "="*70)
    print("Testing on diverse grids")
    print("="*70)

    # Create diverse test grids
    test_grids = create_test_grids_fixed()

    # Load the fixed heuristic
    ml_heuristic = MLHeuristicFixed('fixed_model.pkl')

    # Test on first few grids
    for i, (grid, start, goal) in enumerate(test_grids[:3]):
        try:
            prediction = ml_heuristic(start, goal, grid)

            # Also compute true distance for comparison
            from pathfinding_lab.algorithms.bfs import bfs
            result = bfs(grid, start, goal)

            if result.success:
                true_dist = result.path_length
                manhattan_dist = abs(start[0] - goal[0]) + abs(start[1] - goal[1])

                print(f"\nTest {i+1}:")
                print(f"  Manhattan distance: {manhattan_dist}")
                print(f"  ML prediction:      {prediction:.1f}")
                print(f"  True distance:      {true_dist}")

                # Check admissibility
                if prediction > true_dist:
                    print(f"  ❌ INADMISSIBLE (prediction > true)")
                else:
                    print(f"  ✅ Admissible (prediction <= true)")

        except Exception as e:
            print(f"Test {i+1}: Error - {e}")

    print("\n" + "="*70)
    print("All bugs fixed!")
    print("="*70)
    print("\nKey improvements:")
    print("✅ Consistent feature extraction")
    print("✅ No data leakage (proper train/test split)")
    print("✅ Feature normalization with StandardScaler")
    print("✅ Admissibility guarantee (capped at Manhattan)")
    print("✅ Proper regularization (max_depth, min_samples)")
    print("✅ Comprehensive error handling")
    print("✅ Diverse test set (different from training)")
    print("="*70)
```

### What You Should Understand

1. **Feature Consistency is Critical**: Train and prediction must use identical features in the same order. Feature mismatch is a common source of poor performance.

2. **Data Leakage Inflates Metrics**: Training on test data makes your model look better than it is. Always maintain strict separation.

3. **Admissibility Requires Explicit Guarantees**: ML models don't naturally produce admissible heuristics. You must enforce it (e.g., capping at Manhattan distance).

4. **Feature Scaling Matters**: Even Random Forests can benefit from normalized features, and it's essential for many other models.

5. **Overfitting is Easy with Small Datasets**: 500 samples is relatively small for ML. Use regularization (max_depth, min_samples_split) and cross-validation.

6. **Diverse Test Data Tests Generalization**: Testing on similar data doesn't reveal generalization failures. Use different distributions.

7. **Error Handling is Not Optional**: Production ML code must handle edge cases gracefully. Always provide fallbacks.

8. **Cross-Validation Reveals Overfitting**: If CV scores are much worse than single-split scores, you're overfitting.

9. **Trade-off Between Accuracy and Admissibility**: Capping predictions at Manhattan distance ensures admissibility but may reduce prediction accuracy. This is the right trade-off for A*.

10. **ML Pipelines Have Many Failure Modes**: This exercise shows just a subset! Real ML projects require careful validation at every step.

---

## Summary and Key Takeaways

### When to Use ML Heuristics

✅ **Good Use Cases**:
- Recurring environments (same map played repeatedly)
- Very large grids (>50x50) where node reduction matters more
- Complex cost functions (not simple grid distances)
- Research and experimentation

❌ **Poor Use Cases**:
- General-purpose pathfinding on varied grids
- Real-time performance requirements
- When optimality is critical
- Small to medium grids (<30x30)

### Performance Reality Check

From Exercise 3, typical results show:

- **Node Reduction**: ML heuristics visit 10-30% fewer nodes
- **Runtime Impact**: ML heuristics are often 2-5x SLOWER overall
- **Admissibility**: ML models overestimate in 5-15% of cases
- **Conclusion**: Manhattan distance is usually superior for grid pathfinding

### Best Practices for ML Heuristics

1. **Feature Engineering**: Good features are 80% of success. Include geometric features, obstacle patterns, and domain knowledge.

2. **Data Quality**: Use diverse training data covering the full range of scenarios you'll encounter.

3. **Admissibility**: Always cap predictions at Manhattan distance or provide a classical fallback.

4. **Model Selection**: Random Forests are a good starting point (fast, robust, no scaling needed).

5. **Evaluation**: Test on grids different from training data to verify generalization.

6. **Fallback Strategy**: Always provide a classical heuristic fallback for reliability.

7. **Realistic Expectations**: ML heuristics are educational and interesting, but rarely superior to Manhattan distance for typical grid pathfinding.

### What You Learned

This week, you learned:
- How to generate training data for ML heuristics
- Feature engineering for pathfinding problems
- Training and evaluating regression models with scikit-learn
- Integrating ML models into A* search
- The trade-offs between learned and classical heuristics
- Common pitfalls in ML pipelines (data leakage, overfitting, admissibility violations)
- Why Manhattan distance is hard to beat for grid pathfinding

---

**End of Week 10 Solutions**
