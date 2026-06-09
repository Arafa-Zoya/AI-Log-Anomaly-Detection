"""
Singleton that holds the loaded model and vectorizer in memory.
Call `load()` at startup; the rest of the app imports `ml_model`.
"""

import os
import pickle
from dataclasses import dataclass, field
from typing import Optional

from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

from app.core.config import settings
from app.core.exceptions import ModelNotLoadedError


@dataclass
class MLModel:
    model: Optional[IsolationForest] = field(default=None, repr=False)
    vectorizer: Optional[TfidfVectorizer] = field(default=None, repr=False)

    # ------------------------------------------------------------------ #
    # Load / save                                                          #
    # ------------------------------------------------------------------ #

    def load(self, model_path: str | None = None, vectorizer_path: str | None = None) -> None:
        """Load model and vectorizer from disk. Silently skips if files are absent."""
        model_path = model_path or settings.MODEL_PATH
        vectorizer_path = vectorizer_path or settings.VECTORIZER_PATH

        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            with open(vectorizer_path, "rb") as f:
                self.vectorizer = pickle.load(f)
            print(f"[MLModel] Loaded model from {model_path}")
        else:
            print("[MLModel] No saved artifacts found — model not loaded.")

    def save(self, model_path: str | None = None, vectorizer_path: str | None = None) -> None:
        """Persist model and vectorizer to disk."""
        model_path = model_path or settings.MODEL_PATH
        vectorizer_path = vectorizer_path or settings.VECTORIZER_PATH

        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        os.makedirs(os.path.dirname(vectorizer_path), exist_ok=True)

        with open(model_path, "wb") as f:
            pickle.dump(self.model, f)
        with open(vectorizer_path, "wb") as f:
            pickle.dump(self.vectorizer, f)

    # ------------------------------------------------------------------ #
    # Guards                                                               #
    # ------------------------------------------------------------------ #

    def assert_ready(self) -> None:
        if self.model is None or self.vectorizer is None:
            raise ModelNotLoadedError(
                "Model is not loaded. Train a model first via POST /api/v1/train."
            )

    @property
    def is_ready(self) -> bool:
        return self.model is not None and self.vectorizer is not None


# Module-level singleton — import this everywhere
ml_model = MLModel()
