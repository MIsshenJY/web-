"""
视频相关的 Pydantic Schema
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class VodListItem(BaseModel):
    """视频列表项"""
    vod_id: int
    vod_pic: Optional[str] = None
    vod_name: Optional[str] = None
    vod_remarks: Optional[str] = None


class VodListResponse(BaseModel):
    """视频列表响应"""
    code: int
    message: str
    data: List[VodListItem]


class VodDetailResponse(BaseModel):
    """视频详情响应"""
    code: int
    data: Optional[Dict[str, Any]] = None
    msg: str


class VodDetailOut(BaseModel):
    """视频详情输出（部分字段）"""
    id: int
    vod_id: int
    vod_name: Optional[str] = None
    vod_pic: Optional[str] = None
    vod_content: Optional[str] = None
    vod_play_url: Optional[Dict[str, str]] = None
    vod_time: Optional[str] = None
    vod_actor: Optional[str] = None
    vod_director: Optional[str] = None
    vod_area: Optional[str] = None
    vod_year: Optional[str] = None
    vod_remarks: Optional[str] = None

    class Config:
        from_attributes = True
