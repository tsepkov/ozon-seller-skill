import os
import sys
import requests

BASE_URL = "https://api-seller.ozon.ru"


def _load_dotenv(path):
    try:
        with open(os.path.expanduser(path)) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except FileNotFoundError:
        pass


_load_dotenv("~/.hermes/.env")


def get_session() -> requests.Session:
    api_key = os.environ.get("OZON_API_KEY")
    client_id = os.environ.get("OZON_CLIENT_ID")

    missing = [name for name, val in [("OZON_API_KEY", api_key), ("OZON_CLIENT_ID", client_id)] if not val]
    if missing:
        print(f"Error: missing required environment variable(s): {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    session = requests.Session()
    session.headers.update({
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    })
    return session
