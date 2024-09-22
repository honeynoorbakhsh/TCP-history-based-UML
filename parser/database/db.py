import sqlite3
from contextlib import contextmanager

from parser import configurations as conf


@contextmanager
def get_connection(db_name, db_path=".") -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect("%s/%s" % (db_path, db_name))
        yield conn
        conn.commit()
    finally:
        if conn is not None:
            conn.close()


@contextmanager
def get_cursor() -> sqlite3.Cursor:
    with get_connection(db_name="database.sqlite", db_path=conf.BASE_DIR) as conn:
        yield conn.cursor()
