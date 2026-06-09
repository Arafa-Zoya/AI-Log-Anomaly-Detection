"""
Standalone script to train the model outside of the API.

Usage:
    python scripts/train_model.py --csv path/to/HDFS_2k.log_structured.csv
"""

import argparse
import sys
from pathlib import Path

# Allow running from project root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from app.services.trainer import train_from_dataframe


def main():
    parser = argparse.ArgumentParser(description="Train the log anomaly detection model.")
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to the structured log CSV file (must have a 'Content' column).",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"[ERROR] File not found: {csv_path}")
        sys.exit(1)

    print(f"[INFO] Loading {csv_path} ...")
    df = pd.read_csv(csv_path)
    print(f"[INFO] {len(df)} rows loaded. Training model ...")

    result = train_from_dataframe(df)

    print(f"\n✅ {result.message}")
    print(f"   Rows trained   : {result.rows_trained}")
    print(f"   Anomalies found: {result.anomaly_count} ({result.anomaly_ratio:.1%})")
    print(f"   Model saved to : {result.model_path}")
    print(f"   Vectorizer     : {result.vectorizer_path}")


if __name__ == "__main__":
    main()
