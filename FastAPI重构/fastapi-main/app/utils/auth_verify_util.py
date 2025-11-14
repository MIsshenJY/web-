"""
JWT 认证工具（适配 FastAPI）
基于 authlib 的 JWT 实现
"""
import datetime
from typing import Optional

from authlib.jose import jwt, JoseError
from app.core.config import get_config_value


def generate_auth_token(user_id: int, name: str, effective_time: int = 30, **kwargs) -> str:
    """
    生成用于登录认证的JWT（json web token）

    Args:
        user_id: 用户ID
        name: 用户名
        effective_time: token的有效时长（天）
        **kwargs: 额外数据

    Returns:
        JWT token 字符串
    """
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = get_config_value('SECRET_KEY', 'secret-key')
    # 待签名的数据负载
    data = {
        'id': user_id,
        'name': name,
        'dead_time': (datetime.datetime.now() + datetime.timedelta(days=effective_time)).strftime("%Y-%m-%d")
    }
    data.update(**kwargs)
    token = jwt.encode(header=header, payload=data, key=key)
    return token.decode()


def parse_user_from_token(token: str) -> dict:
    """
    从token中解析用户信息

    Args:
        token: JWT token

    Returns:
        用户数据字典
    """
    key = get_config_value('SECRET_KEY', 'secret-key')
    data = dict(jwt.decode(token, key))
    return data


def validate_token(token: str) -> bool:
    """
    验证token的有效性

    Args:
        token: JWT token

    Returns:
        是否有效
    """
    key = get_config_value('SECRET_KEY', 'secret-key')
    try:
        data = jwt.decode(token, key)
        dead_time = data['dead_time']
        if datetime.datetime.strptime(dead_time, "%Y-%m-%d") > datetime.datetime.now():
            return True
        return False
    except JoseError:
        return False
