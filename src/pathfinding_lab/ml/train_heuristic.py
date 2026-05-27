"""Train a learned heuristic model."""

import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from pathfinding_lab.ml.dataset import generate_training_data


def train_heuristic_model(
    num_samples: int = 1000,
    grid_size: int = 20,
    model_path: str = "learned_heuristic_model.pkl"
) -> RandomForestRegressor:
    """
    Train a Random Forest model to predict distance to goal.

    Args:
        num_samples: Number of training samples
        grid_size: Grid size for training
        model_path: Path to save the trained model

    Returns:
        Trained model
    """
    print("Generating training data...")
    X, y = generate_training_data(num_samples, grid_size)

    print(f"Training on {len(X)} samples...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=20)
    model.fit(X_train, y_train)

    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"Train R² score: {train_score:.4f}")
    print(f"Test R² score: {test_score:.4f}")

    # Save model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"Model saved to {model_path}")

    return model


if __name__ == "__main__":
    # Train and save model
    train_heuristic_model()
