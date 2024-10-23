from pyspark.sql import DataFrame, functions as F
from src.beyond_bets.base.base_transform import BaseTransform
from src.beyond_bets.datasets.market_dataset import MarketDataset

# Transform market data by market and day
class MarketDailyTransform(BaseTransform):
    def __init__(self, data_access: MarketDataset):
        self.data_access = data_access

    def transform(self) -> DataFrame:
        market_data = self.data_access.fetch_market_data()
        print("Applying MarketDaily transformation...")
        return (market_data.groupBy("market_id", F.window("timestamp", "1 day"))
                .agg(F.sum("bet_amount").alias("total_bets")))
