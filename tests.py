import unittest
from ema_drawing import load_data, validate_timeframe, calculate_ohlc, add_ema, generate_chart
import pandas as pd
import os

class TestCandlestickWithEMA(unittest.TestCase):

    def test_load_data(self):
        # This test assumes a sample CSV named 'test_prices.csv' with appropriate data
        data = load_data('test_prices.csv')
        self.assertIn('TS', data.index.name)

    def test_validate_timeframe(self):
        self.assertEqual(validate_timeframe('1h'), 'H')
        self.assertEqual(validate_timeframe('1d'), 'D')
        with self.assertRaises(ValueError):
            validate_timeframe('1x')

    def test_calculate_ohlc(self):
        # Use your test data or mock data for this test
        data = load_data('test_prices.csv')
        ohlc_data = calculate_ohlc(data, 'H')
        self.assertIn('open', ohlc_data.columns)
        self.assertIn('high', ohlc_data.columns)
        self.assertIn('low', ohlc_data.columns)
        self.assertIn('close', ohlc_data.columns)

    def test_add_ema(self):
        # Use your test data or mock data for this test
        data = load_data('test_prices.csv')
        ohlc_data = calculate_ohlc(data, 'H')
        with_ema_data = add_ema(ohlc_data, 4)
        self.assertIn('EMA', with_ema_data.columns)
    
    def test_plot_candlestick_with_ema(self):
        df = pd.DataFrame({
            'open': [1, 2, 3],
            'high': [1.5, 2.5, 3.5],
            'low': [0.5, 1.5, 2.5],
            'close': [1.2, 2.2, 3.2],
            'EMA': [1.1, 2.1, 3.1],
        })
        df.index = pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03"])
        output_file = "test_output.png"
        generate_chart(df, output_file, (800, 600), show=False)
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()