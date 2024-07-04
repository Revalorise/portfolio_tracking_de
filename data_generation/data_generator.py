"""Generate stock data by providing a ticker, start_date, and end_date."""
from pathlib import Path

import pandas as pd
import yfinance as yf


class StockDataGenerator:
    def __init__(self, ticker: str, start_date: str, end_date: str) -> None:
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def _get_data(self) -> pd.DataFrame:
        """
        Get stock data based on instantiated ticker, start_date, and end_date.
        Returns: dataframe of stock data
        """
        data = yf.download(
            self.ticker,
            start=self.start_date,
            end=self.end_date
        )

        return pd.DataFrame(data)

    def save_data(self) -> None:
        """
        Save stock data to a csv file.
        Args:
            data: dataframe of stock data
        """
        file = Path(f"../data/{self.ticker}_{self.start_date}_{self.end_date}.csv")

        if file.exists():
            print(f"{file} already exists... skipping..")
        else:
            data = self._get_data()
            data.to_csv(f"../data/{self.ticker}_{self.start_date}_{self.end_date}.csv")


if __name__ == "__main__":
    apple_data = StockDataGenerator("AAPL", "2011-01-01", "2021-12-31")
    nvidia_data = StockDataGenerator("NVDA", "2011-01-01", "2021-12-31")
    tesla_data = StockDataGenerator("TSLA", "2011-01-01", "2021-12-31")
    amazon_data = StockDataGenerator("AMZN", "2011-01-01", "2021-12-31")
    amd_data = StockDataGenerator("AMD", "2011-01-01", "2021-12-31")

    for data in [apple_data, nvidia_data, tesla_data, amazon_data, amd_data]:
        data.save_data()
