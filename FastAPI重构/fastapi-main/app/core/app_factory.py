"""
FastAPI 应用工厂
整合所有组件：数据库、路由、CORS、APScheduler 等
"""
import os
import platform
import atexit
import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import load_config
from app.models.database import engine
from app.models.base import Base


# APScheduler 实例
scheduler = BackgroundScheduler()


def init_scheduler():
    """
    初始化 APScheduler，添加文件锁防止多进程重复执行
    """
    from app.task.tasks import SakuarDataSchedule

    @scheduler.scheduled_job('cron', id='sakura_update_job', day='*', hour='10', minute='47', second='01', misfire_grace_time=60)
    def scheduler_update_sakura():
        """定时更新樱花动漫数据"""
        import app.utils.avalon_logger as logger
        logger.info('Start Update Sakura Data')
        sd = SakuarDataSchedule()
        sd.get_sakura_data()
        logger.info('Finish Update Sakura Data')


def setup_logging():
    """
    配置日志系统
    """
    config = load_config()
    logging_path = config.get('LOGGING_PATH', './logs')

    # 确保日志目录存在
    if not os.path.exists(logging_path):
        os.makedirs(logging_path, exist_ok=True)

    try:
        import yaml
        with open('./app/config/logging.yaml', 'r', encoding='utf-8') as f:
            logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)
    except Exception as e:
        print(f"Warning: Could not load logging config: {e}")
        # 使用默认配置
        logging.basicConfig(level=logging.INFO)


def create_scheduler_lock():
    """
    创建调度器文件锁，防止多进程下重复启动
    """
    if platform.system() != 'Windows':
        # Linux 环境下
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.start()
            print("Scheduler started successfully (Linux)")
        except:
            print("Scheduler is already running in another process (Linux)")

        def unlock():
            try:
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()
            except:
                pass

        atexit.register(unlock)
    else:
        # Windows 环境下
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler.start()
            print("Scheduler started successfully (Windows)")
        except:
            print("Scheduler is already running in another process (Windows)")

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                f.close()
            except:
                pass

        atexit.register(_unlock_file)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 生命周期管理
    """
    # 启动时执行
    setup_logging()
    init_scheduler()
    create_scheduler_lock()
    print("FastAPI application started")

    yield

    # 关闭时执行
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler shutdown")
    print("FastAPI application shutdown")


def create_app() -> FastAPI:
    """
    创建 FastAPI 应用实例

    Returns:
        FastAPI: 应用实例
    """
    config = load_config()

    # 创建 FastAPI 应用
    app = FastAPI(
        title="Sakura Comic API",
        description="樱花动漫网站 API",
        version="1.0.0",
        lifespan=lifespan
    )

    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境应该配置具体的域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    register_routes(app)

    # 注册事件处理器
    register_event_handlers(app)

    return app


def register_routes(app: FastAPI):
    """
    注册所有 API 路由

    Args:
        app: FastAPI 应用实例
    """
    from app.api.v1 import auth, video, comment, collection

    # 注册 v1 版本路由
    app.include_router(auth.router, prefix="/api/v1", tags=["认证"])
    app.include_router(video.router, prefix="/api/v1", tags=["视频"])
    app.include_router(comment.router, prefix="/api/v1", tags=["评论"])
    app.include_router(collection.router, prefix="/api/v1", tags=["收藏"])


def register_event_handlers(app: FastAPI):
    """
    注册事件处理器

    Args:
        app: FastAPI 应用实例
    """
    @app.get("/")
    async def root():
        return {"message": "Sakura Comic API", "version": "1.0.0"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}
