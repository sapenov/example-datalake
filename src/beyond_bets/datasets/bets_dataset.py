from abc import ABC, abstractmethod
from pyspark.sql import DataFrame, SparkSession

from datetime import datetime, timedelta
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType
import random


# Abstract base class for fetching bet data
class BetsDataset(ABC):
    @abstractmethod
    def fetch_bets(self) -> DataFrame:
        pass

# Concrete class for fetching bet data from a file
class FileBasedBetsDataset(BetsDataset):
    def __init__(self, spark: SparkSession):
        self.spark = spark  # Initialize Spark session
    def fetch_bets(self) -> DataFrame:
        print("Fetching bets from file...")
        # Example: loading data from a JSON file
        # return self.spark.read.format('json').load('bets_data.json')
        # Generate sample data
        mock_data = generate_mock_data(self.spark, 1000)

        return mock_data


# Optionally, here we can add other concrete classes,
# e.g., ApiBasedBetsDataset, DBBasedBetsDataset

def generate_mock_data(spark, data_points=1000):

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


