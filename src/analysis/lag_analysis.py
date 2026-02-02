import pandas as pd
import sys
from pathlib import Path

# Add src/ to Python's search path
sys.path.insert(0, str(Path(__file__).parent.parent))
project_root = Path(__file__).parent.parent.parent


from utils.data_loader import load_csv

fed_events = load_csv("data/processed/fed_events.csv")
master_dataset = load_csv("data/staging/master_dataset.csv")
markets = ['spy', 'xlk', 'xlf', 'xlu', 'xlre']


def get_lag_analysis(fed_events, master_dataset):
    event_dates = fed_events.index



    lag_analysis = pd.DataFrame(index=event_dates)

    lag_analysis['date'] = event_dates
    lag_analysis['rate_change'] = fed_events['rate_change']
    lag_analysis['rate_hike'] = fed_events['rate_hike']
    lag_analysis['rate_cut'] = fed_events['rate_cut']

    for date in event_dates:
        # Get base index for offsets
        event_idx = master_dataset.index.get_loc(date)



        for ticker in markets:
            current_day_close = master_dataset.iloc[event_idx][f'{ticker}_close']

            # Day 0 is always 0 by definition
            lag_analysis.loc[date, f'{ticker}_day0'] = 0.0

            # Calculate other lags with bounds checking
            for lag_days, col_name in [(1, 'day1'), (3, 'day3'), (7, 'day7'), (30, 'day30')]:
                forward_idx = event_idx + lag_days

                if forward_idx >= len(master_dataset):
                    lag_analysis.loc[date, f'{ticker}_{col_name}'] = None
                else:
                    future_close = master_dataset.iloc[forward_idx][f'{ticker}_close']
                    pct_return = ((future_close - current_day_close) / current_day_close) * 100
                    lag_analysis.loc[date, f'{ticker}_{col_name}'] = pct_return



    lag_analysis = lag_analysis.drop(columns=['date'])
    lag_analysis = lag_analysis.round(2)

    lag_analysis.to_csv('../../data/processed/lag_analysis.csv')






if __name__ == "__main__":
    get_lag_analysis(fed_events, master_dataset)