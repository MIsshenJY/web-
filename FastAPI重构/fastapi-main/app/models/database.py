"""
SQLAlchemy 数据库配置
兼容 SQLAlchemy 1.4 版本，适配 FastAPI
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator

from app.core.config import get_database_url


# 创建数据库连接URL
database_url = get_database_url()

# 创建数据库引擎（兼容 SQLAlchemy 1.4）
engine_kwargs = {
    "pool_pre_ping": True,
    "pool_recycle": 1800,
}

# 处理 SQLite 的特殊情况（测试环境）
if database_url.startswith("sqlite"):
    engine_kwargs.update({
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    })

engine = create_engine(database_url, **engine_kwargs)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 数据库会话依赖，用于 FastAPI 的 Depends
def get_db() -> Generator:
    """
     FastAPI 依赖，创建数据库会话
    Yields:
        Session: 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
