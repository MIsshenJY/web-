"""
SQLAlchemy 基础类和会话管理
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Type

Base = declarative_base()


def init_db():
    """
    初始化数据库，创建所有表（仅在需要时使用）
    """
    from app.models.database import engine
    Base.metadata.create_all(bind=engine)
