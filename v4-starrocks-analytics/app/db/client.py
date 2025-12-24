import pymysql
import os

def get_conn():
    return pymysql.connect(
        host=os.getenv("STARROCKS_HOST", "127.0.0.1"),
        port=int(os.getenv("STARROCKS_PORT", 9030)),
        user=os.getenv("STARROCKS_USER", "root"),
        password=os.getenv("STARROCKS_PASSWORD", ""),
        database=os.getenv("STARROCKS_DB", "analytics"),
        autocommit=True,
    )

