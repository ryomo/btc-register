import logging
import os
import sqlite3
from contextlib import closing
from enum import Enum
from sqlite3 import Cursor
from typing import Iterable, List, Callable, Union

logger = logging.getLogger(__name__)


class Fetch(Enum):
    """
    Used in `Db._execute()` to set how many rows to be fetched.
    """
    NONE = 0
    ONE = 1
    ALL = 2


class Db:
    SCHEMA_VERSION_NEW = 0

    def __init__(self, db_path, schema_dir):
        self.db_path = db_path
        self.migration(schema_dir)

    def execute(self, callback: Callable[[Cursor], None], fetch: Fetch = Fetch.NONE)\
            -> Union[sqlite3.Row, List[sqlite3.Row], None]:
        """
        :param callback:
        :param fetch:
        :return:
        """
        with closing(sqlite3.connect(self.db_path)) as connection:
            def sql_trace_callback(raw_sql):
                logger.debug('SQL: {}'.format(raw_sql))
            connection.set_trace_callback(sql_trace_callback)

            connection.row_factory = sqlite3.Row  # https://docs.python.org/3/library/sqlite3.html#row-objects

            cursor = connection.cursor()
            callback(cursor)
            connection.commit()

            if fetch == Fetch.ONE:
                return cursor.fetchone()  # type: sqlite3.Row
            elif fetch == Fetch.ALL:
                return cursor.fetchall()  # type: List[sqlite3.Row]
            else:
                return None

    def execute_simple(self, sql: str, params: Iterable = None, fetch: Fetch = Fetch.NONE):
        """
        :param sql:
        :param params:
        :param fetch:
        :return:
        """
        def callback(cursor: Cursor):
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

        return self.execute(callback, fetch)

    def migration(self, schema_dir):
        """
        Create database if not exists.
        Update schema if not up to date.
        """
        if not os.path.isfile(self.db_path):
            logger.info('MIGRATION: Applies initial schema')
            self._execute_schema(schema_dir, 0)

        schema_version_now = self._load_schema_version()
        if self.SCHEMA_VERSION_NEW == schema_version_now:
            return

        for version in range(schema_version_now+1, self.SCHEMA_VERSION_NEW+1):
            logger.info('MIGRATION: Schema version: now = {}, new = {}'
                        .format(schema_version_now, self.SCHEMA_VERSION_NEW))
            self._execute_schema(schema_dir, version)

        logger.info('MIGRATION: Migration ended')

    def _execute_schema(self, schema_dir: str, version: int):
        with open(schema_dir + '{}.sql'.format(version), 'r') as f:
            sql = f.read()

        def callback(cursor: Cursor):
            cursor.executescript(sql)  # Runs multiple sqls.

        self.execute(callback)

        self._update_schema_version(version)

    def _load_schema_version(self) -> int:
        """
        https://www.sqlite.org/pragma.html#pragma_user_version
        :return:
        """
        sql = (
            'PRAGMA user_version'
        )
        row = self.execute_simple(sql, fetch=Fetch.ONE)  # type: sqlite3.Row
        return row['user_version']

    def _update_schema_version(self, schema_version: int):
        sql = (
            'PRAGMA user_version = {}'.format(schema_version)  # PRAGMA values can not be prarams.
        )
        self.execute_simple(sql)


class DbException(Exception):
    pass


if __name__ == '__main__':
    path = os.path.realpath(__file__)
    dir_path = os.path.dirname(path)
    print(dir_path)
    db = Db(dir_path+'/../../database.db', dir_path+'/../schemas/')
