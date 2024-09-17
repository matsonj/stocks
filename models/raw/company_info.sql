{{
    config(
        pre_hook="""
            set variable my_list = (
                select array_agg(file) from {{ ref('files') }} where entity = 'ticker_info'
            )
        """,
        materialized="incremental",
        unique_key="symbol",
    )
}}

select info.*, now() at time zone 'UTC' as updated_at
from read_csv(getvariable(my_list), filename = true) as info
left join {{ ref("files") }} as files on info.filename = files.file
{% if is_incremental() %}
    where
        not exists (
            select 1
            from {{ this }} existence_ck
            where existence_ck.filename = info.filename
        )
{% endif %}
qualify row_number() over (partition by info.symbol order by files.timestamp desc) = 1
