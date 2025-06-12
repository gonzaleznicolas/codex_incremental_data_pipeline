# Finance Data Pipeline

This project fetches historical stock data using `yfinance`, computes the ratio of
the closing price to its 30-day moving average, and stores the results in a SQLite
database. Stock symbols are stored once in a `stocks` table and the `prices` table
references them via a foreign key.

To ensure the moving average is accurate from the first requested date, the pipeline
fetches an additional 30 days of historical prices prior to the configured start
date.

Database interactions are handled through SQLAlchemy. The pipeline can be run with:

```bash
python -m finance_pipeline.main
```
