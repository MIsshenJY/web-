from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.models import UserCollection, MovDetail
from app.core.security import require_auth
from app.utils.response_util import resp_ok
from pydantic import BaseModel

router = APIRouter(tags=["收藏"])


class CollectionAction(BaseModel):
    user_id: int
    vod_id: int


@router.get("/collection/show", response_model=dict, dependencies=[Depends(require_auth)])
def show_collect_video(
    user_id: int = Query(..., description="用户ID"),
    page: int = Query(1, ge=1, description="页码"),
    db: Session = Depends(get_db)
):
    """
    获取用户的收藏视频列表

    Args:
        user_id: 用户ID
        page: 页码
        db: 数据库会话

    Returns:
        收藏视频列表
    """
    user_collection = db.query(UserCollection).filter(UserCollection.user_id == user_id).first()
    collect_vod_list = []

    if user_collection:
        # 分割收藏的视频ID列表
        store_vod_list = user_collection.movdetail_id_list.split(';')[:-1] if user_collection.movdetail_id_list else []

        if store_vod_list:
            # 分页查询
            per_page = 12
            collect_movs = (db.query(MovDetail)
                           .filter(MovDetail.id.in_(store_vod_list))
                           .order_by(MovDetail.vod_time.desc())
                           .offset((page - 1) * per_page)
                           .limit(per_page)
                           .all())

            for mov in collect_movs:
                collect_vod_list.append({
                    "vod_id": mov.id,
                    "vod_pic": mov.vod_pic,
                    "vod_name": mov.vod_name,
                    "vod_remarks": mov.vod_remarks
                })

    return resp_ok(collect_vod_list, "收藏的视频信息")


@router.get("/collection/is_collection", response_model=dict, dependencies=[Depends(require_auth)])
def show_is_collect_video(
    user_id: int = Query(..., description="用户ID"),
    vod_id: str = Query(..., description="视频ID"),
    db: Session = Depends(get_db)
):
    """
    检查视频是否已被收藏

    Args:
        user_id: 用户ID
        vod_id: 视频ID
        db: 数据库会话

    Returns:
        收藏状态
    """
    user_collection = db.query(UserCollection).filter(UserCollection.user_id == user_id).first()

    if user_collection and vod_id + ';' in (user_collection.movdetail_id_list or ''):
        return resp_ok(1, "该视频已被收藏")

    return resp_ok(0, "该视频未被收藏")


@router.get("/collection/add", response_model=dict, dependencies=[Depends(require_auth)])
def add_collect_video(
    user_id: int = Query(..., description="用户ID"),
    vod_id: str = Query(..., description="视频ID"),
    db: Session = Depends(get_db)
):
    """
    添加收藏视频

    Args:
        user_id: 用户ID
        vod_id: 视频ID
        db: 数据库会话

    Returns:
        收藏结果
    """
    if not user_id or not vod_id:
        return {"code": 400, "message": "没有要收藏的视频信息"}

    user_collection = db.query(UserCollection).filter(UserCollection.user_id == user_id).first()

    try:
        # 如果有收藏信息则更新，没有则添加
        if user_collection:
            # 检查是否已收藏
            if vod_id + ';' not in (user_collection.movdetail_id_list or ''):
                user_collection.movdetail_id_list = (user_collection.movdetail_id_list or '') + vod_id + ';'
        else:
            user_collection = UserCollection(user_id=user_id, movdetail_id_list=vod_id + ';')
            db.add(user_collection)

        db.commit()

        # 返回更新后的收藏列表
        updated_collection = db.query(UserCollection).filter(UserCollection.user_id == user_id).first()
        if updated_collection and updated_collection.movdetail_id_list:
            store_vod_list = updated_collection.movdetail_id_list.split(';')[:-1]
            return resp_ok(list(set(store_vod_list)), "视频收藏成功")

        return resp_ok([], "视频收藏成功")

    except Exception as e:
        db.rollback()
        raise e


@router.get("/collection/remove", response_model=dict, dependencies=[Depends(require_auth)])
def remove_collect_video(
    user_id: int = Query(..., description="用户ID"),
    vod_id: str = Query(..., description="视频ID"),
    db: Session = Depends(get_db)
):
    """
    移除收藏视频

    Args:
        user_id: 用户ID
        vod_id: 视频ID
        db: 数据库会话

    Returns:
        移除结果
    """
    if not user_id or not vod_id:
        return {"code": 400, "message": "没有要删除收藏的视频信息"}

    user_collection = db.query(UserCollection).filter(UserCollection.user_id == user_id).first()

    if user_collection:
        try:
            # 移除指定的视频ID
            if user_collection.movdetail_id_list:
                user_collection.movdetail_id_list = user_collection.movdetail_id_list.replace(vod_id + ';', '')
                db.commit()

                # 返回更新后的收藏列表
                if user_collection.movdetail_id_list:
                    store_vod_list = user_collection.movdetail_id_list.split(';')[:-1]
                    return resp_ok(list(set(store_vod_list)), "视频删除收藏成功")

        except Exception as e:
            db.rollback()
            raise e

    return resp_ok([], "视频删除收藏成功")
