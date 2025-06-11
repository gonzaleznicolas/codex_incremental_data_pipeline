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
   pytest -q
   ```
7. Execute the data pipeline:
   ```bash
   python -m finance_pipeline.main
   ```

Use Cursor IDE to run these commands in its integrated terminal.
