import json
import datetime
import logging

import requests
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.database import SessionLocal
from app.models.models import MovType, MovInfo, MovDetail

# 设置日志
logger = logging.getLogger(__name__)


class SakuarDataSchedule:
    def __init__(self):
        self.sakura_list = 'https://m3u8.apiyhzy.com/api.php/provide/vod/?ac=list&pg={page}'
        self.sakura_detail = 'https://m3u8.apiyhzy.com/api.php/provide/vod/?ac=detail&pg={page}'
        self.total_page = None
        self.avalon_latest_time = None
        self.stop_craw = False  # 当此值为True 不继续抓取数据

    @staticmethod
    def get_avalon_latest_time(session: Session) -> datetime.datetime:
        '''
        获取数据库内 数据最新更新时间
        :param session: 数据库会话
        :return:
        '''
        avalon_latest_time = session.query(func.max(MovDetail.vod_time)).scalar()
        if not avalon_latest_time:
            # 如果没有数据，返回一个很早的时间
            return datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')
        avalon_latest_time_str = avalon_latest_time.strftime('%Y-%m-%d %H:%M:%S').split(' ')[0]
        avalon_latest_time = datetime.datetime.strptime(avalon_latest_time_str, '%Y-%m-%d')
        return avalon_latest_time

    def insert_or_update_movdetail(self, session: Session, mov_list: list) -> None:
        '''
        将 movdetail 数据 插入或更新到数据库
        :param session: 数据库会话
        :param mov_list: list
        :return:
        '''
        need_insert_mov_list = []
        for mov_detail in mov_list:
            vod_time_str = mov_detail.get('vod_time')
            if not vod_time_str:
                continue
            try:
                vod_time = datetime.datetime.strptime(vod_time_str, '%Y-%m-%d %H:%M:%S')
            except:
                continue

            if vod_time > self.avalon_latest_time:
                # 进行更新或插入数据操作
                self.stop_craw = False
                vod_id = mov_detail['vod_id']
                avalon_mov_detail = session.query(MovDetail).filter_by(vod_id=vod_id).first()
                if avalon_mov_detail:
                    # 数据库已有此数据 执行更新操作
                    for k, v in mov_detail.items():
                        if hasattr(avalon_mov_detail, k):
                            setattr(avalon_mov_detail, k, v)
                    session.commit()
                else:
                    # 数据库没有此数据 执行插入操作
                    need_insert_mov_list.append(mov_detail)
            else:
                self.stop_craw = True

        if need_insert_mov_list:
            # 如果有需要插入的新数据
            session.bulk_insert_mappings(
                MovDetail,
                need_insert_mov_list
            )
            session.commit()
            logger.info(f'插入 {len(need_insert_mov_list)} 条新记录')

    def get_sakura_data(self) -> None:
        '''
        获取樱花数据 对已有数据进行更新操作 其他执行插入操作
        :return: None
        '''
        session = SessionLocal()
        try:
            self.avalon_latest_time = self.get_avalon_latest_time(session)  # 数据库vod_time最大值

            url = self.sakura_detail.format(page=1)
            logger.info(f'Updating: {url}')
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                total = int(data['total'])
                limit_per_page = int(data['limit'])
                self.total_page = (total // limit_per_page) + 1 if total % limit_per_page else total // limit_per_page
                mov_detail_list = data['list']
                self.insert_or_update_movdetail(session, mov_detail_list)
            else:
                logger.debug(f"抓取数据失败, code: {response.status_code}")

            for i in range(2, self.total_page + 1):
                url = self.sakura_detail.format(page=i)
                if self.stop_craw:
                    logger.info("数据已更新完毕: 停止抓取")
                    break
                logger.info(f'Updating: {url}')
                response = requests.get(url)
                if response.status_code == 200:
                    data = json.loads(response.text)
                    mov_detail_list = data['list']
                    self.insert_or_update_movdetail(session, mov_detail_list)
                else:
                    logger.debug(f"抓取数据失败, code: {response.status_code}")
        except Exception as e:
            logger.error(f"更新数据时出错: {e}")
            session.rollback()
        finally:
            session.close()


class SakuraData:
    def __init__(self):
        self.total_page = None
        self.mov_type = None
        self.sakura_list = 'https://m3u8.apiyhzy.com/api.php/provide/vod/?ac=list&pg={page}'
        self.sakura_detail = 'https://m3u8.apiyhzy.com/api.php/provide/vod/?ac=detail&pg={page}'
        self.__init_sakura__()

    def __init_sakura__(self):
        url = self.sakura_list.format(page=1)
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            if self.mov_type is None:
                self.mov_type = data['class']
            if self.total_page is None:
                total = int(data['total'])
                limit_per_page = int(data['limit'])
                self.total_page = (total // limit_per_page) + 1 if total % limit_per_page else total // limit_per_page
        else:
            raise Exception(f"初始化失败: 无法获取数据")

    def insert_mov_type(self):
        session = SessionLocal()
        try:
            session.bulk_insert_mappings(
                MovType,
                self.mov_type
            )
            session.commit()
            logger.info(f'保存视频类型进入数据库')
        except Exception as e:
            logger.error(f"插入视频类型失败: {e}")
            session.rollback()
        finally:
            session.close()

    def get_mov_info(self, page=1):
        # 读取url数据并保存到数据库
        session = SessionLocal()
        try:
            url = self.sakura_list.format(page=page)
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                mov_info_list = data['list']
                session.bulk_insert_mappings(
                    MovInfo,
                    mov_info_list
                )
                session.commit()
                logger.info(f'mov_list page {page} catched')
            else:
                logger.debug(f"抓取数据失败, code: {response.status_code}")
        except Exception as e:
            logger.error(f"插入mov_info失败: {e}")
            session.rollback()
        finally:
            session.close()

    def get_mov_detail(self, page=1):
        '''
        抓取 mov detail
        :param page: 页码
        :return:
        '''
        session = SessionLocal()
        try:
            url = self.sakura_detail.format(page=page)
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                mov_detail_list = data['list']
                session.bulk_insert_mappings(
                    MovDetail,
                    mov_detail_list
                )
                session.commit()
                logger.info(f'mov_detail page {page} catched')
            else:
                logger.debug(f"抓取数据失败, code: {response.status_code}")
        except Exception as e:
            logger.error(f"插入mov_detail失败: {e}")
            session.rollback()
        finally:
            session.close()

    def crawl_mov_info_all(self):
        for page in range(1, self.total_page + 1):
            self.get_mov_info(page)

    def crawl_mov_detail_all(self):
        for page in range(1, self.total_page + 1):
            self.get_mov_detail(page)



