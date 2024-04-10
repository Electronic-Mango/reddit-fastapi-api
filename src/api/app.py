"""
Module responsible for API itself, registers all routers.
"""

from fastapi import Depends, FastAPI

from api.routes import router
from api.security import security_enabled, verify_api_key


def prepare_api() -> FastAPI:
    """Prepare and configure API, register all routers"""
    api = FastAPI(dependencies=[Depends(verify_api_key)] if security_enabled() else None)
    api.include_router(router)
    # TODO: Add basic auth middleware
    return api
