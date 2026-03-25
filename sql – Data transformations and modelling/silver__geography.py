import duckdb
import os
# import pandas as pd

# --- connect to duckdb file

con = duckdb.connect(
    os.path.join(
        os.path.dirname(__file__),
        ".." ,
        "product_analytics_light.db"
    )
)

# ---- Path to Excel file ----
# excel_path = os.path.join(
#    os.path.dirname(__file__),
#    ".." ,
#   "raw__geography--.xlsx"
# )

# --- Load Excel into DataFrame ---
# df = pd.read_excel(excel_path, sheet_name=0)

# --- Register Dataframe as temp view ---
# con.register("raw_geography_df", df)
# ---- create Bronze Table (raw structure, no transformations) ---

con.execute("""
CREATE OR REPLACE TABLE silver__geography AS
WITH base AS (
    SELECT 
        UPPER(TRIM(country_code))  AS country_code,
        country_name,
        region,	
        market,	
        currency,
        sales_region
FROM bronze__geography
),

deduped AS (
    SELECT
        *, 
        ROW_NUMBER() OVER(
            PARTITION BY country_code
            ORDER BY country_name
        ) AS rn
    FROM base
) 

SELECT 
    country_code,
    country_name,
    region,


    -- Fill a small known gap from the raw sheet
     CASE
         WHEN country_code = 'UK' AND market is NULL THEN 'UKI'
         ELSE market
    END AS market,  

    currency,
    sales_region,
FROM deduped
WHERE rn = 1;       

""")

print ( "Created silver__geography table")

con.close()