import pandas as pd
import numpy as np
# Objectives

# Group all lag analysis rows by magnitute of rate cut/rate hike
# Small: 0.25 or 25 bps
# Medium: 0.5 or 50 bps
# Large: 0.75-1.0 or 75-100 bps




# We will gather results for all days
# For example we will have small_bucket_spy_day_1, small_bucket_spy_day_3, small_bucket_spy_day_7, small_bucket_spy_day_30
# For each sector, we will have 4 days for each bucket so in total we will have 12 rows for each sector
# In total, we will have 60 rows, because we have 5 sectors, and each sector will have 12 rows. 4 for each bucket


lag_analysis = pd.read_csv("../../data/processed/lag_analysis.csv")
lag_analysis['absolute_rate_change'] = lag_analysis['rate_change'].abs()


bins = [0.25, 0.51, 0.75, 1.0]

labels = ['Small', "Medium", "Large"]

lag_analysis['magnitude_bucket'] = pd.cut(lag_analysis['absolute_rate_change'], bins=bins, labels=labels)


lag_analysis.head()



def categorize_magnitude(rate_change):
    abs_change = abs(rate_change)
    if abs_change <= 0.30:
        return 'Small (0.25bp)'
    elif abs_change <= 0.55:
        return 'Medium (0.50bp)'
    else:
        return 'Large (0.75-1.00bp)'



def magnitude_effect_analysis():
    lag_analysis['magnitude_bucket'] = lag_analysis['rate_change'].apply(categorize_magnitude)

    buckets = lag_analysis['magnitude_bucket'].unique()

    sectors = ["spy", "xlk", "xlf", "xlu", "xlre"]
    days = [1, 3, 7, 30]

    lag_analysis.head()

    magnitude_effect = pd.DataFrame()

    for bucket in buckets:
        bucket_data = lag_analysis[lag_analysis['magnitude_bucket'] == bucket]
        for sector in sectors:
            for day in days:
                col_name = f"{sector}_day{day}"
                total = bucket_data.sum()
                avg_return = bucket_data[col_name].mean()
                std_dev = bucket_data[col_name].std()

                magnitude_effect = pd.concat([magnitude_effect, pd.DataFrame([{
                    'magnitude_bucket': bucket,
                    'event_count': total,
                    'sector': sector,
                    'lag_window': f"Day {day}",
                    'avg_return': round(avg_return, 2),
                    'std_dev': round(std_dev, 2)
                }])])

    key_lags = magnitude_effect[magnitude_effect['lag_window'].isin(['Day 1', 'Day 30'])]

    pivot = key_lags.pivot_table(
        index=['sector', 'lag_window'],
        columns='magnitude_bucket',
        values='avg_return',
        aggfunc='first'  # Just take the value (no aggregation needed)
    )

    pivot.to_csv('../../data/processed/magnitude_effect_summary.csv')



if __name__ == "__main__":
    magnitude_effect_analysis()

