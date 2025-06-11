# Finance Data Pipeline

This project fetches historical stock data using `yfinance`, computes moving averages,
and stores the results in a SQLite database.

Database interactions are handled through SQLAlchemy. The pipeline can be run with:

```bash
python -m finance_pipeline.main
```
