# Finance Data Pipeline

This project fetches historical stock data using `yfinance`, computes the ratio of
the closing price to its 30-day moving average, and stores the results in a SQLite
database. It also calculates the Bollinger Band percent (`bb_pct`) based on a
30-day window. Stock symbols are stored once in a `stocks` table and the `prices`
table references them via foreign keys. The pipeline assigns a `suggested_position`
to each price row based on both the `price_over_ma30` ratio and the Bollinger
Band percent (`bb_pct`). Each indicator makes a recommendation and the final
position is "Long" or "Short" only when they agree; otherwise the row is marked
as "Cash". Allowed positions are stored in the `position` table and are "Long",
"Short" and "Cash".

To ensure the moving average is accurate from the first requested date, the pipeline
fetches an additional 30 days of historical prices prior to the configured start
date.

Database interactions are handled through SQLAlchemy. The pipeline can be run with:

```bash
python -m finance_pipeline.main
```
