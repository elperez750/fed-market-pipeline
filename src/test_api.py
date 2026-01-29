# src/quick_visual_interactive.py
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fredapi import Fred
from dotenv import load_dotenv
import os

load_dotenv()
fred = Fred(api_key=os.getenv('FRED_API_KEY'))

# Get data
fed_rate = fred.get_series('DFF', observation_start='2020-01-01')
sp500 = fred.get_series('SP500', observation_start='2020-01-01')
gdp = fred.get_series('GDP', observation_start='2020-01-01')


gdp_df = pd.DataFrame({
    "date": gdp.index,
    "gdp": gdp.values
})


gdp_df["gdp_trillion"] = gdp_df["gdp"] / 1000
first_five = gdp_df["gdp_trillion"][:5]


print(first_five)

# Create subplots



fig = make_subplots(
    rows=3, cols=1,
    subplot_titles=('Federal Funds Rate (2020-2025)', 'S&P 500 Index (2020-2025)', 'GDP (2020-2025)'),
    vertical_spacing=0.2
)

# Add Fed rate trace
fig.add_trace(
    go.Scatter(
        x=fed_rate.index,
        y=fed_rate.values,
        mode='lines',
        name='Fed Funds Rate',
        line=dict(color='red', width=2),
        hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Rate:</b> %{y:.2f}%<extra></extra>'
    ),
    row=1, col=1
)

# Add S&P 500 trace
fig.add_trace(
    go.Scatter(
        x=sp500.index,
        y=sp500.values,
        mode='lines',
        name='S&P 500',
        line=dict(color='green', width=2),
        hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Value:</b> %{y:.2f}<extra></extra>'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x = gdp_df['date'],
        y = gdp_df['gdp_trillion'],
        mode='lines',
        name='GDP Index',
        line=dict(color='blue', width=2),
        hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Value:</b> %{y:.2f}<extra></extra>'
    ),
    row=3, col=1
)

# Update layout
fig.update_xaxes(title_text="Date", row=3, col=1)
fig.update_yaxes(title_text="Rate (%)", row=1, col=1)
fig.update_yaxes(title_text="Index Value", row=2, col=1)
fig.update_yaxes(title_text="GDP Index (Trillions)", row=3, col=1)

fig.update_layout(
    height=800,
    width=1400,
    showlegend=False,
    hovermode='x unified'  # Shows values for both plots at same x position
)

# Save as HTML (can open in browser later)
 # fig.write_html('visualizations/fed_vs_market_interactive.html')
print("📊 Interactive chart saved to visualizations/fed_vs_market_interactive.html")

# Show in browser
fig.show()
