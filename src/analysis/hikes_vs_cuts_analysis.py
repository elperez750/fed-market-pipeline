import sys
from pathlib import Path
import pandas as pd

# Add src/ to Python's search path
sys.path.insert(0, str(Path(__file__).parent.parent))
project_root = Path(__file__).parent.parent.parent
from utils.data_loader import load_csv


def compare_hikes_vs_cuts():

    # Load lag analysis csv
    lag_analysis = load_csv(project_root / 'data' / 'processed' / 'lag_analysis.csv')


    # Grab all rows where rate hikes are true and rate cuts are true.
    # We separate both since we want to know how much our sectors went up or down after one of these events.
    rate_hikes = lag_analysis[lag_analysis['rate_hike'] == True]
    rate_cuts = lag_analysis[lag_analysis['rate_cut'] == True ]


    # Do the same thing as above except we exclude the two 2020 dates the FED lowered interest rates.
    rate_hikes_no_covid = lag_analysis[lag_analysis['rate_hike'] == True & ~lag_analysis.index.isin(pd.to_datetime(['2020-03-04', '2020-03-16']))]
    rate_cuts_no_covid = lag_analysis[lag_analysis['rate_cut'] == True & ~lag_analysis.index.isin(pd.to_datetime(['2020-03-04', '2020-03-16']))]

    markets = ['spy', 'xlk', 'xlf', 'xlu', 'xlre']

    results = []
    results_no_covid = []
    for ticker in markets:
        for lag in ['day1', 'day3', 'day7', 'day30']:
            col = f'{ticker}_{lag}'


            # Get the average rate hike and rate drop
            hike_avg = rate_hikes[col].mean()
            cuts_avg = rate_cuts[col].mean()



            # Get the average rate hike and rate drop excluding early covid dates
            # Doing this to not skew main results. Covid was an outlier were the FED cut rates by 100 basis points
            hikes_no_covid = rate_hikes_no_covid[col].mean()
            cuts_no_covid = rate_cuts_no_covid[col].mean()


            # Aggregates the results including covid
            results.append({
                'sector': ticker,
                'lag': lag,
                'hike_avg': round(hike_avg,2),
                'cuts_avg': round(cuts_avg,2)
            })



            # Aggregates the results not including covid
            results_no_covid.append({
                'sector': ticker,
                'lag': lag,
                'hike_avg': round(hikes_no_covid,2),
                'cuts_avg': round(cuts_no_covid,2)
            })


    hike_vs_cuts = pd.DataFrame(results)
    hikes_vs_cuts_no_covid = pd.DataFrame(results_no_covid)

    hike_vs_cuts.to_csv('../../data/processed/hike_vs_cuts.csv')
    hikes_vs_cuts_no_covid.to_csv('../../data/processed/hikes_vs_cuts_no_covid.csv')
    print("✓ Hikes vs cuts saved to data/processed/hike_vs_cuts.csv")
    print("✓ Hikes vs cuts not in covid saved to data/processed/hike_vs_cuts.csv")





if __name__ == "__main__":
    compare_hikes_vs_cuts()


