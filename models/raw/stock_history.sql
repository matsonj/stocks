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

select symbol || '-' || date as id, stocks.*, now() at time zone 'UTC' as updated_at
from read_csv(getvariable(my_list), filename = true) as stocks
left join {{ ref("files") }} as files on stocks.filename = files.file
{% if is_incremental() %}
    where
        not exists (
            select 1
            from {{ this }} existence_ck
            where existence_ck.filename = stocks.filename
        )
{% endif %}
qualify
    row_number() over (
        partition by id order by files.timestamp desc
    )
    = 1
