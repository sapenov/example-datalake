from beyond_bets.datasets.bets_dataset import FileBasedBetsDataset
from beyond_bets.datasets.market_dataset import ApiBasedMarketDataset
from beyond_bets.transforms.player_hourly_transform import PlayerHourlyTransform
from beyond_bets.transforms.market_daily_transform import MarketDailyTransform
from beyond_bets.transforms.player_market_daily_transform import PlayerMarketDailyTransform
from beyond_bets.transforms.top_players_transform import TopPlayersTransform
from beyond_bets.transforms.bet_grader_transform import BetGraderTransform
from pyspark.sql import SparkSession
import os


def main():

    # some config that should be done in setup
    os.environ["PYSPARK_PYTHON"] = r"C:\Users\Khazret\PycharmProjects\bbets\venv\Scripts\python.exe"
    os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\Khazret\PycharmProjects\bbets\venv\Scripts\python.exe"
    os.environ["HADOOP_HOME"] = r"C:\hadoop"

    # Initialize SparkSession
    spark = SparkSession.builder.master("local[*]").appName("BeyondBetsDemo").getOrCreate()

    # Instantiate file-based data source for bets
    file_bets_dataset = FileBasedBetsDataset(spark)

    # Use PlayerHourly transform
    player_hourly_transform = PlayerHourlyTransform(file_bets_dataset)
    player_hourly_transform.transform()

    # Instantiate API-based data source for market
    api_market_dataset = ApiBasedMarketDataset(file_bets_dataset)

    # Use MarketDaily transform
    market_daily_transform = MarketDailyTransform(api_market_dataset)
    market_daily_transform.transform()

    # Use PlayerMarketDaily transform
    player_market_daily_transform = PlayerMarketDailyTransform(file_bets_dataset, api_market_dataset)
    player_market_daily_transform.transform()

    # Use TopPlayers transform
    top_players_transform = TopPlayersTransform(file_bets_dataset)
    top_players_transform.transform()

    # Use BetGrader transform
    bet_grader_transform = BetGraderTransform(file_bets_dataset)
    bet_grader_transform.transform()


if __name__ == "__main__":
    main()
