import os 
import json
import time
import requests 
from datetime import datetime 
from dotenv import load_dotenv
from config import TICKERS, REQUEST_DELAY_SECONDS

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def fetch_stock_data(ticker: str) -> dict:
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
    
    return data

def save_raw_json(data: dict, ticker: str, output_dir: str = "data/raw") -> str:
    """Persist the untouched API response, timestamped so re-runs never overwrite."""
    os.makedirs(output_dir, exist_ok=True)
    run_timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filepath = os.path.join(output_dir, f"{ticker}_{run_timestamp}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved raw response to {filepath}")
    return filepath

def run_ingestion(tickers: list[str]):
    """Fetch and save raw data for each ticker, pacing requests to respect rate limits."""
    for i, ticker in enumerate(tickers):
        print(f"Fetching {ticker}...")
        raw_data = fetch_stock_data(ticker)
        save_raw_json(raw_data, ticker)
        
        is_last = (i == len(tickers) - 1)
        if not is_last:
            print(f"Waiting {REQUEST_DELAY_SECONDS}s before next request...")
            time.sleep(REQUEST_DELAY_SECONDS)
            
            
if __name__ == "__main__":
    run_ingestion(TICKERS)