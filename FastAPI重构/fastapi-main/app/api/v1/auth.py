from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.models import User
from app.schemas.auth import UserLogin, TokenResponse, UserRegister, AuthResponse
from app.utils.auth_verify_util import generate_auth_token
from app.utils.response_util import resp_ok, resp_bad_request, resp_server_error

router = APIRouter(tags=["认证"])


@router.post("/auth/login", response_model=dict)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录

    Args:
        credentials: 登录凭证（用户名和密码）
        db: 数据库会话

    Returns:
        包含 token 和用户信息的响应
    """
    name = credentials.name
    password = credentials.password

    if not name or not password:
        return resp_bad_request("请输入账户和密码")

    user = db.query(User).filter(User.name == name).first()
    if not user:
        return resp_bad_request("登录失败, 账户或密码不正确")

    if not user.validate_password(password):
        return resp_bad_request("登录失败, 账户或密码不正确")

    try:
        token = generate_auth_token(user_id=user.id, name=name, effective_time=30)
        return resp_ok({
            "token": "jwt " + token,
            "user": {
                "id": user.id,
                "name": user.name
            }
        }, "Login successfully")
    except Exception as e:
        return resp_server_error("登录失败，请稍后重试")


@router.post("/auth/register", response_model=dict)
def register(
    credentials: UserRegister,
    db: Session = Depends(get_db)
):
    """
    用户注册

    Args:
        credentials: 注册信息（用户名和密码）
        db: 数据库会话

    Returns:
        注册结果
    """
    name = credentials.name
    password = credentials.password

    if not name or not password:
        return resp_bad_request("请输入账户和密码")

    existing_user = db.query(User).filter(User.name == name).first()
    if existing_user:
        return resp_bad_request("注册失败, 当前用户名已被注册, 请更换用户名")

    try:
        user = User(name=name)
        user.set_password(password)
        db.add(user)
        db.commit()
        return resp_ok(None, "注册成功, 请重新登录")
    except Exception as e:
        db.rollback()
        return resp_server_error("注册失败，请稍后重试")


@router.get("/auth/user", response_model=dict)
def get_user(
    token: str = Depends(lambda: None),  # 这里将会被 security 依赖替换
    credentials: Optional[str] = None
):
    """
    获取当前用户信息

    Args:
        credentials: JWT token

    Returns:
        用户信息
    """
    # 注意：在实际使用时，应该在 router 上使用依赖注入
    # 这里只是为了保持与 Flask 版本相同的接口
    from app.utils.auth_verify_util import parse_user_from_token

    # 从请求头获取 token（在实际应用中应该使用 FastAPI 的依赖注入）
    # 这里暂时留空，将会在外部处理
    return {"data": {"code": 200, "message": "获取用户信息成功", "data": {}}}
