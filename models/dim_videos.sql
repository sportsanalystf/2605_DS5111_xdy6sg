{{ config(materialized='table') }}

SELECT
    video_id,
    cleaned_text,
    ARRAY_SIZE(tech_terms_array) AS tech_term_count,
    ARRAY_SIZE(book_names_array) AS book_name_count,
    ARRAY_SIZE(SPLIT(cleaned_text, ' ')) AS word_count,
    LENGTH(cleaned_text) AS char_count,
    INSERTED_AT AS processed_at
FROM {{ ref('stg_youtube_transcripts') }}
