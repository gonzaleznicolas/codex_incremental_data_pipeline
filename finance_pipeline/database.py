from pathlib import Path
from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    ForeignKey,
    create_engine,
    select,
)
from sqlalchemy.engine import Engine

DB_PATH = Path("data.db")

metadata = MetaData()

stocks = Table(
    "stocks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("symbol", String, unique=True, index=True),
)

prices = Table(
    "prices",
    metadata,
    Column("date", String),
    Column("open", Float),
    Column("high", Float),
    Column("low", Float),
    Column("close", Float),
    Column("volume", Float),
    Column("dividends", Float),
    Column("stock_splits", Float),
    Column("stock_id", Integer, ForeignKey("stocks.id")),
    Column("price_over_ma30", Float),
)


def get_engine(db_path: Path = DB_PATH) -> Engine:
    """Return a SQLAlchemy engine connected to the given database path."""
    engine = create_engine(f"sqlite:///{db_path}")
    metadata.create_all(engine)
    return engine
