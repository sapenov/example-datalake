from pyspark.sql import DataFrame, functions as F
from beyond_bets.datasets.bets_dataset import BetsDataset
from beyond_bets.datasets.market_dataset import MarketDataset

# Combine player and market data by day
class PlayerMarketDailyTransform:
    def __init__(self, bets_data: BetsDataset, market_data: MarketDataset):
        self.bets_data = bets_data
        self.market_data = market_data

    def transform(self) -> DataFrame:
        bets = self.bets_data.fetch_bets()
        market = self.market_data.fetch_market_data()
        print("Applying PlayerMarketDaily transformation...")

        # Select relevant columns from each DataFrame to avoid ambiguity
        bets = bets.select("player_id", "market_id", "bet_amount", "timestamp")
        market = market.select("market_id", "day")  # No need to keep player_id from market data

        # Perform the join and group by player_id and market
        return (bets.join(market, ["market_id"])
        .groupBy("player_id", "market_id", "day")
        .agg(F.sum("bet_amount").alias("total_bets")))
