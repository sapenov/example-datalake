import pytest
from beyond_bets.transforms.bet_grader_transform import BetGraderTransform
from unittest.mock import Mock

def test_bet_grader_transform(spark, generate_mock_data):
    # Use mock data fixture
    mock_data = generate_mock_data(data_points=1000)

    mock_dataset = Mock()
    mock_dataset.fetch_bets.return_value = mock_data

    # Test BetGraderTransform
    transform = BetGraderTransform(mock_dataset)
    result = transform.transform()
    assert result.count() > 0  # Ensure data was processed
    assert "bet_grade" in result.columns
