# Federal Reserve Policy → Market Impact Analysis

A data engineering project analyzing how Federal Reserve monetary policy decisions impact financial markets over time.

## 🎯 Project Goals

### Primary Research Question
**Do markets react immediately to Fed rate changes, or is there a measurable lag?**

Specifically investigating:
- Correlation between Fed rate changes and S&P 500 movements
- Time lag between FOMC announcements and full market reactions (Day 0 vs Day 1, 3, 7, 30)
- Sector-specific responses (Technology vs Financials vs Utilities vs Real Estate)
- Whether reaction patterns differ between rate hikes and cuts
- Impact magnitude: Does a 0.75% hike hurt more than three 0.25% hikes?

### Secondary Goals
- Build production-grade data engineering pipeline (ingestion → transformation → analysis)
- Demonstrate financial domain knowledge for fintech/quant roles
- Practice modern data stack: Python, pandas, data warehousing patterns
- Create portfolio piece showing end-to-end data product development

---

## 📚 What I'm Learning

### Data Engineering
- **API Integration**: Working with FRED API and Yahoo Finance to collect economic/market data
- **Data Caching**: Implementing efficient caching strategies to avoid redundant API calls
- **ETL Pipelines**: Extract (APIs) → Transform (pandas) → Load (CSV/potential Snowflake)
- **Data Quality**: Handling missing data, weekend gaps, and data validation
- **Path Management**: Using pathlib for robust, cross-platform file handling

### Financial/Economic Concepts
- **Monetary Policy**: How the Federal Reserve uses interest rates to control inflation and employment
- **Market Mechanics**: Understanding why stock prices react to rate changes
- **Yield Curves**: 2-year vs 10-year Treasury spreads as recession indicators
- **Sector Sensitivity**: Why tech stocks fall harder than utilities during rate hikes
- **Lag Effects**: Behavioral finance vs efficient market hypothesis

### Python/Data Science
- **Pandas**: Time series manipulation, date indexing, rolling calculations
- **Data Modeling**: Structuring datasets for analysis (fact tables, event identification)
- **Statistical Analysis**: Correlation analysis, cumulative returns, lag correlation
- **Code Organization**: Modular design with collectors, transformers, analyzers

---

## 🔍 Expected Insights

By the end of this project, I'll be able to answer:

1. **"What's the average S&P 500 reaction to a 0.25% rate hike?"**
   - Example: "-1.8% over 7 days with 60% occurring in first 2 days"

2. **"Which sectors overreact vs underreact?"**
   - Example: "Tech (XLK) shows 2.3x amplification, Financials (XLF) show 0.6x dampening"

3. **"Is there a consistent lag pattern?"**
   - Example: "Markets show delayed reaction with peak impact occurring Day 3, suggesting gradual position adjustments"

4. **"Do rate cuts work differently than hikes?"**
   - Example: "Cuts show immediate +2% pop but fade to +0.5% by Day 30, while hikes show sustained -1.5% impact"

---

## 📊 Data Sources

- **FRED API**: Federal Funds Rate, S&P 500 Index, Treasury Yields, CPI
- **Yahoo Finance**: ETF pricing data (SPY, XLK, XLF, XLU, XLRE)
- **Time Period**: 2020-2025 (covers COVID emergency cuts, 2022 inflation fight, 2024-25 normalization)

---

## 🛠️ Tech Stack

**Data Collection**
- Python 3.x
- `fredapi` - Federal Reserve Economic Data
- `yfinance` - Market data
- `pandas` - Data manipulation

**Data Storage**
- CSV (current)
- Snowflake (planned)

**Analysis & Visualization**
- Statistical analysis (correlations, lag effects)
- Streamlit dashboard (planned)
- Plotly/Matplotlib visualizations

**Development**
- Git version control
- Modular Python architecture
- pathlib for cross-platform compatibility

---

## 📁 Project Structure
```
fed-market-pipeline/
├── data/
│   ├── raw/              # Cached API responses
│   ├── staging/          # Cleaned, unified dataset
│   └── processed/        # Analysis-ready outputs
├── src/
│   ├── ingestion/        # API collectors (FRED, Yahoo Finance)
│   ├── transformation/   # Data cleaning and combination
│   ├── analysis/         # Event identification, lag analysis
│   └── utils/            # Shared utilities (data loading)
└── README.md
```

---

## 🎓 Why This Project Matters for My Career

**For Data Engineering Roles:**
- Demonstrates real-world ETL pipeline development
- Shows understanding of data quality, caching, and optimization
- Proves ability to work with financial APIs and time-series data

**For Fintech/Quant Roles (Point72, Citizens, Bloomberg):**
- Combines technical skills with financial domain knowledge
- Shows initiative in exploring market microstructure
- Relevant to portfolio management, risk analysis, and trading strategies

**Interview Talking Points:**
- "I built a pipeline analyzing 20+ years of Fed data to quantify market reaction lag"
- "Found statistically significant patterns in how different sectors absorb rate changes"
- "Discovered X-day lag between FOMC announcements and full market adjustment"

---

## 🚀 Current Status

**Completed:**
- ✅ Data ingestion pipeline with caching
- ✅ Master dataset creation (Fed rates + market data)
- ✅ Event identification (19 significant Fed rate changes)
- ✅ Data quality fixes (weekend gaps, missing values)

**In Progress:**
- 🔄 Forward return calculation (lag analysis)
- 🔄 Statistical correlation analysis

**Planned:**
- ⏳ Sector-by-sector comparison
- ⏳ Interactive Streamlit dashboard
- ⏳ Snowflake integration (optional)
- ⏳ Automated data refresh pipeline

---

## 📖 Learning Resources Used

- Ray Dalio: "How The Economic Machine Works"
- Investopedia: Federal Reserve & Monetary Policy
- Khan Academy: Money & Banking series
- FRED API Documentation
- Pandas time-series documentation

---

## 👤 Author

**Sway** - CS Student @ Central Washington University  
Pursuing data engineering internships for Summer 2026

*This project demonstrates my ability to combine technical data engineering skills with financial domain knowledge to extract actionable insights from complex datasets.*
