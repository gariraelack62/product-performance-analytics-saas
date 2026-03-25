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
CREATE OR REPLACE TABLE bronze__product_events AS
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
    country_code,
    event_properties,
    is_test_event,
    source_system,        
FROM raw__product_events,
""")

print ( "Created bronze__product_events table")

con.close()