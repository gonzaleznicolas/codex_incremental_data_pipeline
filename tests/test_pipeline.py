import pandas as pd
from finance_pipeline.main import compute_indicators_and_suggested_positions, load_to_db
from finance_pipeline.data_fetcher import FetchConfig, fetch_data
from finance_pipeline.database import get_engine
from sqlalchemy import inspect
from unittest import mock


def test_compute_indicators_and_suggested_positions():
    data = pd.DataFrame({'close': [1]*30 + [2]})
    result = compute_indicators_and_suggested_positions(data)
    ma30 = pd.Series(data['close']).rolling(30).mean()
    expected_ratio = data['close'] / ma30
    expected_ratio.index = result.index
    pd.testing.assert_series_equal(result['price_over_ma30'], expected_ratio, check_names=False)
    std30 = pd.Series(data['close']).rolling(30).std()
    upper = ma30 + 2 * std30
    lower = ma30 - 2 * std30
    expected_bb = (data['close'] - lower) / (upper - lower)
    expected_bb.index = result.index
    pd.testing.assert_series_equal(result['bb_pct'], expected_bb, check_names=False)
    assert result.loc[result.index[29], 'suggested_position'] == 'Cash'
    assert result.loc[result.index[30], 'suggested_position'] == 'Long'


def test_fetch_data():
    sample = pd.DataFrame({
        'close': [1,2,3],
        'open': [1,2,3],
        'high': [1,2,3],
        'low': [1,2,3],
        'volume': [100,100,100],
        'dividends': [0,0,0],
        'stock_splits': [0,0,0]
    }, index=pd.date_range('2022-01-03', periods=3))
    with mock.patch('yfinance.Ticker') as MockTicker:
        instance = MockTicker.return_value
        instance.history.return_value = sample
        cfg = FetchConfig(symbols=['AAPL'], start='2022-01-03', end='2022-01-10')
        df = fetch_data(cfg)
        assert not df.empty
        assert 'symbol' in df.columns
        instance.history.assert_called_once_with(start='2021-12-04', end='2022-01-10')


def test_load_to_db_creates_stock_entries(tmp_path):
    engine = get_engine(tmp_path / "test.db")
    df = pd.DataFrame(
        {
            "open": [1.0],
            "high": [1.0],
            "low": [1.0],
            "close": [1.0],
            "volume": [1.0],
            "dividends": [0.0],
            "stock_splits": [0.0],
            "symbol": ["AAPL"],
            "price_over_ma30": [1.0],
            "bb_pct": [1.0],
            "suggested_position": ["Cash"],
        },
        index=pd.to_datetime(["2022-01-03"]),
    )
    load_to_db(df, engine)
    insp = inspect(engine)
    tables = set(insp.get_table_names())
    assert tables == {"stocks", "prices", "position"}
    stocks_df = pd.read_sql_table("stocks", engine)
    prices_df = pd.read_sql_table("prices", engine)
    assert stocks_df.loc[0, "symbol"] == "AAPL"
    assert prices_df.loc[0, "stock_id"] == stocks_df.loc[0, "id"]
    assert prices_df.loc[0, "bb_pct"] == 1.0
    pos_df = pd.read_sql_table("position", engine)
    assert prices_df.loc[0, "suggested_position"] == pos_df[pos_df["name"] == "Cash"].iloc[0]["id"]
