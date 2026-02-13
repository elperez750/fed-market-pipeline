import pandas as pd
import sys
from pathlib import Path

# Add src/ to Python's search path
sys.path.insert(0, str(Path(__file__).parent.parent))
project_root = Path(__file__).parent.parent.parent


from utils.data_loader import load_csv

lag_analysis = load_csv("data/processed/lag_analysis.csv")
markets = ['spy', 'xlk', 'xlf', 'xlu', 'xlre']


# The goal of this function is to figure out what percentage of the day 30 final move happens by day 1, day 3, and day 7
def get_sector_reactions(lag_analysis):
    '''

    :param lag_analysis:
    :return:
    '''


    sector_reactions = pd.DataFrame(index=lag_analysis.index)
    # Create a df for sector reactions with initial covid FED events, and without the covid FED events
    sector_reactions_summary = pd.DataFrame()
    sector_reactions_summary_no_covid = pd.DataFrame()

    # Copy rate hike and rate cut columns from lag analysis.
    sector_reactions['rate_hike'] = lag_analysis['rate_hike']
    sector_reactions['rate_cut'] = lag_analysis['rate_cut']

    for ticker in markets:
        # Get the amount the sectors changes after all days
        day_one = lag_analysis[f'{ticker}_day1']
        day_three = lag_analysis[f'{ticker}_day3']
        day_seven = lag_analysis[f'{ticker}_day7']
        day_thirty = lag_analysis[f'{ticker}_day30']


        # What percentage of the 30 day final move happens on day 1?
        sector_reactions[f'{ticker}_day1_reaction_speed'] = (abs(day_one) / abs(day_thirty)) * 100

        # What percentage of the 30 day final move happens on day 3?
        sector_reactions[f'{ticker}_day3_reaction_speed'] = (abs(day_three) / abs(day_thirty)) * 100

        # What percentage of the 30 day final move happens on day 7?
        sector_reactions[f'{ticker}_day7_reaction_speed'] = (abs(day_seven) / abs(day_thirty)) * 100



    # Removing the fed events during covid, which are March 4, 2020 and March 17 2020
    sector_reactions_no_covid = sector_reactions[~sector_reactions.index.isin(pd.to_datetime(['2020-03-04', '2020-03-16']))]


    for ticker in markets:
        for lag in ['day1', 'day3', 'day7']:
            col = f'{ticker}_{lag}_reaction_speed'
            sector_reactions_summary = pd.concat([sector_reactions_summary, pd.DataFrame([{
                'sector': ticker.upper(),
                'lag': lag,
                'avg_reaction_speed': round(sector_reactions[col].mean(), 2)
            }])], ignore_index=True)

            sector_reactions_summary_no_covid  = pd.concat([sector_reactions_summary_no_covid, pd.DataFrame([{
                'sector': ticker.upper(),
                'lag': lag,
                'avg_reaction_speed': round(sector_reactions_no_covid[col].mean(), 2)
            }])], ignore_index=True)




    sector_reactions.to_csv('../../data/processed/sector_reaction_speeds.csv')
    print("✓ Per-event reaction speeds saved to data/processed/sector_reaction_speeds.csv")

    sector_reactions_summary.to_csv('../../data/processed/sector_reaction_speeds_summary.csv')
    print("✓ Summary averages saved to data/processed/sector_reaction_speeds_summary.csv")
    sector_reactions_summary_no_covid.to_csv("../../data/processed/sector_reaction_speeds_no_covid.csv")
    print("✓ Summary averages saved to data/processed/sector_reaction_speeds_summary_no_covid.csv")




if __name__ == '__main__':
    get_sector_reactions(lag_analysis)
