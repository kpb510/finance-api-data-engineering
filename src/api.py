from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import polars as pl
import os 

app = FastAPI(title="Stock Data API")

# CORS: allows React frontend (running on a different port) to call this API.
# Without this, browsers block requests by default for security reasons.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite's default dev server port
    allow_methods=["GET"],
    allow_headers=["*"],
) 

PROCESSED_DIR = "data/processed"

@app.get("/api/tickers/{ticker}")
def get_ticker_data(ticker: str):
    """Return processed price history for a given ticker as JSON."""
    filepath = os.path.join(PROCESSED_DIR, f"{ticker.upper()}.parquet")
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"No data found for {ticker}")
    
    df = pl.read_parquet(filepath)
    return df.to_dicts()

@app.get("/api/tickers")
def list_tickers():
    """List al tickers we have processed data for."""
    files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith(".parquet")]
    tickers = [f.replace(".parquet", "") for f in files]
    return {"tickers": tickers}

@app.get("/api/tickers/{ticker}/analytics")
def get_ticker_analytics(ticker: str): 
    """Return processed price data enriched with computed analytics."""
    filepath = os.path.join(PROCESSED_DIR, f"{ticker.upper()}.parquet")
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"No data found for {ticker}")
    df = pl.read_parquet(filepath)
    df = df.with_columns([
        pl.col("close").rolling_mean(window_size=7).alias("moving_avg_7d"),
        (pl.col("close").pct_change() * 100 ).alias("daily_pct_change"),
    ])
    
    return df.to_dicts()