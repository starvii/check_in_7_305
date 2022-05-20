from fastapi import FastAPI, Request, status
from api.v1 import api_v1


def create_app():
    app = FastAPI(
        title="7-305签到",
        description="7-305签到",
        version="0.0.1",
        docs_url="/api/v1/docs",  # 自定义文档地址
        openapi_url="/api/v1/openapi.json",  #
        redoc_url=None,  # 禁用redoc文档
    )

    # 导入路由, 前缀设置
    app.include_router(
        api_v1,
        prefix="/api/v1/mall",
    )

    # 异常捕获
    # register_exception(app)

    # 跨域设置
    # register_cors(app)

    return app
