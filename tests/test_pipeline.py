import pandas as pd
from finance_pipeline.main import compute_moving_averages
from finance_pipeline.data_fetcher import FetchConfig, fetch_data
from unittest import mock


def test_compute_moving_averages():
    data = pd.DataFrame({'close': list(range(1, 40))})
    result = compute_moving_averages(data)
    ma30 = pd.Series(data['close']).rolling(30).mean()
    expected_ratio = data['close'] / ma30
    expected_ratio.index = result.index
    pd.testing.assert_series_equal(result['price_over_ma30'], expected_ratio, check_names=False)
    assert 'ma7' not in result.columns
    assert 'ma30' not in result.columns


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
