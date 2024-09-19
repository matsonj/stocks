{{
    config(
        pre_hook="""
            set variable my_list = (
                select array_agg(file) from {{ ref('files') }} where entity = 'ticker_info'
            )
        """,
        materialized="incremental",
        unique_key="id",
    )
}}

select
    info.symbol || '-' || info.filename as id,
    info.*,
    now() at time zone 'UTC' as updated_at
from read_csv(getvariable(my_list), filename = true) as info
{% if is_incremental() %}
    where not exists (select 1 from {{ this }} ck where ck.filename = info.filename)
{% endif %}
