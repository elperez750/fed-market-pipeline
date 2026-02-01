"""
Master Dataset Builder
Combines FRED + Market data into unified analysis dataset
"""

import pandas as pd
import sys
sys.path.append("../")


from ingestion.fred_collector import FREDCollector
from ingestion.market_collector import MarketCollector



def calculate_returns(prices):
    """Calculate daily percentage returns"""
    return prices.pct_change() * 100


def create_master_dataset(start_date="2020-01-01"):
    """
    Build unified dataset with all metricst alligned with date
    :param start_date:
    :return:
    """

    fred = FREDCollector()
    market = MarketCollector()


    fred_data = fred.fetch_all_core_data(start_date=start_date)
    market_data = market.fetch_all_etfs(start_date=start_date)


    print(fred_data['DFF'])

    df = pd.DataFrame(index=fred_data["DFF"].index)  # Use DFF's dates as index

    df['fed_rate'] = fred_data["DFF"]
    df['sp500_index'] = fred_data["SP500"]
    df['treasury_10y'] = fred_data["DGS10"]
    df['treasury_2y'] = fred_data["DGS2"]

    df["yield_curve"] = df["treasury_10y"] - df["treasury_2y"]


    markets = ['SPY', 'XLK', 'XLF', 'XLU', 'XLRE']

    for ticker in markets:
        df[f'{ticker.lower()}_close'] = market_data[ticker]['Close']

    for ticker in markets:
        df[f'{ticker.lower()}_return'] = calculate_returns(df[f'{ticker.lower()}_close'])


    for market in markets:
        ticker = market.lower()
        df.loc['2020-03-16', f'{ticker}_return'] = (
                (df.loc['2020-03-16', f'{ticker}_close'] - df.loc['2020-03-13', f'{ticker}_close'])
                / df.loc['2020-03-13', f'{ticker}_close'] * 100
        )





    df['rate_change'] = df['fed_rate'].diff()
    df['rate_hike'] = df['rate_change'] > 0
    df['rate_cut'] = df['rate_change'] < 0

    df = df.dropna(subset=['spy_close'])

    output_path = '../../data/staging/master_dataset.csv'
    df.index.name = 'date'

    df.to_csv(output_path)

    print(f"\n✅ Master dataset created: {output_path}")
    print(f"📊 Shape: {df.shape}")
    print(f"📅 Date range: {df.index.min()} to {df.index.max()}")
    print(f"\n🔍 Sample:")
    print(df.head())

    return df


if __name__ == '__main__':
    df = create_master_dataset()


