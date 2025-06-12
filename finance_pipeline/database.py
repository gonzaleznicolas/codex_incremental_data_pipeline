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
    insert,
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

# Table storing allowed positions for trading signals
position = Table(
    "position",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
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
    Column("suggested_position", Integer, ForeignKey("position.id")),
)


def get_engine(db_path: Path = DB_PATH) -> Engine:
    """Return a SQLAlchemy engine connected to the given database path."""
    engine = create_engine(f"sqlite:///{db_path}")
    metadata.create_all(engine)
    # Ensure the default positions exist
    with engine.begin() as conn:
        existing = list(conn.execute(select(position.c.name)))
        if not existing:
            conn.execute(
                insert(position),
                [{"name": "Long"}, {"name": "Short"}, {"name": "Cash"}],
            )
    return engine
