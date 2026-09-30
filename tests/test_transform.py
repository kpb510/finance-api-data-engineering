import pytest
import polars as pl
from src.transform import parse_to_dataframe 

@pytest.fixture
def sample_raw_data():
    """Reuseable fake Alpha Vantage API response, shaped like the real thing."""
    return {
        "Time Series (Daily)": {
            "2026-09-25": {
                "1. open": "150.00",
                "2. high": "152.50",
                "3. low": "149.00",
                "4. close": "151.25",
                "5. volume": "1000000"
            },
            "2026-09-24": {
                "1. open": "148.00",
                "2. high": "150.00",
                "3. low": "147.50",
                "4. close": "149.75",
                "5. volume": "900000"
            }
        }
    }
    
    
def test_parse_to_dataframe_returns_correct_columns(sample_raw_data):
    df = parse_to_dataframe(sample_raw_data)    
    assert df.columns == ["date", "open", "high", "low", "close", "volume"]
    assert df.height == 2
    
def test_parse_to_dataframe_sorts_by_date_ascending(sample_raw_data):
    df = parse_to_dataframe(sample_raw_data)
    dates = df["date"].to_list()
    assert dates == sorted(dates)

def test_parse_to_dataframe_converts_values_to_float(sample_raw_data):
    df = parse_to_dataframe(sample_raw_data)
    assert df["close"].dtype == pl.Float64