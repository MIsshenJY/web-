"""
统一响应格式工具模块
提供标准化的API响应格式化函数
"""
from typing import Any, Optional, Dict


def success_response(
    data: Any = None,
    message: str = 'Success',
    code: int = 200
) -> Dict[str, Any]:
    """
    生成成功的响应

    :param data: 响应数据
    :param message: 成功消息
    :param code: 状态码，默认为200
    :return: 格式化后的响应字典
    """
    return {
        'code': code,
        'message': message,
        'data': data
    }


def error_response(
    message: str = 'Error',
    code: int = 400,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    生成错误的响应

    :param message: 错误消息
    :param code: 错误状态码，默认为400
    :param data: 可选的错误详情数据
    :return: 格式化后的响应字典
    """
    return {
        'code': code,
        'message': message,
        'data': data
    }


# 常用的快速响应函数
def resp_ok(data: Any = None, message: str = 'Success') -> Dict[str, Any]:
    """快速创建成功响应"""
    return success_response(data=data, message=message, code=200)


def resp_created(data: Any = None, message: str = 'Created successfully') -> Dict[str, Any]:
    """快速创建已创建响应"""
    return success_response(data=data, message=message, code=201)


def resp_bad_request(message: str = 'Bad request', data: Optional[Any] = None) -> Dict[str, Any]:
    """快速创建错误请求响应"""
    return error_response(message=message, code=400, data=data)


def resp_unauthorized(message: str = 'Unauthorized', data: Optional[Any] = None) -> Dict[str, Any]:
    """快速创建未授权响应"""
    return error_response(message=message, code=401, data=data)


def resp_forbidden(message: str = 'Forbidden', data: Optional[Any] = None) -> Dict[str, Any]:
    """快速创建禁止访问响应"""
    return error_response(message=message, code=403, data=data)


def resp_not_found(message: str = 'Not found', data: Optional[Any] = None) -> Dict[str, Any]:
    """快速创建未找到响应"""
    return error_response(message=message, code=404, data=data)


def resp_server_error(message: str = 'Internal server error', data: Optional[Any] = None) -> Dict[str, Any]:
    """快速创建服务器错误响应"""
    return error_response(message=message, code=500, data=data)
