import requests
import pandas as pd
import sqlite3
import os
from datetime import datetime

# --- CONFIGURATION ---
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": "false"
}
DB_PATH = "data/crypto_vault.sqlite"
CSV_PATH = "data/raw_data.csv"

def extract_data():
    """Fetches data from the Public CoinGecko API."""
    print("Step 1: Extracting data from CoinGecko API...")
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status() # Raises an error for bad status codes
        return response.json()
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None

def transform_data(raw_data):
    """Cleans and structures the JSON response into a Pandas DataFrame."""
    print("Step 2: Transforming data...")
    df = pd.DataFrame(raw_data)
    
    # Selecting specific columns (Data Engineering: Schema selection)
    columns_to_keep = [
        'id', 'symbol', 'name', 'current_price', 
        'market_cap', 'total_volume', 'price_change_percentage_24h'
    ]
    df = df[columns_to_keep]
    
    # Adding a 'load_timestamp' (Data Engineering: Audit columns)
    df['extracted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Rounding prices for cleanliness
    df['current_price'] = df['current_price'].round(2)
    
    return df

def load_data(df):
    """Saves data to CSV and SQLite."""
    print("Step 3: Loading data to storage...")
    
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    # 1. Save to CSV
    df.to_csv(CSV_PATH, index=False)
    print(f" - Data saved to {CSV_PATH}")
    
    # 2. Save to SQLite
    conn = sqlite3.connect(DB_PATH)
    # if_exists='replace' ensures we don't duplicate on every run for this beginner project
    df.to_sql('top_cryptos', conn, if_exists='replace', index=False)
    conn.close()
    print(f" - Data saved to {DB_PATH}")

def explore_insights(df):
    """Prints 3 basic insights to the console."""
    print("\n--- DATA INSIGHTS ---")
    
    # Insight 1: Total Market Cap of top 50
    total_mcap = df['market_cap'].sum()
    print(f"1. Total Market Cap of Top 50: ${total_mcap:,.2f}")
    
    # Insight 2: Top Gainer in last 24h
    top_gainer = df.loc[df['price_change_percentage_24h'].idxmax()]
    print(f"2. Top 24h Gainer: {top_gainer['name']} ({top_gainer['price_change_percentage_24h']:.2f}%)")
    
    # Insight 3: Average Price of Top 50
    avg_price = df['current_price'].mean()
    print(f"3. Average Price of Top 50 coins: ${avg_price:.2f}")

def main():
    # Execute the ETL process
    data = extract_data()
    if data:
        df_cleaned = transform_data(data)
        load_data(df_cleaned)
        explore_insights(df_cleaned)
        print("\nETL Pipeline completed successfully!")

if __name__ == "__main__":
    main()
