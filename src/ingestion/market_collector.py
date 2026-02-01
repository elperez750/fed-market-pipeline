"""
Market Data Collection Module
Fetches stock/ETF data from Yahoo Finance
"""
from pathlib import Path

import yfinance as yf
import pandas as pd
import os


class MarketCollector:
    def __init__(self):
        project_root = Path(__file__).parent.parent.parent
        self.raw_data_path = project_root / 'data' / 'raw'



    def fetch_ticker(self, ticker, start_date='2020-01-01', force_refresh=False):
        """
        Fetch ticker data and cache to CSV

        Args:
            ticker: Stock/ETF symbol (e.g., 'SPY', 'XLK')
            start_date: Start date
            force_refresh: Ignore cache

        Returns:
            pandas DataFrame with OHLC data
        """
        cache_file = f'{self.raw_data_path}{ticker}_{start_date}.csv'

        if not force_refresh and os.path.exists(cache_file):
            print(f"📦 Loading {ticker} from cache")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True).squeeze()

        print(f"🌐 Fetching {ticker} from Yahoo Finance")
        data = yf.download(ticker, start=start_date, progress=False)

        data.to_csv(cache_file)
        print(f"💾 Saved {ticker} to {cache_file}")

        return data

    def fetch_all_etfs(self, start_date='2020-01-01'):
        """Fetch sector ETFs for analysis"""
        tickers = {
            'SPY': 'S&P 500 ETF',
            'XLK': 'Technology Sector',
            'XLF': 'Financial Sector',
            'XLU': 'Utilities Sector',
            'XLRE': 'Real Estate Sector'
        }

        data = {}

        """
        data = {
            SPY: Dataframe with all information{}
            XLK: Dataframe with all information{}
            XLF: Dataframe with all information{}
            XLU: Dataframe with all information{}
            XLRE: Dataframe with all information{}
        
        }
        """
        for ticker, name in tickers.items():
            data[ticker] = self.fetch_ticker(ticker, start_date)

        return data


if __name__ == '__main__':
    collector = MarketCollector()
    data = collector.fetch_all_etfs()
    print(f"\n✅ Fetched {len(data)} tickers")