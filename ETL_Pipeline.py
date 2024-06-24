import requests
from datetime import datetime
import pandas as pd
import sqlite3
import os

API_KEY = 'Get-Your-Own-API-Key'
SYMBOLS = [
    "AAPL",   # Apple Inc.
    "MSFT",   # Microsoft Corporation
    "GOOGL",  # Alphabet Inc. (Google)
    "AMZN",   # Amazon.com Inc.
    "TSLA",   # Tesla Inc.
    "META",   # Meta Platforms Inc. (formerly Facebook)
    "NFLX",   # Netflix Inc.
    "NVDA",   # NVIDIA Corporation
    "INTC",   # Intel Corporation
    "AMD",    # Advanced Micro Devices Inc.
]

def fetch_quote(symbol):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'c' in data:
            return data
        else:
            print(f"Error fetching quote for {symbol}: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error for {symbol}: {e}")
        return None

# Fetch quotes for all symbols
def extract_stock_data(symbols):
    all_quotes = {}
    for symbol in symbols:
        print(f"Fetching quote for {symbol}...")
        quote_data = fetch_quote(symbol)
        if quote_data:
            all_quotes[symbol] = quote_data
    df = pd.DataFrame.from_dict(all_quotes, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Symbol', 'c': 'Current_Price','d': 'Change','dp': 'Percent_Change', 'h': 'High_Price', 'l': 'Low_Price', 'o': 'Open_Price', 'pc': 'Previous_Close'}, inplace=True)
    df['timestamp'] = pd.Timestamp.now()
    return df

# Extract data
stock_data_df = extract_stock_data(SYMBOLS)
stock_data_df.to_csv('stock.csv')

def transform_stock_data(df):
    # Drop the 't' column
    if 't' in df.columns:
        df = df.drop(columns=['t'])
    
    # Convert 'timestamp' to datetime and extract year, month, day, and time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['Year'] = df['timestamp'].dt.year
    df['Month'] = df['timestamp'].dt.month
    df['Day'] = df['timestamp'].dt.day
    df['Time'] = df['timestamp'].dt.strftime('%H:%M:%S')
    
    # Drop the original 'timestamp' column
    df = df.drop(columns=['timestamp'])
    
    # Drop rows with NaN values
    df = df.dropna()
    
    return df

# Transform data
transformed_stock_data_df = transform_stock_data(stock_data_df)


def load_data_to_sqlite(df, db_name='Database/stock_data.db', table_name='stock_quotes'):
    
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(db_name), exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            Symbol TEXT,
            Current_Price REAL,
            Change REAL,
            Percent_Change REAL,
            High_Price REAL,
            Low_Price REAL,
            Open_Price REAL,
            Previous_Close REAL,
            Year INTEGER,
            Month INTEGER,
            Day INTEGER,
            Time TEXT
        )
    ''')
    
    # Insert data into table
    df.to_sql(table_name, conn, if_exists='append', index=False)
    
    # Commit and close connection
    conn.commit()
    conn.close()

# Load data
load_data_to_sqlite(transformed_stock_data_df)