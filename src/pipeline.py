import pandas as pd
from word2number import w2n
import numpy as np
from . import config



def load_raw_data():
    '''Load a csv file into pandas as DataFrame'''
    df = pd.read_csv(config.RAW_DATA_PATH, dtype=str)
    return df

def standardize_strings(df):
    '''Remove trailing spaces and turn whole dataset(except Order_ID) to lower case'''
    df=df.apply(lambda x:x.str.strip().str.lower())
    df.iloc[:,0]=df.iloc[:,0].str.upper()
    return df

def deduplicate_orders(df):
  '''Remove duplicate rows and rows with duplicate order_IDs'''
  #Removing duplicate rows
  print(f"Total Duplicated: {df.duplicated().sum()}")
  df = df.drop_duplicates(ignore_index=True)
  #Removing rows with duplicate Order_ID
  print(f"Duplicate Order_IDs: {df.duplicated(subset='Order_ID').sum()}")
  df = df.drop_duplicates(subset='Order_ID',ignore_index=True)
  return df


def _word_to_num(value : str):
   '''A function to turn a number in words to numeric value'''
   if pd.isna(value):
      return value
   try:
      return str(w2n.word_to_num(value))
   except:
      return value

def clean_customer_age(df):
   df['Customer_Age'] = df['Customer_Age'].apply(_word_to_num)
   df['Customer_Age'] = pd.to_numeric(df['Customer_Age'],errors='coerce')
   df.loc[df.query("Customer_Age > 100 or Customer_Age<18 ").index,'Customer_Age'] = np.nan
   df['Had_Age'] = df['Customer_Age'].notna()
   df['Customer_Age'] = df['Customer_Age'].fillna(np.round(df['Customer_Age'].median()))
   df['Customer_Age'] = df['Customer_Age'].astype('Int64')
   return df

def clean_order_amount(df):
   #We will remove the currency signs and commas and should be able to convert the column to numeric
   df['Order_Amount'] = df['Order_Amount'].replace('[$€£₹¥,]','',regex=True)
   df['Order_Amount'] = pd.to_numeric(df['Order_Amount'],errors='coerce')
   #Remove the unrealistic values(<0 | >1_00_000)
   df.loc[~df['Order_Amount'].between(0,1_00_000, inclusive='right'),'Order_Amount'] = np.nan
   df = df.dropna(subset='Order_Amount')
   return df

def clean_order_dates(df):
   #Change datatype
   df['Order_Date'] = pd.to_datetime(df['Order_Date'],format='mixed',errors='coerce')
   #Remove dates after the cutoff date
   df.loc[df['Order_Date'] > config.EXTRACTION_CUTOFF,'Order_Date'] = np.nan
   #Drop all NaN values
   df = df.drop(df.loc[df['Order_Date'].isna(),:].index)
   #Create a order_year, order_month, and order_day column
   df['Order_Year'] = df['Order_Date'].dt.year
   df['Order_Month'] = df['Order_Date'].dt.month_name()
   df['Order_Day'] = df['Order_Date'].dt.day_name()
   df['Order_Hour'] = df['Order_Date'].dt.hour
   return df

def clean_categories_and_boolean(df):
    #Use the Payment_mapping dict to standardize all values 
    df['Payment_Method'] = df['Payment_Method'].replace(config.PAYMENT_MAPPING)
    #Replace na values with unknown
    df['Payment_Method'] = df['Payment_Method'].fillna('Unknown')
    #Change the dtype from plain string to category
    df['Payment_Method'] = df['Payment_Method'].astype('category')

    #Clean the Is_Returned column
    df['Is_Returned'] = df['Is_Returned'].replace(config.RETURN_MAPPING)
    df['Is_Returned'] = df['Is_Returned'].astype('boolean')

    #Clean the Email column
    invalid_email_map = df['Customer_Email'].notna() & ~df['Customer_Email'].str.match(config.EMAIL_REGEX,na=False)
    df.loc[invalid_email_map,'Customer_Email'] = np.nan
    df['Has_Email'] = df['Customer_Email'].notna()

    return df

def export_csv(df):
   df.to_csv(config.PROCESSED_DATA_PATH,index=False)
