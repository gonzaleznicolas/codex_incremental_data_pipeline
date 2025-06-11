from finance_pipeline.database import get_engine
from sqlalchemy import inspect


def test_get_engine_creates_table(tmp_path):
    engine = get_engine(tmp_path / "test.db")
    inspector = inspect(engine)
    assert "prices" in inspector.get_table_names()
