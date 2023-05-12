# Test task for 'Interesnee'


### Testing difficulties
Failed to implement mock authorization via Google and VK api.

## Virtual environment
run the following commands

    python -m venv venv

    pip install -r requirements.txt

## Hooks
run

    pre-commit install

in virtual environment to activate hooks

If you work on Windows remove 'run-tests' hook from pre-commit-config.yaml

In case you work on Linux uncomment 'run-tests' hook otherwise tests will not run before the commit.
