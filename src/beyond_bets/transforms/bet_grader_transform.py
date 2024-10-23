from pyspark.sql import DataFrame, functions as F
from src.beyond_bets.base.base_transform import BaseTransform

# Grade each bet relative to the average bet size in the last 15 minutes
class BetGraderTransform(BaseTransform):
    def transform(self) -> DataFrame:
        bets = self.data_access.fetch_bets()
        print("Grading bets...")
        fifteen_minutes_ago = F.current_timestamp() - F.expr('INTERVAL 15 MINUTES')
        recent_bets = bets.filter(F.col("timestamp") >= fifteen_minutes_ago)
        market_avg_bets = recent_bets.groupBy("market_id").agg(F.avg("bet_amount").alias("avg_bet_amount"))
        graded_bets = (bets.join(market_avg_bets, "market_id")
                       .withColumn("bet_grade", F.col("bet_amount") / F.col("avg_bet_amount")))

        return graded_bets.select("bet_id", "market_id", "bet_amount", "avg_bet_amount", "bet_grade")
