# crypto-data-pipeline

A data engineering pipeline that ingests real-time cryptocurrency market data from the [CoinGecko API](https://www.coingecko.com/en/api), transforms the raw JSON response into a structured format, and stores the results in both **CSV** and **SQLite** for further analysis.

Built as a portfolio project to demonstrate core data engineering concepts: **ingestion → transformation → storage → exploration**.

---

## Motivation

Financial market data is one of the most common and challenging data sources in the industry — it's high-frequency, nested and requires careful transformation before it becomes useful. This project replicates a real-world data pipeline workflow using the CoinGecko public API, with no authentication required, and a stack close to what is used in professional data engineering environments.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| HTTP Requests | `requests` |
| Data Transformation | `pandas` |
| Storage | `sqlite3` + CSV |
| Environment | `python-dotenv` |

---

## Project Structure

```
crypto-data-pipeline/
│
├── data/
│   └── crypto_data.csv        # Output CSV file
│
├── db/
│   └── crypto.db              # SQLite database
│
├── pipeline.py                # Main pipeline script
├── explore.py                 # Data exploration & insights
├── requirements.txt
└── README.md
```

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Heitit/crypto-data-pipeline.git
cd crypto-data-pipeline
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the pipeline**
```bash
python pipeline.py
```

**4. Explore the data**
```bash
python explore.py
```

The pipeline fetches current market data for the top cryptocurrencies, transforms the response into a clean DataFrame, saves it to `data/crypto_data.csv` and inserts it into a `market` table in `db/crypto.db`.

---

## Sample Insights

After running `explore.py`, the script prints:

- Top 5 coins by market cap at time of ingestion
- Coins with highest 24h price drop
- Coins with highest 24h trading volume

---

## What I Learned

- How to consume and parse a JSON REST API response with `requests`
- How to reshape nested JSON into flat tabular data using `pandas`
- How to persist structured data in both CSV and a relational database with `sqlite3`
- The importance of separating ingestion, transformation and storage layers — a pattern used in tools like **Apache Airflow** and **Kedro**
- How financial time-series data maps to real-world data engineering challenges around freshness, consistency and schema design

---

## Next Steps

- [ ] Schedule the pipeline to run every hour using `schedule` or Airflow
- [ ] Track historical price changes over time by appending runs to the database
- [ ] Build a simple dashboard with `matplotlib` or `streamlit`
- [ ] Migrate storage to a cloud database (e.g. AWS RDS or BigQuery)

---

## Contact

**Heitor Antonio Marques Júnior**
[LinkedIn](https://www.linkedin.com/in/heitormarquesjunior) • [GitHub](https://github.com/Heitit) • heitor.hantonio2@gmail.com
