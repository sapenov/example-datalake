from pyspark.sql import DataFrame, functions as F
from src.beyond_bets.base.base_transform import BaseTransform

# Transform bets data by player and hour
class PlayerHourlyTransform(BaseTransform):
    def transform(self) -> DataFrame:
        bets = self.data_access.fetch_bets()
        print("Applying PlayerHourly transformation...")
        return (bets.groupBy("player_id", F.window("timestamp", "1 hour"))
                .agg(F.sum("bet_amount").alias("total_bets")))
