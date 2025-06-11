import pandas as pd
from finance_pipeline.main import compute_moving_averages
from finance_pipeline.data_fetcher import FetchConfig, fetch_data
from unittest import mock


def test_compute_moving_averages():
    data = pd.DataFrame({'close': [1,2,3,4,5,6,7,8,9,10]})
    result = compute_moving_averages(data)
    assert result['ma7'].iloc[6] == sum(range(1,8))/7
    assert pd.isna(result['ma7'].iloc[5])
    assert pd.isna(result['ma30'].iloc[-1])


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
        instance.history.assert_called_once()
