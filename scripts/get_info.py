import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

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

def fetch_stock_info(symbol):
    """Fetches stock information (info endpoint) for a valid symbol."""
    try:
        stock = yf.Ticker(symbol)
        return stock.info
    except Exception as e:
        print(f"Error fetching info for {symbol}: {e}")
        return {}

def main():
    # Read the stock symbols from the file
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'symbols.txt')
    symbols = read_symbols_from_file(file_path)

    if not symbols:
        print("No symbols found in file.")
        return

    all_info = []

    # Validate and fetch stock info for each symbol
    for symbol in symbols:
        if validate_symbol(symbol):
            print(f"Fetching info for: {symbol}")
            stock_info = fetch_stock_info(symbol)
            if stock_info:
                stock_info['Symbol'] = symbol  # Add symbol column to the info
                all_info.append(stock_info)
        else:
            print(f"Invalid symbol: {symbol}")

    if all_info:
        # Create a DataFrame from the info data
        info_df = pd.DataFrame(all_info)

        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Export to CSV with timestamp in the file name
        file_name = os.path.join(script_dir, '..', 'data', f'ticker_info_{timestamp}.csv')
        info_df.to_csv(file_name, index=False)
        print(f"Info saved to {file_name}")
    else:
        print("No valid stock info found to save.")

if __name__ == "__main__":
    main()
