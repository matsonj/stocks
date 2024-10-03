{{
    config(
        pre_hook="""
            set variable my_list = (
                select array_agg(file) from {{ ref('files') }} where entity = 'ticker_history'
            )
        """,
        materialized="incremental",
        unique_key="id",
    )
}}

select
    symbol || '-' || date || '-' || filename as id,
    stocks.*,
    files.modified_ts,
    now() at time zone 'UTC' as updated_ts
from read_csv(getvariable('my_list'), filename = true, union_by_name = true) as stocks
left join {{ ref("files") }} as files on stocks.filename = files.file
{% if is_incremental() %}
    where not exists (select 1 from {{ this }} ck where ck.filename = stocks.filename)
{% endif %}
