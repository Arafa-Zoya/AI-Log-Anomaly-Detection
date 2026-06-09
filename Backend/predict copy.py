from pydantic import BaseModel, Field


# ------------------------------------------------------------------ #
# Request schemas                                                      #
# ------------------------------------------------------------------ #


class PredictRequest(BaseModel):
    log_line: str = Field(
        ...,
        min_length=1,
        description="A single raw log line to classify.",
        examples=["081109 203518 143 INFO dfs.DataNode$PacketResponder: PacketResponder 0 terminating"],
    )


class BatchPredictRequest(BaseModel):
    log_lines: list[str] = Field(
        ...,
        min_length=1,
        description="List of raw log lines to classify.",
    )


# ------------------------------------------------------------------ #
# Response schemas                                                     #
# ------------------------------------------------------------------ #


class PredictResponse(BaseModel):
    log_line: str
    is_anomaly: bool = Field(description="True if the log line is detected as anomalous.")
    anomaly_score: float = Field(description="Raw isolation forest score (lower = more anomalous).")


class BatchPredictResponse(BaseModel):
    results: list[PredictResponse]
    total: int
    anomaly_count: int
