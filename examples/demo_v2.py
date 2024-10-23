from src.beyond_bets.datasets.bets_dataset import FileBasedBetsDataset
from src.beyond_bets.datasets.market_dataset import ApiBasedMarketDataset
from src.beyond_bets.transforms.player_hourly_transform import PlayerHourlyTransform
from src.beyond_bets.transforms.market_daily_transform import MarketDailyTransform
from src.beyond_bets.transforms.player_market_daily_transform import PlayerMarketDailyTransform
from src.beyond_bets.transforms.top_players_transform import TopPlayersTransform
from src.beyond_bets.transforms.bet_grader_transform import BetGraderTransform

def main():
    # Instantiate file-based data source for bets
    file_bets_dataset = FileBasedBetsDataset()

    # Use PlayerHourly transform
    player_hourly_transform = PlayerHourlyTransform(file_bets_dataset)
    player_hourly_result = player_hourly_transform.transform()
    print("PlayerHourly result:", player_hourly_result.show())

    # Instantiate API-based data source for market
    api_market_dataset = ApiBasedMarketDataset()

    # Use MarketDaily transform
    market_daily_transform = MarketDailyTransform(api_market_dataset)
    market_daily_result = market_daily_transform.transform()
    print("MarketDaily result:", market_daily_result.show())

    # Use PlayerMarketDaily transform
    player_market_daily_transform = PlayerMarketDailyTransform(file_bets_dataset, api_market_dataset)
    player_market_daily_result = player_market_daily_transform.transform()
    print("PlayerMarketDaily result:", player_market_daily_result.show())

    # Use TopPlayers transform
    top_players_transform = TopPlayersTransform(file_bets_dataset)
    top_players_result = top_players_transform.transform()
    print("TopPlayers result:", top_players_result.show())

    # Use BetGrader transform
    bet_grader_transform = BetGraderTransform(file_bets_dataset)
    bet_grader_result = bet_grader_transform.transform()
    print("BetGrader result:", bet_grader_result.show())

if __name__ == "__main__":
    main()
