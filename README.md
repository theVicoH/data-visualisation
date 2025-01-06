# data-visualisation

## Set up locally
```
# windows
python -m venv ./.venv
.\.venv\Scripts\activate
pip install -r ./requirements.txt
flask run

# macOS/Linux
python3 -m venv .venv
. .venv/bin/activate
pip install -r ./requirements.txt
flask run
```

## Run the linter
```bash
python -m pylint .
```