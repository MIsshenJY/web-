"""
认证相关的 Pydantic Schema
"""
from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    """用户登录请求"""
    name: str
    password: str


class UserRegister(BaseModel):
    """用户注册请求"""
    name: str
    password: str


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    name: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """登录成功返回的 Token"""
    token: str
    user: UserResponse


class UserInfo(BaseModel):
    """用户信息"""
    id: int
    name: str
    dead_time: str


class AuthResponse(BaseModel):
    """认证响应"""
    code: int
    message: str
    data: Optional[dict] = None
