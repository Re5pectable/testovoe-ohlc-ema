import os
import unittest

import pandas as pd

from ema_drawing import (add_ema, calculate_ohlc, export_ema, generate_chart,
                         load_data, validate_timeframe)


class TestCandlestickWithEMA(unittest.TestCase):

    def test_load_data_valid_path(self):
        data = load_data('test_prices.csv')
        self.assertIn('TS', data.index.name)

    def test_load_data_invalid_path(self):
        with self.assertRaises(ValueError):
            load_data('non_existent.csv')

    def test_load_data_without_TS_column(self):
        with self.assertRaises(ValueError):
            load_data('invalid_test_prices.csv')

    def test_validate_timeframe_valid(self):
        self.assertEqual(validate_timeframe('1h'), '1H')
        self.assertEqual(validate_timeframe('1d'), '1D')
        self.assertEqual(validate_timeframe('12h'), '12H')

    def test_validate_timeframe_invalid(self):
        with self.assertRaises(ValueError):
            validate_timeframe('1x')
        with self.assertRaises(ValueError):
            validate_timeframe('h1')
        with self.assertRaises(ValueError):
            validate_timeframe('123')

    def test_calculate_ohlc(self):
        data = load_data('test_prices.csv')
        ohlc_data = calculate_ohlc(data, '1H')
        self.assertIn('open', ohlc_data.columns)
        self.assertIn('high', ohlc_data.columns)
        self.assertIn('low', ohlc_data.columns)
        self.assertIn('close', ohlc_data.columns)

    def test_add_ema(self):
        data = load_data('test_prices.csv')
        ohlc_data = calculate_ohlc(data, '1H')
        with_ema_data = add_ema(ohlc_data, 4)
        self.assertIn('EMA', with_ema_data.columns)

    def test_export_functions(self):
        data = pd.DataFrame({
            'open': [1, 2, 3],
            'high': [1.5, 2.5, 3.5],
            'low': [0.5, 1.5, 2.5],
            'close': [1.2, 2.2, 3.2],
            'EMA': [1.1, 2.1, 3.1],
        })
        export_ema_path = "test_export.csv"
        export_ema(data, 'csv_ohlc', export_ema_path)
        self.assertTrue(os.path.exists(export_ema_path))
        os.remove(export_ema_path)

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
        generate_chart(df, '1D', 5, (800, 600), output_file=output_file, show=False)
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
