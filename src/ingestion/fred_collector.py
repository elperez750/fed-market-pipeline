"""
FRED Data Collection Module
Fetches economic data and caches to data/raw/
"""

import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path
load_dotenv()


class FREDCollector:
    def __init__(self):
        self.fred = Fred(api_key=os.getenv('FRED_API_KEY'))
        project_root = Path(__file__).parent.parent.parent
        self.raw_data_path = project_root / 'data' / 'raw'
        self.raw_data_path.mkdir(parents=True, exist_ok=True)


    def fetch_series(self, series_id, start_date='2020-01-01', force_refresh=False):
        """
        Fetch a FRED series and cache to CSV

        Args:
            series_id: FRED series code (e.g., 'DFF', 'SP500')
            start_date: Start date for data
            force_refresh:  cache and fetch fresh data

        Returns:
            pandas Series with data
        """
        cache_file = f'{self.raw_data_path}{series_id}_{start_date}.csv'

        # Check cache first
        if not force_refresh and os.path.exists(cache_file):
            print(f"📦 Loading {series_id} from cache")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True).squeeze()

        # Fetch from API
        print(f"🌐 Fetching {series_id} from FRED API")
        data = self.fred.get_series(series_id, observation_start=start_date)

        # Save to cache
        data.to_csv(cache_file)
        print(f"💾 Saved {series_id} to {cache_file}")

        return data


    def fetch_all_core_data(self, start_date='2020-01-01'):
        """Fetch all series needed for analysis"""
        series = {
            'DFF': 'Federal Funds Rate',
            'SP500': 'S&P 500 Index',
            'DGS10': '10-Year Treasury Yield',
            'DGS2': '2-Year Treasury Yield'
        }

        data = {}
        for series_id, name in series.items():
            data[series_id] = self.fetch_series(series_id, start_date)

        return data


if __name__ == '__main__':
    # Test the collector
    collector = FREDCollector()
    data = collector.fetch_all_core_data()
    print(f"\n✅ Fetched {len(data)} series")
    for series_id, series_data in data.items():
        print(f"  {series_id}: {len(series_data)} observations")