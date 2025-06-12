from finance_pipeline.database import get_engine
from sqlalchemy import inspect


def test_get_engine_creates_table(tmp_path):
    engine = get_engine(tmp_path / "test.db")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "prices" in tables
    assert "stocks" in tables
    assert "position" in tables
    price_columns = {col['name'] for col in inspector.get_columns('prices')}
    assert 'stock_id' in price_columns
    assert 'suggested_position' in price_columns
