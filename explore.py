import pandas as pd
import sqlite3

def run_exploration():
    """Lê os dados do banco de dados e gera insights."""
    print("=== Relatório de Exploração de Dados ===\n")
    
    try:
        # Lendo do Banco de Dados (Simulando consumo de dados estruturados)
        conn = sqlite3.connect('db/crypto_vault.sqlite')
        df = pd.read_sql_query("SELECT * FROM cryptos", conn)
        conn.close()

        # Insight 1: Ranking por Preço
        print("1. As 5 criptomoedas mais caras do Top 50:")
        print(df.nlargest(5, 'current_price')[['name', 'current_price']])
        
        # Insight 2: Média de Volatilidade
        avg_change = df['price_change_percentage_24h'].mean()
        print(f"\n2. Variação média de preço nas últimas 24h: {avg_change:.2f}%")
        
        # Insight 3: Dominância de Mercado (Top 3)
        total_market_cap = df['market_cap'].sum()
        df['dominance'] = (df['market_cap'] / total_market_cap) * 100
        print("\n3. Dominância de Mercado (em relação ao Top 50):")
        print(df.nlargest(3, 'dominance')[['name', 'dominance']])

    except Exception as e:
        print(f"Erro ao explorar dados: {e}. Certifique-se de rodar o pipeline.py primeiro.")

if __name__ == "__main__":
    run_exploration()
