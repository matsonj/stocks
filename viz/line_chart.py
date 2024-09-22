import os
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load environment variables from a .env file
load_dotenv()
MOTHERDUCK_TOKEN = os.getenv('MOTHERDUCK_TOKEN')

# Connect to DuckDB using the MotherDuck token
conn = duckdb.connect(f'md:?MOTHERDUCK_TOKEN={MOTHERDUCK_TOKEN}')

# Retrieve available stock symbols for the dropdown menu
symbols_df = conn.execute('''
    SELECT DISTINCT symbol
    FROM stocks_dev.main.market_cap_by_day
    WHERE market_cap IS NOT NULL
    ORDER BY symbol
''').df()
symbols = symbols_df['symbol'].tolist()

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Stock Performance'),
    html.H2('Select a Symbol'),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': sym, 'value': sym} for sym in symbols],
        value='AAPL'  # Default selected symbol
    ),
    html.H2('Market Cap Line Chart'),
    dcc.Graph(id='line-chart'),
    html.H2('Candlestick Chart'),
    dcc.Graph(id='candlestick-chart')
])

# Callback to update charts based on selected symbol
@app.callback(
    [Output('line-chart', 'figure'), Output('candlestick-chart', 'figure')],
    [Input('symbol-dropdown', 'value')]
)
def update_charts(selected_symbol):
    # Query market cap data for the selected symbol
    market_cap_df = conn.execute(f'''
        SELECT Date, market_cap
        FROM stocks_dev.main.market_cap_by_day
        WHERE symbol = '{selected_symbol}'
    ''').df()
    
    # Ensure consistent column naming
    market_cap_df.rename(columns={'Date': 'date'}, inplace=True)

    # Create a line chart for market cap
    line_fig = px.line(
        market_cap_df, x='date', y='market_cap',
        title=f'{selected_symbol} Market Cap: Last 360 days'
    )

    # Query stock price data for the selected symbol
    stock_prices_df = conn.execute(f'''
        SELECT Date, Open, High, Low, Close
        FROM stocks_dev.main.fact_stock_prices
        WHERE symbol = '{selected_symbol}'
    ''').df()
    
    # Ensure consistent column naming
    stock_prices_df.rename(columns={'Date': 'date'}, inplace=True)

    # Create a candlestick chart for stock prices
    candlestick_fig = go.Figure(data=[
        go.Candlestick(
            x=stock_prices_df['date'],
            open=stock_prices_df['Open'],
            high=stock_prices_df['High'],
            low=stock_prices_df['Low'],
            close=stock_prices_df['Close']
        )
    ])
    candlestick_fig.update_layout(
        title=f'{selected_symbol} Candlestick Chart: Last 360 days',
        xaxis_title='Date',
        yaxis_title='Stock Price (USD)',
        yaxis_tickprefix='$',
        template='plotly_white'
    )

    return line_fig, candlestick_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
