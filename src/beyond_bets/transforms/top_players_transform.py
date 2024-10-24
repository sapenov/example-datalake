from pyspark.sql import DataFrame, functions as F
from beyond_bets.base.base_transform import BaseTransform

# Get the top 1% of players by total betting spend
class TopPlayersTransform(BaseTransform):
    def transform(self) -> DataFrame:
        bets = self.data_access.fetch_bets()
        print("Calculating top players...")
        # Calculate total spend per player over the past week
        total_spend_per_player = (bets.groupBy("player_id")
                                  .agg(F.sum("bet_amount").alias("total_spend")).orderBy(F.col("total_spend").desc()))
        top_percent_count = int(total_spend_per_player.count() * 0.03)  # Top 1% of players Edit: I changed it to top 3%

        df = total_spend_per_player.limit(top_percent_count)
        df.show()
        return df
