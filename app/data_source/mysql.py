from app.types.data_source_types import MysqlDataSource
from app.data_source import BaseDataSource


import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import NullPool, QueuePool, text

from typing import Any


class Mysql(BaseDataSource):

    def __init__(self, config: MysqlDataSource) -> None:
        self.conn = None
        self.__is_worker: bool = None
        self.url = (
            "mysql://"
            + config.user
            + ":"
            + config.password
            + "@"
            + config.host
            + ":"
            + str(config.port)
            + "/"
            + config.db
        )

    def connect(self, is_worker: bool = False) -> None:
        if not is_worker:
            engine = sqlalchemy.create_engine(self.url, poolclass=NullPool)
            conn = sessionmaker(bind=engine)()
        else:
            engine = sqlalchemy.create_engine(
                self.url, pool_size=10, max_overflow=0, poolclass=QueuePool
            )
            conn = scoped_session(sessionmaker(bind=engine))
            conn.begin()
        self.conn = conn
        self.__is_worker = is_worker

    @staticmethod
    def __serializer(data: Any):
        keys = data.keys()
        dict_result = [dict(zip(keys, row)) for row in data]
        return dict_result

    def execute(self, query: str):
        result = self.conn.execute(text(query))
        if result:
            data = self.__serializer(result)
            if len(data) == 1:
                data = data[0]
            return data
        return {}

    def disconnect(self) -> None:
        if not self.__is_worker:
            self.conn.close()
        else:
            self.conn.remove()
