"""
数据模型定义
从 Flask 迁移到 FastAPI，保持 SQLAlchemy 1.4 兼容模式
"""
import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base


class MovType(Base):
    __tablename__ = 'sakura_movtype'

    type_id = Column(Integer, primary_key=True)
    type_name = Column(String(20), nullable=False)
    this_type_movies = relationship('MovInfo', back_populates='this_mov_type')
    this_type_movie_details = relationship('MovDetail', back_populates='this_mov_type')


class MovInfo(Base):
    __tablename__ = 'sakura_movinfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey('sakura_movtype.type_id'))  # 一对多关系,ForeignKey在多侧
    type_name = Column(String(20), nullable=False)
    vod_en = Column(Text, nullable=False)
    vod_id = Column(Integer, primary_key=True)
    vod_name = Column(Text, nullable=False)
    vod_play_from = Column(Text)
    vod_remarks = Column(Text)
    vod_time = Column(DateTime)
    this_mov_type = relationship('MovType', back_populates='this_type_movies')


class MovDetail(Base):
    __tablename__ = 'sakura_movdetail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer)
    type_id = Column(Integer, ForeignKey('sakura_movtype.type_id'))  # 一对多,设置外键
    type_id_1 = Column(Integer)
    type_name = Column(String(20))
    vod_actor = Column(Text)
    vod_area = Column(Text)
    vod_author = Column(Text)
    vod_behind = Column(Text)
    vod_blurb = Column(Text)
    vod_class = Column(Text)
    vod_color = Column(Text)
    vod_content = Column(Text)
    vod_copyright = Column(Integer)
    vod_director = Column(Text)
    vod_douban_id = Column(Integer)
    vod_douban_score = Column(String(20))
    vod_down = Column(Integer)
    vod_down_from = Column(Text)
    vod_down_note = Column(Text)
    vod_down_server = Column(Text)
    vod_down_url = Column(Text)
    vod_duration = Column(Text)
    vod_en = Column(Text)
    vod_hits = Column(Integer)
    vod_hits_day = Column(Integer)
    vod_hits_month = Column(Integer)
    vod_hits_week = Column(Integer)
    vod_id = Column(Integer, primary_key=True)
    vod_isend = Column(Integer)
    vod_jumpurl = Column(Text)
    vod_lang = Column(Text)
    vod_letter = Column(Text)
    vod_level = Column(Integer)
    vod_lock = Column(Integer)
    vod_name = Column(Text)
    vod_pic = Column(Text)
    vod_pic_screenshot = Column(Text)
    vod_pic_slide = Column(Text)
    vod_pic_thumb = Column(Text)
    vod_play_from = Column(Text)
    vod_play_note = Column(Text)
    vod_play_server = Column(Text)
    vod_play_url = Column(LONGTEXT)
    vod_plot = Column(Integer)
    vod_plot_detail = Column(Text)
    vod_plot_name = Column(Text)
    vod_points = Column(Integer)
    vod_points_down = Column(Integer)
    vod_points_play = Column(Integer)
    vod_pubdate = Column(Text)
    vod_pwd = Column(Text)
    vod_pwd_down = Column(Text)
    vod_pwd_down_url = Column(Text)
    vod_pwd_play = Column(Text)
    vod_pwd_play_url = Column(Text)
    vod_pwd_url = Column(Text)
    vod_rel_art = Column(Text)
    vod_rel_vod = Column(Text)
    vod_remarks = Column(Text)
    vod_reurl = Column(Text)
    vod_score = Column(Text)
    vod_score_all = Column(Integer)
    vod_score_num = Column(Integer)
    vod_serial = Column(Text)
    vod_state = Column(Text)
    vod_status = Column(Integer)
    vod_sub = Column(Text)
    vod_tag = Column(Text)
    vod_time = Column(DateTime)
    vod_time_add = Column(Integer)
    vod_time_hits = Column(Integer)
    vod_time_make = Column(Integer)
    vod_total = Column(Integer)
    vod_tpl = Column(Text)
    vod_tpl_down = Column(Text)
    vod_tpl_play = Column(Text)
    vod_trysee = Column(Integer)
    vod_tv = Column(Text)
    vod_up = Column(Integer)
    vod_version = Column(Text)
    vod_weekday = Column(Text)
    vod_writer = Column(Text)
    vod_year = Column(Text)
    this_mov_type = relationship('MovType', back_populates='this_type_movie_details')
    comments = relationship('Comment', back_populates='mov_detail', cascade='all, delete-orphan')


class User(Base):
    __tablename__ = 'sakura_user'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    password_hash = Column(String(128))

    comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan')  # 用户信息被删除后 评论也一起被删除
    collections = relationship('UserCollection', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        # 生成hash后的密码
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        # 将hash密码和密码进行比对
        return check_password_hash(self.password_hash, password)


class Comment(Base):
    __tablename__ = 'sakura_comment'

    id = Column(Integer, primary_key=True)
    body = Column(Text)
    reviewed = Column(Boolean, default=True)  # 该评论是否通过审核
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    user_id = Column(Integer, ForeignKey('sakura_user.id'))
    replied_id = Column(Integer, ForeignKey('sakura_comment.id'))  # 将replied_id定义为外键
    movdetail_id = Column(Integer, ForeignKey('sakura_movdetail.id'))

    user = relationship('User', back_populates='comments')
    mov_detail = relationship('MovDetail', back_populates='comments')
    replies = relationship('Comment', back_populates='replied', cascade='all, delete-orphan')  # 父评论，对应一,父评论被删除子评论也会删除
    replied = relationship('Comment', back_populates='replies', remote_side=[id])  # 子评论，对应多，remote_side参数指定了自己代表多


class UserCollection(Base):
    __tablename__ = 'sakura_user_collection'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('sakura_user.id'))
    movdetail_id_list = Column(LONGTEXT)

    user = relationship('User', back_populates='collections')
