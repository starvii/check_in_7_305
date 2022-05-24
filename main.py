#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
运行命令：
uvicorn main:app --port=8000
"""
import os

from api import create_app


# initialize
app = create_app()


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8000,
        access_log=False,
        debug=True,
        workers=os.cpu_count(),
    )
