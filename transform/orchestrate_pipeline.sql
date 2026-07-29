-- Master Pipeline Orchestrator
USE ROLE DS5111_STUDENT_ROLE;
USE DATABASE DS5111_DB;
USE SCHEMA XDY6SG;
USE WAREHOUSE DS5111_WH;

EXECUTE IMMEDIATE FROM @XDY6SG.DS5111_GIT_STAGE/branches/LAB09_gitops_snowflake/transform/01_stg_youtube_transcripts.sql;
EXECUTE IMMEDIATE FROM @XDY6SG.DS5111_GIT_STAGE/branches/LAB09_gitops_snowflake/transform/02_dim_videos.sql;
EXECUTE IMMEDIATE FROM @XDY6SG.DS5111_GIT_STAGE/branches/LAB09_gitops_snowflake/transform/03_fct_entities.sql;
