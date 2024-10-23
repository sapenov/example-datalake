# File: /tests/test_market_daily.py

import pytest
from src.beyond_bets.transforms.market_daily_transform import MarketDailyTransform
from unittest.mock import Mock

def test_market_daily_transform(spark, generate_mock_data):
    # Use mock data fixture
    mock_data = generate_mock_data(data_points=1000)

    mock_dataset = Mock()
    mock_dataset.fetch_market_data.return_value = mock_data

    # Test MarketDailyTransform
    transform = MarketDailyTransform(mock_dataset)
    result = transform.transform()
    assert result.count() > 0  # Ensure data was processed
    assert "total_bets" in result.columns
