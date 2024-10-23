# File: /tests/conftest.py

import math
from random import Random
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType
from datetime import datetime, timedelta, date
import pytest

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local").appName("TestApp").getOrCreate()

def get_rand_stream(seed: int):
    return Random(seed)

@pytest.fixture
def generate_mock_data(spark):
    def _generate(data_points: int = 1000):
        # Set up deterministic mock data
        _today: date = date.today()
        _now: datetime = datetime(_today.year, _today.month, _today.day)
        _days: int = 10
        _markets: list[str] = [
            "MIA @ BOS Over 110.5",
            "LAL @ CHI Under 107.5",
            "DEN @ GSW Over 115.5",
            "DET @ OKC Over 111.5",
        ]
        _odds: list[int] = [-115, -110, -105]

        # individual streams to help with determinism
        market_rand_stream: Random = get_rand_stream(500)
        time_rand_stream: Random = get_rand_stream(333)
        odds_rand_stream: Random = get_rand_stream(27)
        amt_rand_stream: Random = get_rand_stream(88)
        player_rand_stream: Random = get_rand_stream(100)

        return spark.createDataFrame(
            [
                (
                    market_rand_stream.choice(_markets),
                    odds_rand_stream.choice(_odds),
                    _now - timedelta(seconds=time_rand_stream.randint(0, _days * 3600 * 24)),
                    (amt_rand_stream.random() * 1999) + 1,
                    player_rand_stream.randint(1, math.ceil(data_points / 100)),
                )
                for _ in range(data_points)
            ],
            schema=StructType(
                [
                    StructField("market", StringType(), False),
                    StructField("odds", IntegerType(), False),
                    StructField("timestamp", TimestampType(), False),
                    StructField("bet_amount", DoubleType(), False),
                    StructField("player_id", IntegerType(), False),
                ]
            ),
        )
    return _generate
