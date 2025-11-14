"""
FastAPI 安全认证模块
使用依赖注入实现 JWT 认证
"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.auth_verify_util import validate_token, parse_user_from_token


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    FastAPI 依赖：获取当前登录用户

    Args:
        credentials: HTTP Bearer Token

    Returns:
        用户信息字典

    Raises:
        HTTPException: token 无效时抛出 401 错误
    """
    token = credentials.credentials
    if not validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = parse_user_from_token(token)
    return user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """
    FastAPI 依赖：可选的用户认证
    用于某些需要认证但不强制认证的接口

    Args:
        credentials: HTTP Bearer Token（可选）

    Returns:
        用户信息字典或 None
    """
    if not credentials:
        return None
    token = credentials.credentials
    try:
        if validate_token(token):
            return parse_user_from_token(token)
    except Exception:
        pass
    return None


def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    确保用户已登录的装饰器

    Args:
        credentials: HTTP Bearer Token

    Raises:
        HTTPException: token 无效时抛出 401 错误
    """
    token = credentials.credentials
    if not validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401 Unauthorized Access",
            headers={"WWW-Authenticate": "Bearer"},
        )
