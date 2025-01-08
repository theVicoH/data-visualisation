# data-visualisation

## API

### Set up locally
```
# windows
cd api
python -m venv ./.venv
.\.venv\Scripts\activate
pip install -r ./requirements.txt
flask run

# macOS/Linux
cd api
python3 -m venv .venv
. .venv/bin/activate
pip install -r ./requirements.txt
flask run
```

### Run the linter
```bash
python -m pylint .
```

### API Documentation

To access api documentation go to http://127.0.0.1:5000/apidocs

## Client

### Set up locally
Before running the development server, create a `.env` file in the root of the client directory and add the necessary environment variables.
```
# .env
API_URL="http://127.0.0.1:5000"
```
```
cd client
pnpm install
pnpm dev
```

To access client development server go to http://localhost:3000
