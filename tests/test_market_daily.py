# File: /tests/test_market_daily.py

import pytest
from beyond_bets.transforms.market_daily_transform import MarketDailyTransform
from unittest.mock import Mock

def test_market_daily_transform(spark, generate_mock_data_md):
    # Use mock data fixture
    mock_data = generate_mock_data_md()

    mock_dataset = Mock()
    mock_dataset.fetch_market_data.return_value = mock_data

    # Test MarketDailyTransform
    md = MarketDailyTransform(mock_dataset)
    result = md.transform()
    assert result.count() > 0  # Ensure data was processed
    assert "market_value" in result.columns
