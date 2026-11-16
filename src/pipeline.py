import pandas as pd

def load_raw_data(filepath):
    df = pd.read_csv(filepath, dtype=str)
    return df

def standardize_strings(df):
    df=df.str.strip()