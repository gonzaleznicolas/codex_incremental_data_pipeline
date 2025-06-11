import pandas as pd
from sqlalchemy.engine import Engine
from .data_fetcher import FetchConfig, fetch_data
from .database import get_engine


def compute_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Sort data and compute moving averages.

    yfinance returns columns capitalized (e.g. ``Close``). To keep the
    database schema simple we normalise all column names to lowercase before
    calculating the moving averages.
    """

    # Normalise columns: lowercase and replace spaces with underscores
    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_")).sort_index()

    # Calculate moving averages on the closing price
    df["ma7"] = df["close"].rolling(window=7).mean()
    df["ma30"] = df["close"].rolling(window=30).mean()
    return df


def load_to_db(df: pd.DataFrame, engine: Engine | None = None) -> None:
    engine = engine or get_engine()
    df.to_sql("prices", engine, if_exists="append", index_label="date")


def run_pipeline(config: FetchConfig = FetchConfig()) -> None:
    data = fetch_data(config)
    if data.empty:
        print("No data fetched")
        return
    data = compute_moving_averages(data)
    load_to_db(data)


if __name__ == "__main__":
    run_pipeline()
