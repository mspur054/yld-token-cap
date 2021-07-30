from contextlib import contextmanager

import psycopg2


class Database(object):
    def __init__(
        self, database: str, username: str, password: str, host: str, port: int
    ):
        self.conn_url = f'postgresql://{username}:{password}@{host}:{port}/{database}'
        
    @contextmanager
    def managed_cursor(self, cursor_factory=None):
        self.conn = psycopg2.connect(self.conn_url)
        self.conn.autocommit = True
        self.curr = self.conn.cursor(cursor_factory=cursor_factory)
        try:
            yield self.curr
        finally:
            self.curr.close()
            self.conn.close()
