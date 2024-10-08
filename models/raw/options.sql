{{
    config(
        pre_hook="""
            set variable my_list = (
                select array_agg(file) from {{ ref('files') }} where entity = 'option_history'
            )
        """,
        materialized="incremental",
        unique_key="id",
    )
}}

select
    options.contractsymbol || '-' || options.filename as id,
    options.*,
    files.modified_ts,
    now() at time zone 'UTC' as updated_ts
from read_csv(getvariable('my_list'), filename = true, union_by_name = true) as options
left join {{ ref("files") }} as files on options.filename = files.file
{% if is_incremental() %}
    where not exists (select 1 from {{ this }} ck where ck.filename = options.filename)
{% endif %}
