import argparse
import os

import pandas as pd
import plotly.graph_objects as go

TIMEFRAMES_MAPPING = {
    'mo': 'M',
    'w': 'W',
    'd': 'D',
    'h': 'H',
    'm': 'T',
    's': 'S',
}

def load_data(filename):
    """Load data from CSV and preprocess it."""
    if not os.path.exists(filename):
        raise ValueError(f"File '{filename}' not found.")
    
    data = pd.read_csv(filename)
    
    if 'TS' not in data.columns:
        raise ValueError("Expected 'TS' column not found in the CSV.")
    
    data['TS'] = pd.to_datetime(data['TS'])
    data = data.sort_values(by='TS')
    data.set_index('TS', inplace=True)
    return data

def validate_timeframe(timeframe: str):
    """Validate the timeframe against allowed pandas resampling frequencies."""
    base_timeframe = ''.join([char for char in timeframe if not char.isdigit()])
    
    if base_timeframe not in TIMEFRAMES_MAPPING.keys():
        raise ValueError(f"Invalid timeframe '{timeframe}'. Choose from: {', '.join(TIMEFRAMES_MAPPING.keys())} (with prefix number). Example: '1h'.")
    return TIMEFRAMES_MAPPING[base_timeframe]

def calculate_ohlc(data: pd.DataFrame, timeframe: str):
    """Calculate OHLC data from provided dataframe."""
    data = data.resample(timeframe).ohlc()
    data.columns = data.columns.droplevel()
    return data

def add_ema(data: pd.DataFrame, ema_length: int):
    """Calculate and add the EMA to the data."""
    data['EMA'] = data.close.ewm(span=ema_length, adjust=False).mean()
    return data

def generate_chart(data: pd.DataFrame, resolution: tuple[int, int], show: bool = True, output_file: str = None):
    """Generate the candlestick chart with EMA overlay and save to a file."""
    fig = go.Figure(data=[
        go.Candlestick(
            x=data.index,
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            name="Candles"
        ),
        go.Scatter(
            x=data.index,
            y=data['EMA'],
            mode='lines',
            name='EMA',
            line={'color':'blue', 'width': 1})
        ]
    )
    fig.update_layout(
        title="Candlestick Chart with EMA Overlay",
        width=resolution[0],
        height=resolution[1],
        xaxis_rangeslider_visible=False
    )
    if show:
        fig.show()
    if output_file:
        fig.write_image(output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a candlestick chart with EMA overlay.')
    parser.add_argument(
        '--file_input', '-f',
        required=True,
        dest='file',
        help='Path to the CSV data file.'
    )
    parser.add_argument(
        '--ema_length', '-el',
        required=True,
        type=int,
        dest='ema_length',
        help='Length for EMA calculation.'
    )
    parser.add_argument(
        '--timeframe', '-t',
        required=True,
        dest='timeframe',
        help='Timeframe for resampling. Examples: 1h, 15m, 1d, etc.'
    )
    parser.add_argument(
        '--chart_show', '-cs',
        action='store_false',
        dest='show_chart',
        help='Show the chart after generation.'
    )
    parser.add_argument(
        '--chart_width', '-cw',
        dest='chart_width',
        type=int,
        default=1920,
        help='Width in pixels of the chart.'
    )
    parser.add_argument(
        '--chart_height', '-ch',
        dest='chart_height',
        type=int,
        default=1080,
        help='Height in pixels of the chart.'
    )
    parser.add_argument(
        '--chart_output', '-co',
        dest='chart_output',
        help='Path to save the output chart image.'
    )
    args = parser.parse_args()

    timeframe = validate_timeframe(args.timeframe)
    if args.ema_length <= 0:
        raise ValueError("EMA Length should be a positive integer.")
    
    data = load_data(args.file)
    data = calculate_ohlc(data, timeframe)
    data = add_ema(data, args.ema_length)
    if args.show_chart or args.chart_output:
        generate_chart(data, (args.chart_width, args.chart_height),
                       show=args.show_chart,
                       output_file=args.chart_output
                    )