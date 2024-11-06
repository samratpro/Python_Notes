from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config.config import Config

security = HTTPBearer()


def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Authenticates by credentials.
    Args:
        credentials provided by the user.
    Returns:
        str: The secret key if the authentication is successful.
    Raises:
        HTTPException: If the provided secret key is incorrect.
    """
    correct_secret_key = Config.SECRET_KEY
    if credentials.credentials != correct_secret_key:
        raise HTTPException(
            status_code=401,
            detail="Incorrect secret key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
