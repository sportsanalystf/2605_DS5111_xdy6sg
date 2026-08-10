{{ config(materialized='table') }}

SELECT
    video_id,
    f.value::STRING AS tech_term,
    INSERTED_AT AS processed_at
FROM {{ ref('stg_youtube_transcripts') }},
LATERAL FLATTEN(input => tech_terms_array) f
