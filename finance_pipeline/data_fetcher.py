import yfinance as yf
import pandas as pd
from typing import List
from dataclasses import dataclass, field
from datetime import timedelta

@dataclass
class FetchConfig:
    symbols: List[str] = field(default_factory=lambda: ["AAPL", "GOOG"])
    start: str = "2022-01-01"
    end: str = "2022-12-31"


def fetch_data(config: FetchConfig) -> pd.DataFrame:
    """Fetch historical data for the configured symbols from yfinance."""
    frames = []
    for symbol in config.symbols:
        ticker = yf.Ticker(symbol)
        try:
            start_dt = pd.to_datetime(config.start) - timedelta(days=30)
            start_str = start_dt.strftime("%Y-%m-%d")
            hist = ticker.history(start=start_str, end=config.end)
        except Exception as exc:
            print(f"Failed to fetch data for {symbol}: {exc}")
            continue
        if hist.empty:
            print(f"No data returned for {symbol}")
            continue
        hist["symbol"] = symbol
        frames.append(hist)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames)
