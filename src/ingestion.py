import os 
import requests 
import polars as pl
from datetime import datetime 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def fetch_stock_data(ticker: str) -> pl.DataFrame:
    """Fetch daily time series data for a given stock ticker from Alpha Vantage."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")
    
    data = response.json()
    
    if "Time Series (Daily)" not in data:
        raise Exception(f"Unexpected API response: {data}")
    
    time_series = data["Time Series (Daily)"]
    
    # Reshape nested JSON into flat list of row dicts 
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

def save_raw_data(df: pl.DataFrame, ticker: str, output_dir: str = "data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    fetch_date = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(output_dir, f"{ticker}_{fetch_date}.csv")
    df.write_csv(filepath)
    print(f"Saved {df.height} rows to {filepath}")
    return filepath

if __name__ == "__main__":
    ticker = "AAPL"
    df = fetch_stock_data(ticker)
    print(df.head())
    save_raw_data(df, ticker) 