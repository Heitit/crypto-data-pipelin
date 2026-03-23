import requests
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Configurações do Pipeline
API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": "false"
}
DB_PATH = "db/crypto_vault.sqlite"
CSV_PATH = "data/crypto_data.csv"

def extract():
    """Extrai dados brutos da API CoinGecko."""
    print("Iniciando Extração...")
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro na extração: {e}")
        return None

def transform(raw_data):
    """Limpa e estrutura os dados brutos."""
    print("Iniciando Transformação...")
    df = pd.DataFrame(raw_data)
    
    # Seleção de colunas relevantes (Schema Enforcement)
    cols = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h']
    df = df[cols]
    
    # Adicionando metadados de processamento
    df['extracted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Arredondamento para facilitar a leitura
    df['current_price'] = df['current_price'].round(2)
    
    return df

def load(df):
    """Salva os dados em CSV e Banco de Dados SQLite."""
    print("Iniciando Carga...")
    
    # Garantir que as pastas existem
    os.makedirs('data', exist_ok=True)
    os.makedirs('db', exist_ok=True)
    
    # Salvar em CSV
    df.to_csv(CSV_PATH, index=False)
    
    # Salvar em SQLite
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('cryptos', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Sucesso! Dados salvos em {CSV_PATH} e {DB_PATH}")

if __name__ == "__main__":
    data = extract()
    if data:
        df_transformed = transform(data)
        load(df_transformed)
