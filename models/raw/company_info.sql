{{
    config(
        pre_hook="""
            set variable my_list = (
                select array_agg(file) from {{ ref('files') }} where entity = 'ticker_info'
            )
        """,
        materialized="incremental",
        unique_key="symbol",
        post_hook="""
            delete from {{this}} where filename not in (select file from {{ ref('files') }} where entity = 'ticker_info')   
            """
    )
}}

select *
from read_csv(getvariable(my_list), filename = true)
{% if is_incremental() %}
    where filename not in (select filename from {{ this }})
{% endif %}
