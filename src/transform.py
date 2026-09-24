import os
import json 
import glob
import polars as pl 
from config import TICKERS

def load_latest_raw_json(ticker: str, raw_dir: str = "data/raw") -> dict:
    """Find and load the most recently saved raw JSON file for a ticker."""
    pattern = os.path.join(raw_dir, f"{ticker}_*.json")
    matches = sorted(glob.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No raw data found for {ticker}")
    latest_file = matches[-1]
    with open(latest_file, "r") as f:
        return json.load(f)
    
def parse_to_dataframe(raw_data: dict) -> pl.DataFrame:
    """Flatten Alpha Vantage's nested JSON into a typed Polars DataFrame."""
    time_series = raw_data["Time Series (Daily)"]
    
    records = []
    for date_str, values in time_series.items():
        record = {"date": date_str}
        for key, value in values.items():
            clean_key = key.split(". ")[1] # "1. open" -> "open"
            record[clean_key] = float(value)
        records.append(record)
    
    df = pl.DataFrame(records)
    df = df.with_columns(pl.col("date").str.to_date())
    df = df.sort("date")
    return df 

def save_processed_parquet(df: pl.DataFrame, ticker: str, output_dir: str = "data/processed") -> str:
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{ticker}.parquet")
    df.write_parquet(filepath)
    print(f"Saved {df.height} rows to {filepath}")
    return filepath

def run_transform(tickers: list[str]):
    """Transform each ticker's latest raw JSON into a processed Parquet file."""
    for ticker in tickers:
        print(f"Transforming {ticker}...")
        raw_data = load_latest_raw_json(ticker)
        df = parse_to_dataframe(raw_data)
        save_processed_parquet(df, ticker)

if __name__ == "__main__":
    run_transform(TICKERS)