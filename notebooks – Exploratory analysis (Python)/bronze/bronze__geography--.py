import duckdb
import os
import pandas as pd

# --- connect to duckdb file

con = duckdb.connect(
    os.path.join(
        os.path.dirname(__file__),
        ".." ,
        "product_analytics_light.db"
    )
)

# ---- Path to Excel file ----
excel_path = os.path.join(
    os.path.dirname(__file__),
    ".." ,
    "raw__geography--.xlsx"
)

# --- Load Excel into DataFrame ---
df = pd.read_excel(excel_path, sheet_name=0)

# --- Register Dataframe as temp view ---
con.register("raw_geography_df", df)
# ---- create Bronze Table (raw structure, no transformations) ---

con.execute("""
CREATE OR REPLACE TABLE bronze__geography AS
SELECT 
country_code,
country_name,
region,	
market,	
currency,
sales_region
FROM raw_geography_df
""")

print ( "Created bronze__geography table")

con.close()