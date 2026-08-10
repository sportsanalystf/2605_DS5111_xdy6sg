{{ config(materialized='table') }}

SELECT
    video_id,
    f.value::STRING AS book_name,
    INSERTED_AT AS processed_at
FROM {{ ref('stg_youtube_transcripts') }},
LATERAL FLATTEN(input => book_names_array) f
