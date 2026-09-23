import os 
import json
import requests 
from datetime import datetime 
from dotenv import load_dotenv

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

if __name__ == "__main__":
    ticker = "AAPL"
    raw_data = fetch_stock_data(ticker)
    save_raw_json(raw_data, ticker)