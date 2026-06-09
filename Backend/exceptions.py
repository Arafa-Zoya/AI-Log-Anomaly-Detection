from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ModelNotLoadedError(Exception):
    """Raised when a prediction is attempted but no model is loaded."""


class TrainingError(Exception):
    """Raised when model training fails."""


class InvalidInputError(Exception):
    """Raised when the input data is invalid or empty."""


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ModelNotLoadedError)
    async def model_not_loaded_handler(request: Request, exc: ModelNotLoadedError):
        return JSONResponse(
            status_code=503,
            content={
                "error": "ModelNotLoaded",
                "detail": (
                    str(exc)
                    or "No trained model found. POST /api/v1/train to train one first."
                ),
            },
        )

    @app.exception_handler(TrainingError)
    async def training_error_handler(request: Request, exc: TrainingError):
        return JSONResponse(
            status_code=500,
            content={"error": "TrainingError", "detail": str(exc)},
        )

    @app.exception_handler(InvalidInputError)
    async def invalid_input_handler(request: Request, exc: InvalidInputError):
        return JSONResponse(
            status_code=422,
            content={"error": "InvalidInput", "detail": str(exc)},
        )
