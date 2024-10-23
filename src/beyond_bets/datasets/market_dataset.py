from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

# Abstract base class for fetching market data
class MarketDataset(ABC):
    @abstractmethod
    def fetch_market_data(self) -> DataFrame:
        pass

# Concrete class for fetching market data from an API
class ApiBasedMarketDataset(MarketDataset):
    def fetch_market_data(self) -> DataFrame:
        print("Fetching market data from API...")
        # Example: loading data from an API
        return spark.read.format('json').load('market_data.json')
