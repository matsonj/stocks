with
    cte_all_rows as (
        select
            symbol,
            * exclude(symbol),
            modified_ts as ts
        from {{ ref("stock_history") }}
    )
select unnest(arg_max(cte_all_rows, ts))
from cte_all_rows
group by symbol, date
