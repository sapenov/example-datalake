from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

# Abstract base class for fetching bet data
class BetsDataset(ABC):
    @abstractmethod
    def fetch_bets(self) -> DataFrame:
        pass

# Concrete class for fetching bet data from a file
class FileBasedBetsDataset(BetsDataset):
    def fetch_bets(self) -> DataFrame:
        print("Fetching bets from file...")
        # Example: loading data from a JSON file
        return spark.read.format('json').load('bets_data.json')

# Optionally, here we can add other concrete classes,
# e.g., ApiBasedBetsDataset, DBBasedBetsDataset
