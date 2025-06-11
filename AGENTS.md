# Agent instructions
Always start by reading the `README.md` file to get context on what the code does.
Always `pip install -q -r requirements.txt` as that will be necessary in order to run tests and execute the data pipeline.
Always add unit tests in the `/tests` directory for any feature you implement.
After making code changes, always run `PYTHONPATH=. pytest -q` to ensure all the unit tests pass.
After making code changes, always run `python -m finance_pipeline.main` to ensure the pipeline successfully runs end to end.
Always end by updating the `README.md` file (if necessary) to update the documentation on what the code does.