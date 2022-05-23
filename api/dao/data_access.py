import os
import time
from typing import List, Dict

from api.dao.async_sqlite import AsyncSqlite, CursorState
from api.utility.net import ARP, ip2int

classmates = [
    ("200102160101", "李月月", "女", 1),
    ("200102160102", "胡盎", "男", 1),
    ("200102160103", "缪露露", "女", 1),
    ("200102160104", "俞震坤", "男", 1),
    ("200102160105", "俞伟杰", "男", 1),
    ("200102160106", "李希菡", "女", 1),
    ("200102160107", "李靖瑞", "男", 1),
    ("200102160108", "胡佳丽", "女", 1),
    ("200102160109", "陈堞", "男", 1),
    ("200102160110", "朱敏欣", "女", 1),
    ("200102160111", "潘梦", "女", 1),
    ("200102160112", "魏旭涛", "男", 1),
    ("200102160113", "蔡瑞", "男", 1),
    ("200102160114", "许佳裕", "女", 1),
    ("200102160115", "陆燕倩", "女", 1),
    ("200102160116", "吴宇骋", "男", 1),
    ("200102160117", "曾一帆", "女", 1),
    ("200102160118", "郑意亭", "女", 1),
    ("200102160119", "方昊", "男", 1),
    ("200102160120", "廖思源", "男", 1),
    ("200102160121", "谢燕平", "女", 1),
    ("200102160122", "葛宇轩", "男", 1),
    ("200102160123", "陈雨婷", "女", 1),
    ("200102160124", "徐佳", "女", 1),
    ("200102160125", "钟宇昕", "男", 1),
    ("200102160126", "王经纬", "男", 1),
    ("200102160127", "叶翱齐", "男", 1),
    ("200102160128", "陈梦琳", "女", 1),
    ("200102160129", "俞乐宁", "男", 1),
    ("200102160130", "余增添", "男", 1),
    ("200102160132", "南钰", "女", 1),
    ("200102160133", "戴舒琪", "女", 1),
    ("200102160134", "彭潇彤", "女", 1),
    ("200102160135", "王李悠悠", "女", 1),
    ("200102160136", "沈子琪", "女", 1),
    ("200102160137", "王楠", "女", 1),
    ("200102160138", "陈清方", "男", 1),
    ("200102160139", "董相南", "男", 1),
    ("200102160140", "余叶钒", "男", 1),
    ("200102160141", "袁鋆枫", "男", 1),
    ("200102160142", "熊浩洋", "男", 1),
    ("200102160143", "钱绎伊", "女", 1),
    ("200102160144", "侯仰信", "男", 1),
    ("200102160145", "陈可颖", "女", 1),
    ("200102160146", "吴萍", "女", 1),
    ("200102160147", "蔡燕霞", "女", 1),
    ("200102160148", "寿恒莉", "女", 1),
    ("200102160149", "胡星昊", "男", 1),
    ("200102160150", "郭旺超", "男", 1),

    ("200102160201", "王艳", "女", 2),
    ("200102160202", "叶群", "女", 2),
    ("200102160203", "应杰杰", "男", 2),
    ("200102160204", "沈俏妤", "女", 2),
    ("200102160205", "陈鑫", "男", 2),
    ("200102160206", "林甲贺", "男", 2),
    ("200102160207", "成昊天", "男", 2),
    ("200102160208", "叶婷", "女", 2),
    ("200102160209", "许楠", "男", 2),
    ("200102160210", "方诗怡", "女", 2),
    ("200102160211", "林哲宇", "男", 2),
    ("200102160212", "苏忠祥", "男", 2),
    ("200102160213", "吴浪浪", "女", 2),
    ("200102160214", "阮朦朦", "女", 2),
    ("200102160215", "姚璐", "女", 2),
    ("200102160216", "王艳", "女", 2),
    ("200102160217", "童雅薷", "女", 2),
    ("200102160218", "陈飞", "男", 2),
    ("200102160219", "林倩", "女", 2),
    ("200102160220", "蒋贤恒", "男", 2),
    ("200102160221", "王浩宇", "男", 2),
    ("200102160222", "周雯晓", "女", 2),
    ("200102160223", "潘佳瑶", "女", 2),
    ("200102160224", "郭嘉宁", "女", 2),
    ("200102160225", "葛倩琳", "女", 2),
    ("200102160226", "刘溯", "男", 2),
    ("200102160227", "吴震", "男", 2),
    ("200102160228", "朱小龙", "男", 2),
    ("200102160229", "叶剑宏", "男", 2),
    ("200102160230", "陆林莹", "女", 2),
    ("200102160231", "丁萍", "女", 2),
    ("200102160232", "黄玉敏", "男", 2),
    ("200102160233", "黄珍璇", "女", 2),
    ("200102160234", "左婉君", "女", 2),
    ("200102160236", "杨军", "男", 2),
    ("200102160237", "严鸣涛", "男", 2),
    ("200102160238", "施妮娜", "女", 2),
    ("200102160239", "方欣", "女", 2),
    ("200102160240", "楼剑宇", "男", 2),
    ("200102160241", "潘云鹤", "男", 2),
    ("200102160242", "童婷婷", "女", 2),
    ("200102160243", "李小龙", "男", 2),
    ("200102160244", "王黎宇", "男", 2),
    ("200102160245", "谢尚访", "男", 2),
    ("200102160246", "李思瑞", "女", 2),
    ("200102160247", "陈思思", "女", 2),
    ("200102160248", "吴钰鹏", "男", 2),
    ("200102160249", "吴俊鹏", "男", 2),
    ("200102160250", "魏尧涛", "男", 2),
    ("200102160251", "冯琪", "女", 2),
]


class DataAccess:
    def __init__(self):
        db_file = os.environ['DATABASE']
        self.db_thread = AsyncSqlite(db_file, False)

    def init(self):
        sql = '''
create table if not exists `classroom`(
   `id` integer primary key autoincrement,
   `name` varchar(100) not null unique,
   `columns` integer,
   `rows` integer,
   `comment` text
);

create table if not exists `checkin`(
    `id` integer primary key autoincrement,
    `code` integer,
    `date` date,
    `ip` integer,
    `mac` varchar(20),
    `coordinate_x` integer,
    `coordinate_y` integer,
    `comment` text
);

CREATE UNIQUE INDEX if not exists `uni_date_ip`
ON `checkin`(
  `date`, 
  `ip`
);

CREATE UNIQUE INDEX if not exists `uni_date_mac`
ON `checkin`(
  `date`, 
  `mac`
);

CREATE UNIQUE INDEX if not exists `uni_date_stu`
ON `checkin`(
  `date`, 
  `code`
);

CREATE UNIQUE INDEX if not exists `uni_date_pos`
ON `checkin`(
  `date`, 
  `coordinate_x`,
  `coordinate_y`
);

create table if not exists `classmate`(
    `id` integer primary key autoincrement,
    `code` varchar(100) unique,
    `name` varchar(100),
    `gender` varchar(10),
    `class_id` integer
);

BEGIN;
insert or replace into `classroom`
values(1, '7-305', 6, 8, '');
'''
        s = [s.strip() for s in sql.split(';') if len(s.strip()) > 0]
        for _sql in s:
            self.db_thread.execute(_sql)
        sql = '''
        INSERT INTO `classmate`(`id`, `code`, `name`, `gender`, `class_id`)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS(
            SELECT 1 FROM `classmate`
            WHERE `code` = ?
        );
        '''
        for c in classmates:
            self.db_thread.execute(sql, (int(c[0]), c[0], c[1], c[2], c[3], c[0]))
        self.db_thread.commit()

    def select_checkin_result(self) -> List[Dict]:
        today = time.strftime('%Y-%m-%d', time.localtime())
        sql = f'''
        select 
            t2.code,
            t2.name,
            t1.coordinate_x,
            t1.coordinate_y
        from checkin t1
        left join classmate t2
        on t1.code = t2.id
        where t1.date = ?
        '''
        records = self.db_thread.select(sql, (today,))
        buffer = []
        for rec in records:
            buffer.append(dict(
                code=rec[0],
                name=rec[1],
                x=rec[2],
                y=rec[3],
            ))
        return buffer

    def select_classroom(self) -> Dict:
        sql = '''select * from `classroom` where `id`=1;'''
        rec = self.db_thread.select_one(sql)
        return dict(
            name=rec[1],
            columns=rec[2],
            rows=rec[3],
        )

    def select_classmate(self, code: str, name: str) -> bool:
        sql = '''select count(1) from `classmate` where code=? and name=?;'''
        rec = self.db_thread.select_one(sql, (code, name))
        return rec[0] != 0

    def insert_checkin_action(self, code: int, x: int, y: int, arp: ARP) -> int:
        today = time.strftime('%Y-%m-%d', time.localtime())
        sql = f'''
                            insert into `checkin`(
                                `code`,
                                `date`,
                                `ip`,
                                `mac`,
                                `coordinate_x`,
                                `coordinate_y`
                            ) values (
                                ?, ?, ?, ?, ?, ?
                            );
                            '''
        ip = ip2int(arp.ip)
        mac = arp.mac
        self.db_thread.execute('begin;')
        c: CursorState = self.db_thread.execute(sql, (code, today, ip, mac, x, y))
        self.db_thread.commit()
        return c.last_row_id
