## MotherDuck Stocks Data Workshop

This workshop will help you get data from csv into MotherDuck, and lay out basic patterns for using dbt + MotherDuck in a performant way.

### Getting Started
1. Create a MotherDuck account.
2. Create a database called "stocks_dev" inside of MotherDuck. This can be done with the command `create database stocks_dev;` from the MotherDuck UI.
3. Fork the `matsonj/stocks` repo in GitHub.
4. Generate an access token inside of MotherDuck and add it as a codespace secret inside of GitHub.
5. Open a codespace on the repo.
6. After it loads completely, _reload the window_ in order to make sure the dbt power user extension has access to your md environment.

### Running the project
1. Get data from the yahoo finance api by running the following 3 commands:
    - `python3 get_info.py`
    - `python3 get_options.py`
    - `python3 get_stock_history.py`
2. Build the data warehouse with `dbt build` in the CLI.
3. Lastly, plot the results using `python3 viz/line_chart.py`. The webpage will be available at `127.0.0.1:8050`.
4. Alternatively, you can invoke these 3 steps with `make run`.

### Data Flow Overview
1. Data is extracted from yahoo finance API using python. The scripts run and write out a file to `data` folder with the timestamp in the name for each file.
    - `symbols.txt` contains the list of symbols for which to fetch data.
    - `get_info.py` gets the company information for each company.
    - `get_options.py` gets the currently open options. *note:* this data is temporal, and thus needs to be snapshotted. This is left as an exercise to the reader.
    - `get_stock_history.py` gets the stock price history for the last 30 days.
2. dbt creates a list of these files in `files.sql` with the Duckdb `glob` function.
3. for each model - `company_info.sql` `options.sql` `stock_history.sql` - de-duplicate and load any new files.
4. for the models in step 3, test to make sure that the primary key is unique.
5. create a dataset of closing stock price X outstanding shares over time to estimate Market Cap.
   
### Plotting

1. Plotting is defined in the `viz/line_chart.py` file. It is a set of simple charts using `plotly` and `dash`. 
2. You can serve the plots with `python3 viz/line_chart.py`.
