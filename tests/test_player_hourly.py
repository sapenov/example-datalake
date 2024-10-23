# File: /tests/test_player_hourly.py

import pytest
from src.beyond_bets.transforms.player_hourly_transform import PlayerHourlyTransform
from unittest.mock import Mock

def test_player_hourly_transform(spark, generate_mock_data):
    # Use mock data fixture
    mock_data = generate_mock_data(data_points=1000)

    mock_dataset = Mock()
    mock_dataset.fetch_bets.return_value = mock_data

    # Test PlayerHourlyTransform
    transform = PlayerHourlyTransform(mock_dataset)
    result = transform.transform()
    assert result.count() == 1000  # Ensure data was processed
    assert "total_bets" in result.columns
