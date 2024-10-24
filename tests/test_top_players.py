# File: /tests/test_top_players.py

import pytest
from beyond_bets.transforms.top_players_transform import TopPlayersTransform
from unittest.mock import Mock

def test_top_players_transform(spark, generate_mock_data):
    # Use mock data fixture
    mock_data = generate_mock_data(data_points=1000)

    mock_dataset = Mock()
    mock_dataset.fetch_bets.return_value = mock_data

    # Test TopPlayersTransform
    transform = TopPlayersTransform(mock_dataset)
    result = transform.transform()
    assert result.count() > 0  # Ensure top players are selected
    assert "total_spend" in result.columns
