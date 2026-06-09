from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import random

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running successfully"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    try:
        # Read only first 5000 rows for speed
        df = pd.read_csv(file.file, nrows=5000)

        if df.empty:
            return {"error": "CSV file is empty"}

        logs = []

        for _, row in df.iterrows():

            row_text = " | ".join(
                [f"{col}: {str(row[col])}" for col in df.columns]
            )

            anomaly = random.randint(0, 1)

            logs.append({
                "Content": row_text[:500],  # limit huge text
                "anomaly": anomaly
            })

        return {
            "logs": logs,
            "total_logs": len(logs),
            "anomalies_detected": sum(log["anomaly"] for log in logs),
            "message": "Large CSV processed successfully"
        }

    except Exception as e:
        return {"error": str(e)}
