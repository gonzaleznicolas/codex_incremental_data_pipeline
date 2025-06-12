import pandas as pd
from sqlalchemy import insert, select
from sqlalchemy.engine import Engine
from .data_fetcher import FetchConfig, fetch_data
from .database import get_engine, stocks


def compute_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Sort data and compute the price divided by the 30-day moving average.

    yfinance returns columns capitalized (e.g. ``Close``). To keep the
    database schema simple we normalise all column names to lowercase before
    calculating the indicator.
    """

    # Normalise columns: lowercase and replace spaces with underscores
    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_")).sort_index()
    df.index = pd.to_datetime(df.index).tz_localize(None)

    # Calculate 30-day moving average on the closing price and derive ratio
    ma30 = df["close"].rolling(window=30).mean()
    df["price_over_ma30"] = df["close"] / ma30
    return df


def load_to_db(df: pd.DataFrame, engine: Engine | None = None) -> None:
    engine = engine or get_engine()
    with engine.begin() as conn:
        existing = {row.symbol: row.id for row in conn.execute(select(stocks))}
        for symbol in df["symbol"].unique():
            if symbol not in existing:
                result = conn.execute(insert(stocks).values(symbol=symbol))
                existing[symbol] = result.inserted_primary_key[0]
        df = df.copy()
        df["stock_id"] = df["symbol"].map(existing)
        df = df.drop(columns=["symbol"])
        df.to_sql("prices", conn, if_exists="append", index_label="date")


def run_pipeline(config: FetchConfig = FetchConfig()) -> None:
    data = fetch_data(config)
    if data.empty:
        print("No data fetched")
        return
    data = compute_moving_averages(data)
    data = data.loc[pd.to_datetime(config.start): pd.to_datetime(config.end)]
    load_to_db(data)


if __name__ == "__main__":
    run_pipeline()
