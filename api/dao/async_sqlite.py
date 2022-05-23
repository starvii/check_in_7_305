import sqlite3
from enum import Enum
from multiprocessing.dummy import Process
from queue import Queue
from typing import Optional, Tuple, List, Union, Any


class CursorState:
    def __init__(self, cursor: sqlite3.Cursor):
        self.last_row_id = cursor.lastrowid
        self.row_count = cursor.rowcount
        self.description = cursor.description

    def __repr__(self):
        return f'last_row_id = {self.last_row_id}, row_count = {self.row_count}, description = {self.description}'

    def __str__(self):
        return self.__repr__()


class Command(Enum):
    Close = 0x00
    Commit = 0x01
    RollBack = 0x02
    NoMore = 0x03
    Execute = 0x11
    ExecuteMany = 0x12
    SelectOne = 0x21
    Select = 0x22


class AsyncQuery:
    def __init__(
            self,
            command: Command,
            request: Optional[str] = None,
            arguments: Optional[Tuple] = None,
            response_queue: Optional[Queue] = None,
    ):
        self.cmd = command
        self.sql = request
        self.arg = arguments
        self.res = response_queue

    def __repr__(self):
        return f'cmd = {self.cmd}, sql = {self.sql}, arg = {self.arg}, res = {self.res}'

    def __str__(self):
        return self.__repr__()


class AsyncSqlite(Process):
    def __init__(self, filename: str, autocommit: bool = False, journal_mode: str = "WAL"):
        super(AsyncSqlite, self).__init__()
        self.filename: str = filename
        self.autocommit: bool = autocommit
        self.journal_mode: str = journal_mode
        # use request queue of unlimited size
        self.reqs: Queue[AsyncQuery] = Queue()
        self.setDaemon(True)  # python2.5-compatible
        self.start()

    def run(self):
        if self.autocommit:
            conn: sqlite3.Connection = sqlite3.connect(self.filename, isolation_level=None, check_same_thread=False)
        else:
            conn: sqlite3.Connection = sqlite3.connect(self.filename, check_same_thread=False)
        conn.execute('PRAGMA journal_mode = %s' % self.journal_mode)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('PRAGMA synchronous=OFF')
        while 1:
            query: AsyncQuery = self.reqs.get()
            if query.cmd == Command.Close:
                break
            elif query.cmd == Command.Commit:
                conn.commit()
            elif query.sql is not None:
                sql: str = query.sql.strip()
                ret: Optional[Union[BaseException, CursorState]] = None
                try:
                    cursor.execute(sql, query.arg) if query.arg is not None else cursor.execute(sql)
                    if query.cmd in {Command.Execute, Command.ExecuteMany}:
                        ret = CursorState(cursor)
                except Exception as e:
                    ret = e
                if query.res is not None:
                    if ret is not None:
                        query.res.put(ret)
                    elif query.cmd == Command.SelectOne:
                        query.res.put(cursor.fetchone())
                    elif query.cmd == Command.Select:
                        for rec in cursor:
                            query.res.put(rec)
                        query.res.put(Command.NoMore)
        conn.close()

    def execute(self, req: str, arg: Optional[Tuple] = None) -> CursorState:
        query = AsyncQuery(Command.Execute, req, arg, Queue())
        self.reqs.put(query)
        ret: Union[BaseException, CursorState] = query.res.get()
        if isinstance(ret, BaseException):
            self.reqs.put(AsyncQuery(Command.RollBack))
            raise ret
        if self.autocommit:
            self.reqs.put(AsyncQuery(Command.Commit))
        return ret

    def execute_many(self, req: str, items: List[Tuple]) -> List[CursorState]:
        results: List[CursorState] = []
        queue = Queue()
        for item in items:
            query = AsyncQuery(Command.ExecuteMany, req, item, queue)
            self.reqs.put(query)
            ret: Union[BaseException, CursorState] = query.res.get()
            if isinstance(ret, BaseException):
                self.reqs.put(AsyncQuery(Command.RollBack))
                raise ret
            results.append(ret)
        if self.autocommit:
            self.reqs.put(AsyncQuery(Command.Commit))
        return results

    def select(self, req: str, arg: Optional[Tuple] = None):
        query: AsyncQuery = AsyncQuery(Command.Select, req, arg, Queue())
        self.reqs.put(query)
        while 1:
            ret: Union[BaseException, Command, Any] = query.res.get()
            if isinstance(ret, BaseException):
                raise ret
            if isinstance(ret, Command) and ret == Command.NoMore:
                break
            yield ret

    def select_one(self, req: str, arg: Optional[Tuple] = None):
        query: AsyncQuery = AsyncQuery(Command.SelectOne, req, arg, Queue())
        self.reqs.put(query)
        ret: Union[BaseException, Any] = query.res.get()
        if isinstance(ret, BaseException):
            raise ret
        return ret

    def commit(self):
        self.reqs.put(AsyncQuery(Command.Commit))

    def close(self):
        self.reqs.put(AsyncQuery(Command.Close))
