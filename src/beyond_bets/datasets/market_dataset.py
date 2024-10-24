from abc import ABC, abstractmethod
from pyspark.sql import DataFrame, SparkSession
import pyspark.sql.functions as F
from beyond_bets.datasets.bets_dataset import BetsDataset, FileBasedBetsDataset  # Import BetsDataset and concrete implementation


# Abstract base class for fetching market data
class MarketDataset(ABC):
    @abstractmethod
    def fetch_market_data(self) -> DataFrame:
        pass

# Concrete class for fetching market data from an API
class ApiBasedMarketDataset(MarketDataset):

    def __init__(self, bets_dataset: BetsDataset):
        self.bets_dataset = bets_dataset  # Initialize with a BetsDataset object

    def fetch_market_data(self) -> DataFrame:
        print("Fetching market data from bets dataset...")

        # Fetch the bets data from the bets dataset
        bets_data = self.bets_dataset.fetch_bets()

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
