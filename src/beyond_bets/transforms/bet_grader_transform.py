from pyspark.sql import DataFrame, functions as F
from beyond_bets.base.base_transform import BaseTransform

# BetGraderTransform: Grade each bet relative to the average bet size in the last 15 minutes
class BetGraderTransform(BaseTransform):
    def transform(self) -> DataFrame:
        bets = self.data_access.fetch_bets()
        print("Fetched bets:")
        bets.show()  # Show the fetched bets before filtering

        print("Grading bets...")
        #fifteen_minutes_ago = F.current_timestamp() - F.expr('INTERVAL 15 MINUTES')
        fifteen_days_ago = F.current_timestamp() - F.expr('INTERVAL 15 DAYS')
        recent_bets = bets.filter(F.col("timestamp") >= fifteen_days_ago)
        print("Recent bets (last 15 minutes):")
        recent_bets.show()  # Show the recent bets after filtering

        market_avg_bets = recent_bets.groupBy("market_id").agg(F.avg("bet_amount").alias("avg_bet_amount"))
        print("Market average bets:")
        market_avg_bets.show()  # Show the market average bets

        graded_bets = bets.join(market_avg_bets, "market_id").withColumn("bet_grade", F.col("bet_amount") / F.col("avg_bet_amount"))

        return graded_bets.select("bet_id", "market_id", "bet_amount", "avg_bet_amount", "bet_grade")


