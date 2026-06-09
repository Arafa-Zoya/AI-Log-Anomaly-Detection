from fastapi import APIRouter

from app.schemas.predict import (
    BatchPredictRequest,
    BatchPredictResponse,
    PredictRequest,
    PredictResponse,
)
from app.services.predictor import predict_batch, predict_single

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post(
    "",
    response_model=PredictResponse,
    summary="Predict anomaly for a single log line",
)
async def predict(body: PredictRequest) -> PredictResponse:
    """
    Classify a single log line as **normal** or **anomalous**.

    Returns the raw Isolation Forest score alongside the boolean flag
    (`is_anomaly`). Lower scores indicate more anomalous behaviour.
    """
    return predict_single(body.log_line)


@router.post(
    "/batch",
    response_model=BatchPredictResponse,
    summary="Predict anomalies for multiple log lines",
)
async def predict_batch_endpoint(body: BatchPredictRequest) -> BatchPredictResponse:
    """
    Classify a list of log lines in one request.
    Returns per-line results plus aggregate counts.
    """
    return predict_batch(body.log_lines)
