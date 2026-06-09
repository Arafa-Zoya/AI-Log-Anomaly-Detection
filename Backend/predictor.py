"""
Predictor service: transforms raw log strings → anomaly predictions.
"""

from app.core.exceptions import InvalidInputError
from app.models.ml_model import ml_model
from app.schemas.predict import BatchPredictResponse, PredictResponse


def predict_single(log_line: str) -> PredictResponse:
    """Run anomaly detection on a single log line."""
    ml_model.assert_ready()

    if not log_line.strip():
        raise InvalidInputError("log_line must not be empty or whitespace.")

    X = ml_model.vectorizer.transform([log_line])
    prediction = ml_model.model.predict(X)[0]       # 1 = normal, -1 = anomaly
    score = ml_model.model.score_samples(X)[0]      # lower = more anomalous

    return PredictResponse(
        log_line=log_line,
        is_anomaly=bool(prediction == -1),
        anomaly_score=float(score),
    )


def predict_batch(log_lines: list[str]) -> BatchPredictResponse:
    """Run anomaly detection on a list of log lines."""
    ml_model.assert_ready()

    if not log_lines:
        raise InvalidInputError("log_lines list must not be empty.")

    X = ml_model.vectorizer.transform(log_lines)
    predictions = ml_model.model.predict(X)
    scores = ml_model.model.score_samples(X)

    results = [
        PredictResponse(
            log_line=line,
            is_anomaly=bool(pred == -1),
            anomaly_score=float(score),
        )
        for line, pred, score in zip(log_lines, predictions, scores)
    ]

    anomaly_count = sum(1 for r in results if r.is_anomaly)

    return BatchPredictResponse(
        results=results,
        total=len(results),
        anomaly_count=anomaly_count,
    )
