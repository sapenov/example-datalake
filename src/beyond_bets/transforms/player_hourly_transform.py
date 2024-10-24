from pyspark.sql import DataFrame, functions as F
from beyond_bets.base.base_transform import BaseTransform

# Transform bets data by player and hour
class PlayerHourlyTransform(BaseTransform):
    def transform(self) -> DataFrame:
        bets = self.data_access.fetch_bets()
        print("Applying PlayerHourly transformation...")
        bets_hourly = (bets.groupBy("player_id", F.window("timestamp", "1 hour"))
                       .agg(F.sum("bet_amount").alias("total_bets_amount") ))

        # Select the necessary fields and add day and hour columns
        bets_hourly_with_day_hour = bets_hourly.select(
            "player_id",
            F.col("window.start").alias("start_time"),
            F.col("window.end").alias("end_time"),
            F.date_format(F.col("window.start"), "yyyy-MM-dd").alias("day"),  # Extract the day
            F.hour(F.col("window.start")).alias("hour"),  # Extract the hour
            "total_bets_amount"
        )

        # Order by day and hour
        bets_ordered = bets_hourly_with_day_hour.orderBy("player_id","day", "hour")
        bets_ordered.show()

        return bets_ordered
