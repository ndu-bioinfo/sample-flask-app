# Agent Rules

## Python Environment

All Python dependencies must be installed into a local virtual environment and sourced from there:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Always use `.venv` as the virtual environment directory name
- Always activate the virtual environment before running any Python commands
- Do not install packages globally or with `--user`
