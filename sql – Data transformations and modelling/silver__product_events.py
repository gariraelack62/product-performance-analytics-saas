import duckdb
import os

# --- connect to duckdb file

con = duckdb.connect(
    os.path.join(
        os.path.dirname(__file__),
        ".." ,
        "product_analytics_light.db"
    )
)

# ---- create Bronze Table (raw structure, no transformations) ---

con.execute("""
CREATE OR REPLACE TABLE silver__product_events AS

WITH base AS (
    SELECT 
        event_id,
        event_name,
        user_id,
        account_id,
        deal_id,
        event_timestamp,
        ingested_at,
        event_date,
        platform,
        device_type,
        app_version,
        
        UPPER(country_code) AS country_code,
        event_properties,
        is_test_event,
        source_system
                    
FROM bronze__product_events
WHERE is_test_event = FALSE
),
            
enriched AS (
    SELECT
        *,
            
        CAST(event_timestamp AS DATE)    AS event_ts_date,
        DATE_TRUNC('month', event_timestamp)  AS event_ts_month,
            
        
        CASE 
            WHEN event_name LIKE '%login%' THEN 'AUTH'
            WHEN event_name LIKE '%pipeline%' OR event_name LIKE '%deal%' THEN 'PIPELINE'
            WHEN event_name LIKE '%activity%' OR event_name LIKE '%call%' OR event_name LIKE '%email%' THEN 'ACTIVITY'
            WHEN event_name LIKE '%workflow%' OR event_name LIKE '%automation%' THEN 'AUTOMATION'
            ELSE 'OTHER'
        END AS event_category,
        
        
        CASE 
            WHEN deal_id IS NOT NULL THEN TRUE
            ELSE FALSE
        END AS has_deal_context
    FROM base
)

SELECT
    event_id,
    event_name,
    event_category,
            
    user_id,
    account_id,
    deal_id,
    has_deal_context,

    event_timestamp,
    event_ts_date,
    event_ts_month,
    
    ingested_at,
    event_date,
    
    platform,
    device_type,
    app_version,
    country_code,
            
    event_properties,
    source_system
                      
FROM enriched;
            
""")

print ( "Created bronze__product_events table")

con.close()