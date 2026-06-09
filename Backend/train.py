from fastapi import APIRouter, UploadFile, File

from app.core.config import settings
from app.models.ml_model import ml_model
from app.schemas.train import TrainResponse, TrainStatusResponse
from app.services.trainer import train_from_csv_bytes

router = APIRouter(prefix="/train", tags=["Training"])


@router.post(
    "",
    response_model=TrainResponse,
    summary="Train (or re-train) the model from an uploaded CSV",
)
async def train(file: UploadFile = File(..., description="CSV file with a 'Content' column")) -> TrainResponse:
    """
    Upload a structured log CSV (must contain a **Content** column).
    The endpoint fits a fresh TF-IDF vectorizer and Isolation Forest,
    then saves the artifacts to disk and hot-swaps the in-memory model.

    Replaces any previously loaded model.
    """
    contents = await file.read()
    return train_from_csv_bytes(contents)


@router.get(
    "/status",
    response_model=TrainStatusResponse,
    summary="Check whether a trained model is available",
)
async def train_status() -> TrainStatusResponse:
    return TrainStatusResponse(
        model_loaded=ml_model.is_ready,
        model_path=settings.MODEL_PATH,
        vectorizer_path=settings.VECTORIZER_PATH,
    )
