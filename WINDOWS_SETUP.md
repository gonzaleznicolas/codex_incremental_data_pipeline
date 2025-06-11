# Running the Data Pipeline on Windows using Cursor IDE

This project requires Python 3.9 or newer. The steps below show how to run the pipeline natively on Windows using a virtual environment.

1. Install [Python for Windows](https://www.python.org/downloads/windows/).
2. Clone this repository using Cursor IDE or Git and open a terminal in the project directory.
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment. In **Command Prompt** run:
   ```cmd
   .venv\Scripts\activate.bat
   ```
   Or in **PowerShell** run:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
5. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. (Optional) run the unit tests:
   ```bash
   python -m pytest -q
   ```
7. Execute the data pipeline:
   ```bash
   python -m finance_pipeline.main
   ```

8. Inspect the SQLite database created by the pipeline (optional):
   The pipeline writes its results to `data.db` in the project directory. You
   can examine this file using the `sqlite3` CLI that ships with Python:
   ```bash
   python -m sqlite3 data.db
   ```
   From the prompt you can list tables with `.tables` and query data, e.g.:
   ```sql
   SELECT COUNT(*) FROM prices;
   .quit
   ```

Use Cursor IDE to run these commands in its integrated terminal.
