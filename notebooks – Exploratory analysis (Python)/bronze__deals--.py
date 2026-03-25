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
CREATE OR REPLACE TABLE bronze__deals AS
SELECT 
    deal_id,
    account_id,
    owner_user_id,
    pipeline_id,
    current_stage_id,
    status,
    created_at,
    closed_at,
    last_stage_changed_at,
    amount,
    currency,
    country_code,
    source_system,
FROM raw__deals,
""")

print ( "Created bronze_deals table")

con.close()