run:
	python3 scripts/get_info.py
	python3 scripts/get_options.py
	python3 scripts/get_stock_history.py
	dbt build
	python3 viz/line_chart.py