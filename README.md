# Finance Data Pipeline

This project fetches historical stock data using `yfinance`, computes moving averages,
and stores the results in a SQLite database.

To ensure moving averages are accurate from the first requested date, the pipeline
fetches an additional 30 days of historical prices prior to the configured start
date.

Database interactions are handled through SQLAlchemy. The pipeline can be run with:

```bash
python -m finance_pipeline.main
```
