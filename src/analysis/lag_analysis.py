import pandas as pd
import sys
from pathlib import Path

# Add src/ to Python's search path
sys.path.insert(0, str(Path(__file__).parent.parent))
project_root = Path(__file__).parent.parent.parent


from utils.data_loader import load_csv


# Load fed events and master dataset
fed_events = load_csv("data/processed/fed_events.csv")
master_dataset = load_csv("data/staging/master_dataset.csv")
markets = ['spy', 'xlk', 'xlf', 'xlu', 'xlre']


def get_lag_analysis(fed_events, master_dataset):

    # Use event dates as the index.
    event_dates = fed_events.index



    lag_analysis = pd.DataFrame(index=event_dates)

    # Copy rate change, rate hike, and rate drop from fed events.
    lag_analysis['date'] = event_dates
    lag_analysis['rate_change'] = fed_events['rate_change']
    lag_analysis['rate_hike'] = fed_events['rate_hike']
    lag_analysis['rate_cut'] = fed_events['rate_cut']


    for date in event_dates:
        # Get base index for offsets
        event_idx = master_dataset.index.get_loc(date)


        # Our tickers are spy, xlk, xlf, xlu, xlre
        for ticker in markets:

            # Get the closing price for the ticker at the specific date.
            # For example, this would be March 4, 2020, March 16, 2020 etc.
            current_day_close = master_dataset.iloc[event_idx][f'{ticker}_close']

            # Day 0 is always 0 by definition
            lag_analysis.loc[date, f'{ticker}_day0'] = 0.0

            # Calculate other lags with bounds checking
            for lag_days, col_name in [(1, 'day1'), (3, 'day3'), (7, 'day7'), (30, 'day30')]:
                forward_idx = event_idx + lag_days


                if forward_idx >= len(master_dataset):
                    lag_analysis.loc[date, f'{ticker}_{col_name}'] = None
                else:
                    # Get the closing price at the current day, which could be 1, 3, 7, 30
                    future_close = master_dataset.iloc[forward_idx][f'{ticker}_close']

                    # Calculate the return from the current day to the day 1 day out, 3 days out, 7 days out, and 30 days out
                    pct_return = ((future_close - current_day_close) / current_day_close) * 100


                    # Create column where the specific date is
                    # Example columns would be SPY_day1, XLRE_day30
                    # These have the amount that the stock changes from the current date.
                    lag_analysis.loc[date, f'{ticker}_{col_name}'] = pct_return


    # We dropped duplicate date
    lag_analysis = lag_analysis.drop(columns=['date'])

    # Round all numbers to 2 decimal points
    lag_analysis = lag_analysis.round(2)

    lag_analysis.to_csv('../../data/processed/lag_analysis.csv')






if __name__ == "__main__":
    get_lag_analysis(fed_events, master_dataset)