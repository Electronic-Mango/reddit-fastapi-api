"""
Module responsible for authorization of users.
"""

from secrets import compare_digest

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from settings import API_AUTHORIZATION_HEADER_NAME, API_AUTHORIZATION_HEADER_VALUE

api_key_header = APIKeyHeader(name=API_AUTHORIZATION_HEADER_NAME or "")


def verify_api_key(api_key_header_value: str = Security(api_key_header)):
    if not compare_digest(api_key_header_value, API_AUTHORIZATION_HEADER_VALUE):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid API key")


def security_enabled() -> bool:
    return API_AUTHORIZATION_HEADER_NAME and API_AUTHORIZATION_HEADER_VALUE
