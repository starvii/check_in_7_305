import sqlite3
from abc import abstractmethod
from typing import Optional, Any


# class IQuery:
#     """
#     高级查询使用接口
#     """
#     def __init__(self, conn: Optional[sqlite3.Connection] = None) -> None:
#         super().__init__()
#         self._conn: Optional[sqlite3.Connection] = conn
#
#     @property
#     def connection(self) -> sqlite3.Connection:
#         return self._conn
#
#     @connection.setter
#     def connection(self, value: sqlite3.Connection):
#         self._conn = value
#
#     @abstractmethod
#     def execute(self, *args) -> Any:
#         pass



