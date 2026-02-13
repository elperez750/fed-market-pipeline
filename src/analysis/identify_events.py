import sys
from pathlib import Path

# Add src/ to Python's search path
sys.path.insert(0, str(Path(__file__).parent.parent))
project_root = Path(__file__).parent.parent.parent


import pandas as pd
from utils.data_loader import load_csv


def identify_rate_events():
    # Load from the master data
    df = load_csv("data/staging/master_data.csv")
    output_path = '../../data/processed/fed_events.csv'


    # Get a data set where we only have fed events.
    # A fed event is constituted as a rate hike or rate cut of 10 basis points or more
    events = df[abs(df['rate_change']) >= 0.10].copy()


    events.to_csv(output_path)

    return events





if __name__ == '__main__':
    df = identify_rate_events()