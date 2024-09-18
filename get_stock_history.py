import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def read_symbols_from_file(file_path):
    """Reads stock symbols from a file."""
    try:
        with open(file_path, 'r') as file:
            symbols = file.read().splitlines()
        return symbols
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def validate_symbol(symbol):
    """Validates a symbol using yfinance."""
    try:
        stock = yf.Ticker(symbol)
        if stock.history(period='1d').empty:
            return False
        return True
    except Exception as e:
        print(f"Error validating symbol {symbol}: {e}")
        return False

def fetch_stock_data(symbol, start_date, end_date):
    """Fetches stock data for a valid symbol."""
    try:
        return yf.download(symbol, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

def main():
    # Define the date range (last 30 days)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=360)).strftime('%Y-%m-%d')

    # Read the stock symbols from the file
    symbols = read_symbols_from_file('symbols.txt')

    if not symbols:
        print("No symbols found in file.")
        return

    all_data = []

    # Validate and fetch stock data for each symbol
    for symbol in symbols:
        if validate_symbol(symbol):
            print(f"Fetching data for: {symbol}")
            stock_data = fetch_stock_data(symbol, start_date, end_date)
            stock_data['Symbol'] = symbol  # Add symbol column to the data
            all_data.append(stock_data)
        else:
            print(f"Invalid symbol: {symbol}")

    if all_data:
        # Concatenate all stock data into one DataFrame
        result_df = pd.concat(all_data)

        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Export to CSV with timestamp in the file name
        file_name = f"data/ticker_history_{timestamp}.csv"
        result_df.to_csv(file_name, index=True)
        print(f"Data saved to {file_name}")
    else:
        print("No valid stock data found to save.")

if __name__ == "__main__":
    main()

