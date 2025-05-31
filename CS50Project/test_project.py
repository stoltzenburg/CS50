import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from project import fetch_data, analyze, user_action, execute, tp_level, sl_level

def test_fetch_data():
    # Mock yfinance download to return a predefined DataFrame
    with patch('yfinance.download') as mock_download:
        # Conatin enough data points for ATR to be calculated
        dates = pd.date_range(start='2023-01-01', periods=20)
        sample_data = pd.DataFrame({
            'Open': np.random.rand(20) * 100,
            'High': np.random.rand(20) * 110,
            'Low': np.random.rand(20) * 90,
            'Close': np.random.rand(20) * 100,
            'Volume': np.random.rand(20) * 1000000
        }, index=dates)

        # Convert to MultiIndex columns like yfinance returns
        columns = pd.MultiIndex.from_product([['Open', 'High', 'Low', 'Close', 'Volume'], ['Adj']])
        sample_data.columns = columns

        mock_download.return_value = sample_data

        result = fetch_data('AAPL')

        assert result is not None
        assert 'ATR' in result.columns
        mock_download.assert_called_once_with('AAPL', period='6mo', interval='1d', auto_adjust=False)

    # Test empty data
    with patch('yfinance.download') as mock_download:
        mock_download.return_value = pd.DataFrame()
        result = fetch_data('INVALID')
        assert result is None

def test_analyze():
    # Create test data
    dates = pd.date_range(start='2023-01-01', periods=60)
    data = pd.DataFrame({
        'Open': np.random.rand(60) * 100,
        'High': np.random.rand(60) * 110,
        'Low': np.random.rand(60) * 90,
        'Close': np.linspace(80, 120, 60),  # Trending up
        'Volume': np.random.rand(60) * 1000000,
        'ATR': np.ones(60) * 2.5  # Constant ATR for simplicity
    }, index=dates)

    # Pre-calculate SMA and RSI for testing
    data['SMA50'] = data['Close'].rolling(window=50).mean()

    with patch('builtins.print'):
        result, atr = analyze(data)

        assert result is not None
        assert isinstance(atr, float)
        assert round(atr, 1) == 2.5
        assert 'RSI' in data.columns
        assert 'SMA50' in data.columns

def test_user_action_buy():
    # Test when user chooses "yes" and RSI is oversold
    analysis_oversold = pd.Series({'RSI': 20, 'Close': 100, 'SMA50': 110})
    with patch('builtins.input', return_value='yes'):
        result = user_action(analysis_oversold)
        assert result == 'BUY'

def test_user_action_sell():
    # Test when user chooses "yes" and RSI is overbought
    analysis_overbought = pd.Series({'RSI': 80, 'Close': 100, 'SMA50': 90})
    with patch('builtins.input', return_value='yes'):
        result = user_action(analysis_overbought)
        assert result == 'SELL'

def test_user_action_neutral():
    # Test when user chooses "yes" but RSI is neutral
    analysis_neutral = pd.Series({'RSI': 50, 'Close': 100, 'SMA50': 100})
    with patch('builtins.input', return_value='yes'):
        with pytest.raises(SystemExit):
            user_action(analysis_neutral)

def test_user_action_no():
    # Test when user chooses "no"
    analysis_oversold = pd.Series({'RSI': 20, 'Close': 100, 'SMA50': 110})
    with patch('builtins.input', return_value='no'):
        with pytest.raises(SystemExit):
            user_action(analysis_oversold)

def test_execute_buy():
    # Mock user input and yfinance Ticker for BUY action
    with patch('builtins.input', return_value='1000'):
        with patch('yfinance.Ticker') as mock_ticker:
            mock_instance = MagicMock()
            mock_instance.info = {'currentPrice': 150.0}
            mock_ticker.return_value = mock_instance

            # Test BUY action
            stock_price, stop_loss, take_profit, quantity = execute('BUY', 'AAPL', 5.0)

            assert stock_price == 150.0
            assert stop_loss == 145.0  # 150 - 5
            assert take_profit == 160.0  # 150 + 2*5
            assert quantity == 1000

def test_execute_sell():
    # Mock user input and yfinance Ticker for SELL action
    with patch('builtins.input', return_value='1000'):
        with patch('yfinance.Ticker') as mock_ticker:
            mock_instance = MagicMock()
            mock_instance.info = {'currentPrice': 150.0}
            mock_ticker.return_value = mock_instance

            # Test SELL action
            stock_price, stop_loss, take_profit, quantity = execute('SELL', 'AAPL', 5.0)

            assert stock_price == 150.0
            assert stop_loss == 155.0  # 150 + 5
            assert take_profit == 140.0  # 150 - 2*5
            assert quantity == 1000

def test_tp_level_buy():
    tp = tp_level('BUY', 5.0, 100.0)
    assert tp == 110.0

def test_tp_level_sell():
    tp = tp_level('SELL', 5.0, 100.0)
    assert tp == 90.0

def test_sl_level_buy():
    sl = sl_level(5.0, 100.0, 'BUY')
    assert sl == 95.0

def test_sl_level_sell():
    sl = sl_level(5.0, 100.0, 'SELL')
    assert sl == 105.0
