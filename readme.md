# Candlestick Chart Generator with EMA Overlay

This script provides a tool to generate a candlestick chart with an Exponential Moving Average (EMA) overlay from time series data stored in a CSV file.

## Requirements

- Python 3.x
- pandas
- plotly
- argparse
- re
- os
- kaleido (optional for exporting images)

## CSV Format

The input CSV file should have at least a column named 'TS' (indicating the timestamp). This column will be used to sort the data and serve as the X-axis of the chart.

## Usage

```
python ema_drawing.py -f [FILE_PATH] -el [EMA_LENGTH] -t [TIMEFRAME] -e [EXPORT_OPTION] [OPTIONAL_ARGUMENTS]
```

### Arguments:

- `--file_input, -f`: Path to the CSV data file. **(Required)**
- `--ema_length, -el`: Length for EMA calculation. Should be a positive integer. **(Required)**
- `--timeframe, -t`: Timeframe for resampling. Examples: 1h, 15m, 1d, 123mo. Should start with a sequence of digits followed by a sequence of letters. **(Required)**
- `--export, -e`: Export method for EMA data. Options: "print" (to console), "csv_ohlc" (CSV with OHLC), "csv_ema" (CSV with only EMA). **(Required)**
- `--export_ema_path, -ep`: Path to save the exported EMA data. Required if `--export` is set to "csv_ohlc" or "csv_ema".
- `--chart_show, -cs`: Flag to show the chart after generation.
- `--chart_width, -cw`: Width in pixels of the chart. Default is 1600 pixels.
- `--chart_height, -ch`: Height in pixels of the chart. Default is 800 pixels.
- `--chart_output, -co`: Path to save the output chart image.

## Examples:

To generate a chart and print EMA values:
```bash
python script_name.py -f data.csv -el 10 -t 1h -e print -cs
```

To generate a chart, save it, and also save OHLC and EMA values to a CSV file:
```bash
python script_name.py -f data.csv -el 10 -t 1d -e csv_ohlc -ep output_ema.csv -cs -co output_chart.png
```