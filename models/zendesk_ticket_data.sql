{{ config(materialized='table') }}

with source_data as (

    select * from {{ ref('raw_zendesk_data') }}
)

select *
from source_data
