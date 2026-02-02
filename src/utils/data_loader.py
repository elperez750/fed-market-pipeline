from pathlib import Path
import pandas as pd


def load_csv(relative_path):
    """
    Load the master dataset with all historical data

    Returns:
        pandas DataFrame with dates as index
    """

    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent
    file_path = project_root / relative_path

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"\n❌ Master dataset not found at:\n   {file_path}\n"
            f"💡 Run 'python src/transformation/create_master_dataset.py' first!\n"
        )

    print(f"📦 Loading master dataset from: {file_path.name}")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    print(f"✅ Loaded {len(df)} days of data ({df.index.min().date()} to {df.index.max().date()})")

    return df