import duckdb
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the MOTHERDUCK_TOKEN from environment variables
MOTHERDUCK_TOKEN = os.getenv('MOTHERDUCK_TOKEN')

# Sample data from DuckDB
conn = duckdb.connect(f'md:?MOTHERDUCK_TOKEN={MOTHERDUCK_TOKEN}')
df = conn.execute('''
select date as date, market_cap as value, symbol
from stocks_dev.main.market_cap_by_day
where symbol = 'AAPL'
''').df()

df2 = conn.execute('''
select * exclude(id, date), date as date
from stocks_dev.main.fact_stock_prices
where symbol = 'AAPL'
''').df()

df3 = conn.execute('''
                   select distinct symbol
                   from stocks_dev.main.market_cap_by_day
                   where market_cap is not null
                   ''').df()


import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)
# Create a dropdown list using df3
dropdown_options = [{'label': symbol, 'value': symbol} for symbol in df3['symbol']]

app.layout = html.Div(children=[
    html.H1(children='Stock Performance'),
    html.H2(children='Select a Symbol'),
    
    dcc.Dropdown(
        id='symbol-dropdown',
        options=dropdown_options,
        value='AAPL'  # Default value
    ),
    
    html.H2(children='Market Cap Line Chart'),
    dcc.Graph(
        id='line-chart'
    ),
    
    html.H2(children='Candlestick Chart'),
    dcc.Graph(
        id='candlestick-chart'
    )
])

@app.callback(
    [Output('line-chart', 'figure'), Output('candlestick-chart', 'figure')],
    [Input('symbol-dropdown', 'value')]
)
def update_charts(selected_symbol):
    # Query data based on selected symbol
    df = conn.execute(f'''
    select date as date, market_cap as value, symbol
    from stocks_dev.main.market_cap_by_day
    where symbol = '{selected_symbol}'
    ''').df()

    df2 = conn.execute(f'''
    select * exclude(id, date), date as date
    from stocks_dev.main.fact_stock_prices
    where symbol = '{selected_symbol}'
    ''').df()

    # Create a line chart using Plotly Express
    fig = px.line(df, x='date', y='value', title=f'{selected_symbol} Market Cap: Last 360 days')

    # Update layout for better aesthetics
    fig.update_layout(
        title={
            'text': f'{selected_symbol} Market Cap: Last 360 days',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title='Market Cap (USD)',
        yaxis_tickprefix="$",
        template='plotly_white',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="RebeccaPurple"
        )
    )

    # Update traces for better visibility
    fig.update_traces(
        line=dict(color='royalblue', width=2),
        marker=dict(size=4)
    )

    # Create a candlestick chart using Plotly
    fig2 = go.Figure(data=[go.Candlestick(x=df2['date'], 
                                          open=df2['Open'], 
                                          high=df2['High'], 
                                          low=df2['Low'], 
                                          close=df2['Close'])])

    # Update layout for better aesthetics
    fig2.update_layout(
        title={
            'text': f'{selected_symbol} Candlestick Chart: Last 360 days',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title='Stock Price (USD)',
        yaxis_tickprefix="$",
        template='plotly_white',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="RebeccaPurple"
        )
    )

    # Update traces for better visibility
    fig2.update_traces(
        increasing_line_color='royalblue', 
        decreasing_line_color='firebrick',
        line_width=1
    )

    return fig, fig2

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
