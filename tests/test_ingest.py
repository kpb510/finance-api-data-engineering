import pytest
from unittest.mock import patch, Mock 
from src.ingestion import fetch_stock_data

@patch("src.ingestion.requests.get")
def test_fetch_stock_data_returns_json_on_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200 
    mock_response.json.return_value = {
        "Time Series (Daily)": {"2026-09-25": {"1. open": "150.00"}}
    }
    mock_get.return_value = mock_response 
    
    result = fetch_stock_data("AAPL")
    
    assert "Time Series (Daily)" in result
    
@patch("src.ingestion.requests.get")
def test_fetch_stock_data_raises_on_bad_status_code(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500 
    mock_get.return_value = mock_response
    
    with pytest.raises(Exception):
        fetch_stock_data("AAPL")

@patch("src.ingestion.requests.get")
def test_fetch_stock_data_raises_on_unexpected_json_shape(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200 
    mock_response.json.return_value = {"Note": "You have hit your rate limit"}
    mock_get.return_value = mock_response
    
    with pytest.raises(Exception):
        fetch_stock_data("AAPL")