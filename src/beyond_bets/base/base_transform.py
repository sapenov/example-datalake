from abc import ABC, abstractmethod
from pyspark.sql import DataFrame
from beyond_bets.datasets.bets_dataset import BetsDataset

# Base class for transformations, adhering to OCP and SRP
class BaseTransform(ABC):
    def __init__(self, data_access: BetsDataset):
        self.data_access = data_access

    @abstractmethod
    def transform(self) -> DataFrame:
        pass
