from datetime import datetime

#Define the import and export file paths
import pathlib
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / 'data' /'raw' / 'ecommerce_orders_data.csv'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed' / 'ecommerce_orders_clean.csv'

#Data Extraction Cutoff (for future-date validation)
EXTRACTION_CUTOFF = datetime(2026,11,1)

#Domain Validation Bounds
MIN_VALID_AGE = 18
MAX_VALID_AGE = 100
MAX_VALID_ORDER_AMOUNT = 1_000_000.0 #Filters unrealistic extremely high values

#Regex & Category Mappings
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

PAYMENT_MAPPING = {
    "debitcard": "Debit Card",
    "debit card": "Debit Card",
    "cod": "Cash On Delivery",
    "cash on delivery": "Cash On Delivery",
    "upi": "UPI",
    "wallet": "Wallet",
    "net banking": "Net Banking",
    "credit card": "Credit Card",
    "crypto": "Crypto",
    "unknown": "Unknown",
}

RETURN_MAPPING = {
    "true": True,
    "yes": True,
    "1": True,
    "y": True,
    "returned": True,
    "false": False,
    "not returned": False,
    "n": False,
    "no": False,
    "0": False,
}