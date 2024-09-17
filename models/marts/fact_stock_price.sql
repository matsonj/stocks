select * from {{ ref("stock_history")}}
order by symbol, date