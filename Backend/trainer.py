"""
Trainer service: reads a CSV, fits TF-IDF + Isolation Forest, saves artifacts.
"""

import io

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

from app.core.config import settings
from app.core.exceptions import InvalidInputError, TrainingError
from app.models.ml_model import ml_model
from app.schemas.train import TrainResponse


def train_from_dataframe(df: pd.DataFrame) -> TrainResponse:
    """
    Fit a new model on the given DataFrame.
    The DataFrame must contain a 'Content' column (same as the notebook).
    """
    if "Content" not in df.columns:
        raise InvalidInputError(
            "CSV must contain a 'Content' column with log text. "
            f"Found columns: {list(df.columns)}"
        )

    logs = df["Content"].dropna().astype(str)
    if logs.empty:
        raise InvalidInputError("The 'Content' column is empty after dropping nulls.")

    try:
        vectorizer = TfidfVectorizer(max_features=settings.TFIDF_MAX_FEATURES)
        X = vectorizer.fit_transform(logs)

        model = IsolationForest(
            contamination=settings.IF_CONTAMINATION,
            random_state=settings.IF_RANDOM_STATE,
        )
        model.fit(X)
    except Exception as exc:
        raise TrainingError(f"Training failed: {exc}") from exc

    # Store in singleton
    ml_model.model = model
    ml_model.vectorizer = vectorizer
    ml_model.save()

    # Compute stats
    predictions = model.predict(X)
    anomaly_count = int((predictions == -1).sum())

    return TrainResponse(
        message="Model trained and saved successfully.",
        rows_trained=len(logs),
        anomaly_count=anomaly_count,
        anomaly_ratio=round(anomaly_count / len(logs), 4),
        model_path=settings.MODEL_PATH,
        vectorizer_path=settings.VECTORIZER_PATH,
    )


def train_from_csv_bytes(file_bytes: bytes) -> TrainResponse:
    """Parse CSV bytes then delegate to train_from_dataframe."""
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as exc:
        raise InvalidInputError(f"Could not parse uploaded file as CSV: {exc}") from exc
    return train_from_dataframe(df)
