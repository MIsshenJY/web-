from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.models import Comment, User
from app.core.security import require_auth, get_current_user
from app.utils.response_util import resp_ok
from pydantic import BaseModel

router = APIRouter(tags=["评论"])


class CommentCreate(BaseModel):
    """创建评论请求"""
    body: str
    user_id: int


class CommentReply(BaseModel):
    """回复评论请求"""
    body: str
    user_id: int


def get_all_replies(reply_comments: List[Comment], result: List[dict]):
    """
    递归获取所有回复

    Args:
        reply_comments: 评论列表
        result: 结果列表
    """
    for comment in reply_comments:
        reply = {
            "user_name": comment.user.name,
            "id": comment.id,
            "reply_user_name": comment.replied.user.name if comment.replied and comment.replied.user else "",
            "body": comment.body,
            "time": comment.timestamp.strftime('%Y-%m-%d')
        }
        result.append(reply)
        if comment.replies:
            get_all_replies(comment.replies, result)


@router.get("/show/comment/{vod_id}", response_model=dict)
def show_comments(
    vod_id: int,
    db: Session = Depends(get_db)
):
    """
    获取视频的评论列表

    Args:
        vod_id: 视频ID
        db: 数据库会话

    Returns:
        评论列表
    """
    comments = db.query(Comment).filter(Comment.movdetail_id == vod_id).order_by(Comment.timestamp.desc()).all()

    comment_list = []
    for comment in comments:
        c = {
            "user_name": comment.user.name,
            "body": comment.body,
            "time": comment.timestamp.strftime('%Y-%m-%d'),
            "id": comment.id
        }
        reply_list = []
        get_all_replies(comment.replies, reply_list)
        c['reply_list'] = reply_list
        comment_list.append(c)

    return resp_ok(comment_list, "评论获取成功")


@router.post("/publish/comment/{vod_id}", response_model=dict, dependencies=[Depends(require_auth)])
def post_comments(
    vod_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db)
):
    """
    发表评论

    Args:
        vod_id: 视频ID
        comment_data: 评论内容
        db: 数据库会话

    Returns:
        发表结果
    """
    body = comment_data.body
    user_id = comment_data.user_id

    if not body or not user_id:
        return {"code": 400, "message": "请输入评论内容"}

    try:
        comment = Comment(body=body, user_id=user_id, movdetail_id=vod_id)
        db.add(comment)
        db.commit()
        return resp_ok(None, "评论发布成功")
    except Exception as e:
        db.rollback()
        raise e


@router.post("/reply/comment/{comment_id}", response_model=dict, dependencies=[Depends(require_auth)])
def reply_comment(
    comment_id: int,
    reply_data: CommentReply,
    db: Session = Depends(get_db)
):
    """
    回复评论

    Args:
        comment_id: 被回复的评论ID
        reply_data: 回复内容
        db: 数据库会话

    Returns:
        回复结果
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        return {"code": 400, "message": "此评论已不存在"}

    body = reply_data.body
    user_id = reply_data.user_id

    try:
        r_comment = Comment(body=body, user_id=user_id, replied_id=comment_id)
        db.add(r_comment)
        db.commit()
        return resp_ok(None, "评论回复成功")
    except Exception as e:
        db.rollback()
        raise e
