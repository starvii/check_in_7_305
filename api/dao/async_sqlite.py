from multiprocessing.dummy import Process
from sqlite3 import connect
from queue import Queue


class AsyncSqlite():
    def __init__(self, filename='db.sqlite'):
        self._proc = Process()
