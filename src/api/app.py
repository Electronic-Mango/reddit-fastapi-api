"""
Module responsible for API itself, registers all blueprints.
"""

from fastapi import FastAPI

from api.routes import subreddit_router, user_router


def prepare_api() -> FastAPI:
    """Prepare and configure API, register all blueprints"""
    api = FastAPI(docs_url="/")
    api.include_router(subreddit_router)
    api.include_router(user_router)
    # TODO: Add basic auth middleware
    return api
