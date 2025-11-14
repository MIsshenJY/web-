"""
配置加载模块
从 YAML 配置文件中加载应用配置
"""
import os
import yaml
from typing import Dict, Any


def load_config(env: str = None) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        env: 环境名称（DEVELOPMENT, PRODUCTION），如果不传则使用 ENV 环境变量

    Returns:
        配置字典
    """
    # 如果未指定环境，则使用环境变量或默认为 PRODUCTION
    if env is None:
        env = os.getenv('ENV', 'PRODUCTION')

    # 构建配置文件路径
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')

    # 读取配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    # 获取指定环境的配置，如果不存在则使用 COMMON
    if env in config_data:
        return config_data[env]
    else:
        return config_data.get('COMMON', {})


def get_database_url() -> str:
    """
    获取数据库连接URL

    Returns:
        数据库连接字符串
    """
    config = load_config()
    return config.get('SQLALCHEMY_DATABASE_URI', '')


def get_config_value(key: str, default: Any = None) -> Any:
    """
    获取配置项的值

    Args:
        key: 配置项名称
        default: 默认值

    Returns:
        配置值
    """
    config = load_config()
    return config.get(key, default)
