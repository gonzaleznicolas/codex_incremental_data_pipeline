import sqlite3
from pathlib import Path

DB_PATH = Path("data.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS prices (
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    dividends REAL,
    stock_splits REAL,
    symbol TEXT,
    ma7 REAL,
    ma30 REAL
);
"""

def get_connection(db_path: Path = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    return conn
