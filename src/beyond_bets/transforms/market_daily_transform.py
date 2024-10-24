from pyspark.sql import DataFrame, functions as F, Window
from beyond_bets.base.base_transform import BaseTransform
from beyond_bets.datasets.market_dataset import MarketDataset

# Transform market data by market and day
class MarketDailyTransform(BaseTransform):
    def __init__(self, data_access: MarketDataset):
        self.data_access = data_access

    def transform(self) -> DataFrame:
        market_data = self.data_access.fetch_market_data()
        print("Applying MarketDaily transformation...")

        # Apply transformations
        market_data = self.add_daily_trends(market_data)
        market_data = self.add_moving_average(market_data)
        market_data = self.add_volatility(market_data)
        market_data = self.detect_anomalies(market_data)
        market_data = self.calculate_market_share(market_data)
        #market_data = self.add_cumulative_sums(market_data)

        # Show the final transformed data
        market_data.show()
        return market_data

    def add_daily_trends(self, market_data: DataFrame) -> DataFrame:
        window_spec = Window.partitionBy("market_id").orderBy("day")
        market_data = market_data.withColumn("prev_market_value", F.lag("market_value", 1).over(window_spec))
        market_data = market_data.withColumn("market_value_diff", F.col("market_value") - F.col("prev_market_value"))
        return market_data

    def add_moving_average(self, market_data: DataFrame) -> DataFrame:
        window_spec = Window.partitionBy("market_id").orderBy("day").rowsBetween(-6, 0)
        market_data = market_data.withColumn("7_day_avg_market_value", F.avg("market_value").over(window_spec))
        return market_data

    def add_volatility(self, market_data: DataFrame) -> DataFrame:
        window_spec = Window.partitionBy("market_id").orderBy("day")
        market_data = market_data.withColumn("volatility", F.stddev("market_value").over(window_spec))
        return market_data

    def detect_anomalies(self, market_data: DataFrame) -> DataFrame:
        window_spec = Window.partitionBy("market_id").orderBy("day")
        avg_value = F.avg("market_value").over(window_spec)
        stddev_value = F.stddev("market_value").over(window_spec)
        market_data = market_data.withColumn("is_anomaly", (F.col("market_value") > (avg_value + 3 * stddev_value)) |
                                                           (F.col("market_value") < (avg_value - 3 * stddev_value)))
        return market_data

    def calculate_market_share(self, market_data: DataFrame) -> DataFrame:
        total_value = market_data.agg(F.sum("market_value").alias("total_market_value")).collect()[0]["total_market_value"]
        market_data = market_data.withColumn("market_share", F.col("market_value") / total_value)
        return market_data

    def add_cumulative_sums(self, market_data: DataFrame) -> DataFrame:
        window_spec = Window.partitionBy("market_id").orderBy("day").rowsBetween(Window.unboundedPreceding, 0)
        market_data = market_data.withColumn("cumulative_market_value", F.sum("market_value").over(window_spec))
        return market_data
