import yfinance as yf
import pandas as pd
from datetime import datetime

def read_symbols_from_file(file_path):
    """Reads stock symbols from a file."""
    try:
        with open(file_path, 'r') as file:
            symbols = file.read().splitlines()
        return symbols
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def fetch_option_data(symbol):
    """Fetches option chain data for a valid symbol."""
    try:
        stock = yf.Ticker(symbol)
        # Get all expiration dates for options
        exp_dates = stock.options
        
        if not exp_dates:
            print(f"No option data available for {symbol}")
            return pd.DataFrame()

        # Fetch option data for each expiration date
        all_options_data = []
        for exp in exp_dates:
            print(f"Fetching options for {symbol} expiring on {exp}")
            options = stock.option_chain(exp)
            
            # Combine calls and puts with expiration date
            calls = options.calls
            calls['Type'] = 'Call'
            puts = options.puts
            puts['Type'] = 'Put'
            
            options_data = pd.concat([calls, puts])
            options_data['Expiration'] = exp
            options_data['Symbol'] = symbol
            
            all_options_data.append(options_data)
        
        return pd.concat(all_options_data)
    
    except Exception as e:
        print(f"Error fetching option data for {symbol}: {e}")
        return pd.DataFrame()

def main():
    # Read the stock symbols from the file
    symbols = read_symbols_from_file('symbols.txt')

    if not symbols:
        print("No symbols found in file.")
        return

    all_option_data = []

    # Fetch option data for each symbol
    for symbol in symbols:
        print(f"Fetching option data for: {symbol}")
        option_data = fetch_option_data(symbol)
        if not option_data.empty:
            all_option_data.append(option_data)
        else:
            print(f"No valid option data for {symbol}")

    if all_option_data:
        # Concatenate all option data into one DataFrame
        result_df = pd.concat(all_option_data)

        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')


        # Export to CSV with timestamp in the file name
        file_name = f"data/option_history_{timestamp}.csv"
        result_df.to_csv(file_name, index=True)
        print(f"Data saved to {file_name}")
    else:
        print("No valid option data found to save.")

if __name__ == "__main__":
    main()

