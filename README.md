# Finance Data Pipeline

This project fetches historical stock data using `yfinance`, computes the ratio of
the closing price to its 30-day moving average, and stores the results in a SQLite
database. Stock symbols are stored once in a `stocks` table and the `prices` table
references them via foreign keys. The pipeline also assigns a `suggested_position`
to each price row based on the `price_over_ma30` ratio. Allowed positions are
stored in the `position` table and are "Long", "Short" and "Cash".

To ensure the moving average is accurate from the first requested date, the pipeline
fetches an additional 30 days of historical prices prior to the configured start
date.

Database interactions are handled through SQLAlchemy. The pipeline can be run with:

```bash
python -m finance_pipeline.main
```
