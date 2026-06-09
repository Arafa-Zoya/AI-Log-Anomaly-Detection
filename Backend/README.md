# Log Anomaly Detection API

FastAPI backend for HDFS log anomaly detection using TF-IDF + Isolation Forest.

## Project Structure

```
log-anomaly-api/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   └── v1/
│   │       ├── router.py        # API v1 router aggregator
│   │       └── endpoints/
│   │           ├── predict.py   # Single & batch prediction endpoints
│   │           ├── train.py     # Model training endpoint
│   │           └── health.py    # Health check endpoint
│   ├── core/
│   │   ├── config.py            # App settings (env vars)
│   │   └── exceptions.py        # Custom exception handlers
│   ├── models/
│   │   └── ml_model.py          # Model loader/singleton
│   ├── schemas/
│   │   ├── predict.py           # Request/response Pydantic schemas
│   │   └── train.py             # Training schemas
│   └── services/
│       ├── predictor.py         # Prediction logic
│       └── trainer.py           # Training logic
├── scripts/
│   └── train_model.py           # Standalone training script
├── tests/
│   ├── test_predict.py
│   └── test_train.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Train the model

```bash
# Option 1: via script
python scripts/train_model.py --csv path/to/HDFS_2k.log_structured.csv

# Option 2: via API endpoint (POST /api/v1/train)
```

## Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/predict` | Predict anomaly for a single log line |
| POST | `/api/v1/predict/batch` | Predict anomalies for multiple log lines |
| POST | `/api/v1/train` | Re-train model from uploaded CSV |
| GET | `/api/v1/train/status` | Get training status |

## Example Usage

```bash
# Single prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"log_line": "081109 203518 143 INFO dfs.DataNode$PacketResponder: PacketResponder 0 for block blk_38865049064139660 terminating"}'

# Batch prediction
curl -X POST http://localhost:8000/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"log_lines": ["log line 1", "log line 2"]}'
```
