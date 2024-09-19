with
    cte_all_rows as (
        select
            symbol,
            * exclude(id, symbol),
            strptime(regexp_extract("filename", '_(\d+)\.csv', 1), '%Y%m%d%H%M%S') as ts
        from {{ ref("company_info") }}
    )
select unnest(arg_max(cte_all_rows, ts))
from cte_all_rows
group by symbol
