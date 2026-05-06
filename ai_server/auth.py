from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from .config import config

api_key_header = APIKeyHeader(name=config.API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == config.API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid or missing API Key. Access denied.",
    )
