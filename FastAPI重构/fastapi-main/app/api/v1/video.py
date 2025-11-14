import os
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from app.models.database import get_db
from app.models.models import MovDetail
from app.utils.response_util import resp_ok, resp_bad_request

router = APIRouter(tags=["视频"])

# 视频类型映射字典
mov_type_dict = {
    1: [1, 6, 7, 8, 9, 10, 11, 12, 20, 21, 22, 34],
    2: [2, 13, 14, 15, 16, 23, 24, 25],
    3: [3, 26, 27, 28, 29],
    4: [4, 30, 31, 32, 33, 22],
    5: [5, 17, 18],
    0: [1, 2, 3, 4, 5]
}


@router.get("/vod_list", response_model=dict)
def get_vod_list(
    page: int = Query(1, ge=1, description="页码"),
    movtype: int = Query(0, description="视频类型"),
    vod_area: Optional[str] = Query(None, description="视频地区"),
    vod_class: Optional[str] = Query(None, description="视频二级类型"),
    vod_year: Optional[str] = Query(None, description="视频年份"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """
    获取视频列表，支持多种筛选条件

    Args:
        page: 页码
        movtype: 视频类型 (一级类型)
        vod_area: 视频地区
        vod_class: 视频二级类型
        vod_year: 视频年份
        keyword: 搜索关键词
        db: 数据库会话

    Returns:
        视频列表
    """
    # 获取二级类型列表
    mov_type_list = mov_type_dict.get(movtype, [])

    # 基础查询
    if vod_class:
        query = db.query(MovDetail).filter(MovDetail.type_name == vod_class)
    else:
        query = db.query(MovDetail).filter(MovDetail.type_id.in_(mov_type_list))

    # 地区筛选
    if vod_area:
        if vod_area != 'more':
            query = query.filter(MovDetail.vod_area == vod_area)
        else:
            query = query.filter(
                MovDetail.vod_area.notin_(["中国", "内地", "美国", "日本", "韩国", "英国", "法国", "香港", "泰国"])
            )

    # 年份筛选
    if vod_year:
        if vod_year != 'more':
            query = query.filter(MovDetail.vod_year == vod_year)
        else:
            query = query.filter(
                MovDetail.vod_year.notin_([
                    "2023", "2022", "2021", "2020", "2019", "2018", "2017",
                    "2016", "2015", "2014", "2013", "2012", "2011", "2010"
                ])
            )

    # 关键词搜索
    if keyword:
        query = query.filter(
            or_(
                MovDetail.vod_name.like(f"%{keyword}%"),
                MovDetail.vod_content.like(f"%{keyword}%"),
                MovDetail.vod_director.like(f"%{keyword}%"),
                MovDetail.vod_actor.like(f"%{keyword}%")
            )
        )

    # 分页查询
    per_page = 12
    total = query.count()
    movs = query.order_by(MovDetail.vod_time.desc()).offset((page - 1) * per_page).limit(per_page).all()

    # 构建响应数据
    vod_list = []
    for mov in movs:
        vod_list.append({
            "vod_id": mov.id,
            "vod_pic": mov.vod_pic,
            "vod_name": mov.vod_name,
            "vod_remarks": mov.vod_remarks
        })

    return resp_ok(vod_list, "success")


@router.get("/vod_detail", response_model=dict)
def get_vod_detail(
    vod_id: int = Query(..., description="视频ID"),
    db: Session = Depends(get_db)
):
    """
    获取视频详情

    Args:
        vod_id: 视频ID
        db: 数据库会话

    Returns:
        视频详情
    """
    mov = db.query(MovDetail).filter(MovDetail.id == vod_id).first()

    if not mov:
        return {"code": 400, "msg": "failed no this mov", "data": None}

    # 处理内容中的 HTML 标签
    if mov.vod_content:
        mov.vod_content = (mov.vod_content.replace('<p>', '')
                          .replace('</p>', '')
                          .replace('<span>', '')
                          .replace('</span>', ''))

    # 处理播放URL
    if mov.vod_play_url:
        pay_url_dict = {}
        if mov.vod_play_url:
            for play_url_set in mov.vod_play_url.split('#'):
                if '$' in play_url_set:
                    k, v = play_url_set.split('$')
                    pay_url_dict[k] = v
        mov.vod_play_url = pay_url_dict

    # 格式化时间
    if mov.vod_time:
        mov.vod_time = mov.vod_time.strftime("%Y-%m-%d %H:%M:%S")

    # 转换为字典
    result = {c.name: getattr(mov, c.name) for c in mov.__table__.columns}

    return {"code": 200, "data": result, "msg": "success"}
