{{
    config(
        pre_hook="""
            set variable my_list = (
                select array_agg(file) from {{ ref('files') }} where entity = 'option_history'
            )
        """,
        materialized="incremental",
        unique_key="contractSymbol",
    )
}}

select options.*, now() at time zone 'UTC' as updated_at
from read_csv(getvariable(my_list), filename = true) as options
left join {{ ref("files") }} as files on options.filename = files.file
{% if is_incremental() %}
    where
        not exists (
            select 1
            from {{ this }} existence_ck
            where existence_ck.filename = options.filename
        )
{% endif %}
qualify
    row_number() over (
        partition by options.contractsymbol order by files.timestamp desc
    )
    = 1
