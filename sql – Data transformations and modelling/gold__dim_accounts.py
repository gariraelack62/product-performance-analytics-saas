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

# ---- create Gold Table (Business Ready) ---

con.execute("""
CREATE OR REPLACE TABLE gold__dim_accounts AS
SELECT 
    account_id              AS AccountId,
            
    -- Core Descriptors
    account_name            AS AccountName,
    segment                 AS Segment,
    industry                AS Industry,
    employee_band           AS EmployeeBand,
    acquisition_channel     AS AcquisitionChannel,

            
    -- Geography Attributes (Gold-level)
    country_code            AS CountryCode,
    country_name            AS CountryName,
    region                  AS Region,
    market                  AS Market,
    sales_region            AS SalesRegion,
    local_currency          AS LocalCurrency,


    account_status          AS AccountStatus,
    is_active_account       AS IsActiveAccount,
    has_trial               AS HasTrial,
                     
    -- Dates       
    created_at            AS CreatedAt,
    created_date            AS CreatedDate,
    trial_start_date        AS TrialStartDate,
    trial_end_date          AS TrialEndDate,
            

    -- Age metrics
    account_age_days        AS AccountAgeDays,
    account_age_bucket      AS AccountAgeBucket,
    trial_length_days       AS TrialLengthDays
    
FROM silver__accounts 
ORDER BY AccountID
""")

print ( "Created gold__dim_accounts table")

con.close()