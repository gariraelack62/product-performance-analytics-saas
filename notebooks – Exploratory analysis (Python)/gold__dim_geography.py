import duckdb, os


con = duckdb.connect(
    os.path.join(
        os.path.dirname(__file__),
        ".." ,
        "product_analytics_light.db"
    )
)

con.execute("""
CREATE OR REPLACE TABLE gold__dim_geography AS
      
SELECT 
    country_code        AS CountryCode,
    country_name        AS CountryName,
    region              AS Region,
    market              AS Market,  
    currency            AS Currency,
    sales_region        AS SalesRegion
FROM silver__geography      
ORDER BY CountryCode
""")

print ( "Created gold__dim_geography table")

con.close()