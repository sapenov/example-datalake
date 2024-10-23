# File: /tests/test_player_market_daily.py

import pytest
from src.beyond_bets.transforms.player_market_daily_transform import PlayerMarketDailyTransform
from unittest.mock import Mock

def test_player_market_daily_transform(spark, generate_mock_data):
    # Use mock data fixture for both bets and market datasets
    mock_bets_data = generate_mock_data(data_points=1000)
    mock_market_data = generate_mock_data(data_points=1000)

    mock_bets_dataset = Mock()
    mock_bets_dataset.fetch_bets.return_value = mock_bets_data

    mock_market_dataset = Mock()
    mock_market_dataset.fetch_market_data.return_value = mock_market_data

    # Test PlayerMarketDailyTransform
    transform = PlayerMarketDailyTransform(mock_bets_dataset, mock_market_dataset)
    result = transform.transform()
    assert result.count() > 0  # Ensure data was processed
    assert "total_bets" in result.columns
