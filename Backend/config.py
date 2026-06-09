from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Log Anomaly Detection API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Artifact paths
    MODEL_PATH: str = "artifacts/model.pkl"
    VECTORIZER_PATH: str = "artifacts/vectorizer.pkl"

    # Isolation Forest hyperparameters
    IF_CONTAMINATION: float = 0.1
    IF_RANDOM_STATE: int = 42

    # TF-IDF hyperparameters
    TFIDF_MAX_FEATURES: int = 2000


settings = Settings()
