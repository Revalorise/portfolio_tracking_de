"""Generate stock data by providing a ticker, start_date, and end_date."""
from pathlib import Path

import pandas as pd
import yfinance as yf
from google.cloud import storage


class StockDataManager:

    credentials = '../gcp_project_key.json'
    storage_client = storage.Client.from_service_account_json(credentials)
    bucket = storage_client.get_bucket('portfolio_tracking_de')

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def _get_data(self) -> pd.DataFrame:
        """
        Get stock data based on instantiated ticker, start_date, and end_date.
        Returns: dataframe of stock data
        """
        data = yf.download(
            self.ticker,
            period="max"
        )

        return pd.DataFrame(data)

    def save_data(self) -> None:
        """
        Save stock data to a csv file.
        Args:
            data: dataframe of stock data
        """
        file = Path(f"../data/{self.ticker}_data.csv")

        if file.exists():
            print(f"{file} already exists... skipping..")
        else:
            data = self._get_data()
            data.to_csv(f"../data/{self.ticker}_data.csv")

    def load_to_gcs(self, file: str) -> None:
        """
        Load data from data folder to Google Cloud Storage, existing data will be skipped.
        Args:
            file: file path of data
        """
        file_name = file.split("/")[2]
        print(f"Uploading {file_name} to Google Cloud Storage...")
        blob = self.bucket.blob(file_name)

        if self.bucket.blob(file_name).exists():
            print(f"{file_name} already exist in Google Cloud Storage... skipping..")
            pass
        else:
            blob.upload_from_filename(file)

        print(f"{file_name} uploaded successfully!")


if __name__ == "__main__":
    apple_data = StockDataManager("AAPL")
    nvidia_data = StockDataManager("NVDA")
    tesla_data = StockDataManager("TSLA")
    amazon_data = StockDataManager("AMZN")
    amd_data = StockDataManager("AMD")

    for data in [apple_data, nvidia_data, tesla_data, amazon_data, amd_data]:
        data.save_data()
        data.load_to_gcs(f"../data/{data.ticker}_data.csv")
