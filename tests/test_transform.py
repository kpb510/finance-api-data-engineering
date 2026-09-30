import polars as pl
from src.transform import parse_to_dataframe 

def test_parse_to_dataframe_returns_correct_columns():
    fake_raw_data = {
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
    
    df = parse_to_dataframe(fake_raw_data)
    
    assert df.columns == ["date", "open", "high", "low", "close", "volume"]
    assert df.height == 2
    
def test_parse_to_dataframe_sorts_by_date_ascending():
    fake_raw_data = {
        "Time Series (Daily)": {
            "2026-09-25": {"1. open": "150.00", "2. high": "152.50", "3. low": "149.00", "4. close": "151.25", "5. volume": "1000000"},
            "2026-09-24": {"1. open": "148.00", "2. high": "150.00", "3. low": "147.50", "4. close": "149.75", "5. volume": "900000"},
        }
    }

    df = parse_to_dataframe(fake_raw_data)

    dates = df["date"].to_list()
    assert dates == sorted(dates)

def test_parse_to_dataframe_converts_values_to_float():
    fake_raw_data = {
        "Time Series (Daily)": {
            "2026-09-25": {"1. open": "150.00", "2. high": "152.50", "3. low": "149.00", "4. close": "151.25", "5. volume": "1000000"}
        }
    }

    df = parse_to_dataframe(fake_raw_data)

    assert df["close"].dtype == pl.Float64