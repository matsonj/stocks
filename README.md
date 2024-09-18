## MotherDuck Stocks Data Workshop

This workshop will help you get data from csv into MotherDuck, and lay out basic patterns for using dbt + MotherDuck in a performant way.

### Getting Started
1. Create a MotherDuck account.
2. Create a database called "stocks" inside of MotherDuck. This can be done with the command `create database stocks;` from the MotherDuck UI.
3. Fork the `matsonj/stocks` repo in GitHub.
4. Generate an access token inside of MotherDuck and add it to your `.env` file or as a secret inside of GitHub.
    - it should be noted that using it as a codespace-scoped secret allows all github extensions to use it, as we can put it in the dbt path easily.
5. Open a codespace on the repo.
6. After it loads completely, _reload the window_ in order to make sure the dbt power user extension has access to your md environment.

### Data Flow Overview
1. Data is extracted from yahoo finance API using python. The scripts run and write out a file to `data` folder with the timestamp in the name for each file.
    - `symbols.txt` contains the list of symbols for which to fetch data.
    - `get_info.py` gets the company information for each company.
    - `get_options.py` gets the currently open options. *note:* this data is temporal, and thus needs to be snapshotted.
    - `get_stock_history.py` gets the stock price history for the last 30 days.
2. dbt creates a list of these files in `files.sql` with the Duckdb `glob` function.
3. for each model - `company_info.sql` `options.sql` `stock_history.sql` - de-duplicate and load any new files.
4. for the models in step 3, test to make sure that the primary key is unique.
5. create a dataset of closing stock price X outstanding shares over time to estimate Market Cap.
   
### Plotting
