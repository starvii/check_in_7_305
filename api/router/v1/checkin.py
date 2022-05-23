from concurrent.futures import Executor, wait, FIRST_COMPLETED
from logging import Logger
from typing import Dict

from sanic import Blueprint, Sanic, json, Request

from api.dao.data_access import DataAccess
from api.utility.net import get_ip_mac, ARP

PREFIX = '/api'
VERSION = 'v1'
bp: Blueprint = Blueprint(
    'checkin',
    url_prefix=PREFIX,
    version=VERSION,
)
app: Sanic = Sanic.get_app()
executor: Executor = app.ctx.executor
dao: DataAccess = app.ctx.dao
logger: Logger = app.ctx.logger


@bp.get('/checkin')
async def checkin_result(request: Request):
    if 'classroom' not in app.ctx.__dict__:
        app.ctx.classroom = dao.select_classroom()
    checkin = dao.select_checkin_result()
    return json(dict(
        code=0,
        message='ok',
        data=dict(
            classroom=app.ctx.classroom,
            checkin=checkin,
        ),
    ))


@bp.post('/checkin/<position>')
async def checkin_action(request: Request, position: str):
    try:
        req_data = request.json
        name = req_data['name']
        code = req_data['code']
        x, y = [int(t) for t in position.split(',') if t.strip().isdigit()]

        if not dao.select_classmate(code, name):
            return json(dict(code=-2, message='学号或姓名错误'))
        if 'classroom' not in app.ctx.__dict__:
            app.ctx.classroom = dao.select_classroom()
        if x < 0 or x >= app.ctx.classroom['columns']:
            return json(dict(code=-3, message='座位超限'))
        if y < 0 or y >= app.ctx.classroom['rows']:
            return json(dict(code=-3, message='座位超限'))
        client_ip = request.ip
        if client_ip == '127.0.0.1':
            arp = ARP(client_ip, 0, client_ip, 'ff-ff-ff-ff-ff-ff', False)
        else:
            task = executor.submit(get_ip_mac)
            wait([task], return_when=FIRST_COMPLETED)
            ip_mac_table: Dict[str, ARP] = task.result()
            if client_ip not in ip_mac_table:
                return json(dict(code=-4, message='网络参数错误'))
            arp = ip_mac_table[client_ip]
        try:
            last_insert_rowid = dao.insert_checkin_action(int(code), x, y, arp)
            if last_insert_rowid <= 0:
                return json(dict(code=-5, message='数据写入失败'))
        except Exception as e:
            logger.error('%s: %s', type(e), e)
            return json(dict(code=1, message='已签到'))
        return json(dict(code=0, message='ok'))
    except Exception as e:
        logger.error('%s: %s', type(e), e)
        return json(dict(code=-1, message='提交数据格式有误'))
