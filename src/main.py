"""
Main module, configures logging, initializes and serves the API.
"""

from logging import INFO, basicConfig

from uvicorn import run

from api.app import prepare_api
from settings import API_HOST, API_PORT

if __name__ == "__main__":
    basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=INFO)
    api = prepare_api()
    run(api, host=API_HOST, port=API_PORT)
