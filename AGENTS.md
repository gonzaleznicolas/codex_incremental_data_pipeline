# Agent instructions
Always start by running `pip install -q -r requirements.txt`
Always add unit tests in the `/tests` directory for any feature you implement.
After making code changes, always run `PYTHONPATH=. pytest -q` to ensure all the unit tests pass.
After making code changes, always run `python -m finance_pipeline.main` to ensure the pipeline successfully runs end to end.
