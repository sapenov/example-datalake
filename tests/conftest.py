import math
from random import Random
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType
from datetime import datetime, timedelta, date
import pytest
import os, random
from pyspark.sql import functions as F

@pytest.fixture(scope="module")
def spark():
    # Change this to your own settings
    os.environ["PYSPARK_PYTHON"] = r"C:\Users\Khazret\PycharmProjects\bbets\venv\Scripts\python.exe"
    os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\Khazret\PycharmProjects\bbets\venv\Scripts\python.exe"
    os.environ["HADOOP_HOME"] = r"C:\hadoop"

    return SparkSession.builder.master("local[*]").appName("TestApp").getOrCreate()

def get_rand_stream(seed: int):
    return Random(seed)


@pytest.fixture
def generate_mock_data(spark):
    def _generate(data_points: int = 1000):
        # Set up deterministic mock data
        _now = datetime.now()
        _markets = ["MIA @ BOS Over 110.5", "LAL @ CHI Under 107.5", "DEN @ GSW Over 115.5", "DET @ OKC Over 111.5"]
        _odds = [-115, -110, -105]

        # Generate mock data
        return spark.createDataFrame(
            [
                (
                    f"bet_{i}",
                    _markets[i % len(_markets)],
                    _odds[i % len(_odds)],
                    # _now - timedelta(minutes=i % 30),
                    # Randomize the timestamp within the past two weeks
                    _now - timedelta(days=random.randint(0, 13), minutes=random.randint(0, 1440)),
                    (i + 1) * 10.0,
                    i % 100
                )
                for i in range(data_points)
            ],
            schema=StructType(
                [
                    StructField("bet_id", StringType(), False),
                    StructField("market_id", StringType(), False),
                    StructField("odds", IntegerType(), False),
                    StructField("timestamp", TimestampType(), False),
                    StructField("bet_amount", DoubleType(), False),
                    StructField("player_id", IntegerType(), False),
                ]
            )
        )
    return _generate

@pytest.fixture
def generate_mock_data_md(spark, generate_mock_data):
    def _generate():
        print("Fetching market data from bets dataset...")

        # Fetch the bets data from the bets dataset
        bets_data = generate_mock_data()

        # Aggregate data from bets to generate market-level data
        market_data = bets_data.groupBy("market_id", F.window("timestamp", "1 week")).agg(
            F.sum("bet_amount").alias("market_value"),
            F.avg("odds").alias("average_odds"),
            F.count("bet_id").alias("total_bets"),
        )

        # Select the necessary fields and add day and hour columns
        market_data_with_day_hour = market_data.select(
            "market_id",
            # F.col("window.start").alias("start_time"),
            # F.col("window.end").alias("end_time"),
            F.date_format(F.col("window.start"), "yyyy-MM-dd").alias("day"),  # Extract the day
            F.hour(F.col("window.start")).alias("hour"),  # Extract the hour
            "market_value",
            "average_odds",
            "total_bets"
        )

        # Order by day and hour
        market_data_ordered = market_data_with_day_hour.orderBy("day", "hour")

        return market_data_ordered

    return _generate