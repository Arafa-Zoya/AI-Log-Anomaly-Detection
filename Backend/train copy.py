from pydantic import BaseModel, Field


class TrainResponse(BaseModel):
    message: str
    rows_trained: int
    anomaly_count: int
    anomaly_ratio: float = Field(description="Fraction of rows flagged as anomalous.")
    model_path: str
    vectorizer_path: str


class TrainStatusResponse(BaseModel):
    model_loaded: bool
    model_path: str
    vectorizer_path: str
