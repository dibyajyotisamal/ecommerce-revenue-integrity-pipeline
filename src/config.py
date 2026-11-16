from datetime import datetime

RAW_DATA_PATH = 'data/raw/ecommerce_orders_raw.csv'
CLEAN_DATA_PATH = "data/processed/ecommerce_orders/clean.csv"

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