{{ config(materialized="table") }}

select
    c.symbol,
    c.sharesoutstanding,
    sp.close,
    sp.date,
    round(c.sharesoutstanding::real * sp.close::real, 0) as market_cap
from {{ ref("dim_companies") }} c
left join {{ ref("fact_stock_prices") }} sp on c.symbol = sp.symbol
order by c.symbol, sp.date
