"""
Module responsible for API itself, registers all blueprints.
"""

from fastapi import FastAPI

from api.routes import router


def prepare_api() -> FastAPI:
    """Prepare and configure API, register all blueprints"""
    api = FastAPI()
    api.include_router(router)
    # TODO: Add basic auth middleware
    return api
