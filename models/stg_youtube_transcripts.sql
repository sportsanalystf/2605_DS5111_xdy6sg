{{ config(materialized='view') }}

SELECT
    JSON_PAYLOAD:video_id::STRING AS video_id,
    JSON_PAYLOAD:cleaned_text::STRING AS cleaned_text,
    JSON_PAYLOAD:tech_terms AS tech_terms_array,
    JSON_PAYLOAD:book_names AS book_names_array,
    INSERTED_AT
FROM DS5111_DB.PUBLIC.RAW_TRANSCRIPTS
