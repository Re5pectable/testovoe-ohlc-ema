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

Basic execution:
```
python ema_drawing.py -f data.csv -el 4 -t 1h -e print
```

Export EMA data to CSV with OHLC values:
```
python ema_drawing.py -f data.csv -el 4 -t 1h -e csv_ohlc -ep ema_output_ohlc.csv
```

Export only the EMA data to a CSV:
```
python ema_drawing.py -f data.csv -el 4 -t 1h -e csv_ema -ep ema_output.csv
```

Show the chart after generating it:
```
python ema_drawing.py -f data.csv -el 4 -t 1h -e print -cs
```

Adjust chart resolution and save the chart to a file:
```
python ema_drawing.py -f data.csv -el 4 -t 1h -e print -cs -cw 1280 -ch 720 -co output_chart.png
```

Use a different EMA length and timeframe:
```
python ema_drawing.py -f data.csv -el 10 -t 15m -e print
```

Do not show the chart, but save it to a file:
```
python ema_drawing.py -f data.csv -el 4 -t 1h -e print -co output_chart.png
```

Export EMA data to CSV with OHLC values and save chart:
```
python ema_drawing.py -f data.csv -el 4 -t 1h -e csv_ohlc -ep ema_output_ohlc.csv -co output_chart.png
```

Use a different timeframe:
```
python ema_drawing.py -f data.csv -el 4 -t 1d -e print -cs
```

Combination of different parameters:
```
python ema_drawing.py -f data.csv -el 20 -t 4h -e csv_ema -ep ema_output.csv -cs -cw 1024 -ch 768 -co custom_chart.png
```