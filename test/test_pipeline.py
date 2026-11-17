import pandas as pd
from src import PROCESSED_DATA_PATH

def test_clean_dataset_integrity():
    df = pd.read_csv(PROCESSED_DATA_PATH)

    #1. Primary Key Uniqueness
    assert df['Order_ID'].is_unique, "Duplicate Order_IDs found"
    assert df['Order_ID'].isna().sum() == 0, "Null Order_IDs found"

    #2. Domain Bounds
    assert df['Customer_Age'].between(18,100).all(), "Invalid Age outside 18-100"
    assert (df['Order_Amount'] > 0) .all(), "Negetive/Zero order amounts"
    assert (df['Order_Amount']<= 1_00_000).all(), "High Outlier order amounts"

    #3. DateTime Integrity
    dates = pd.to_datetime(df['Order_Date'].dropna())
    assert (dates <= '2026-11-01').all(), "Future Dates Detected"

    #4. Indicator columns consistency
    assert (df['Has_Email'] == df['Customer_Email'].notna()).all(), "Email indicator column inconsistency"
