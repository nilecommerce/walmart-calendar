import os
from urllib.parse import quote_plus

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import redis
import pandas as pd

load_dotenv(find_dotenv())

def db_conn(name=os.environ.get("DB_NAME")):
    params = quote_plus("DRIVER={driver};SERVER={server};DATABASE={db};UID={user};PWD={password}".format(
        driver="ODBC Driver 13 for SQL Server",
        server = os.environ.get("DB_HOST"),
        db = name,
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASS")))

    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    return engine.connect()

def redis_conn():
    return redis.StrictRedis(
        host = os.environ.get('REDIS_HOST'),
        port = os.environ.get('REDIS_PORT'),
        password = os.environ.get('REDIS_PASS'))

def load_data(query_id, query, db_name, expire_time=1440, force_refresh=False):

    r = redis_conn()
    key = '{}_{}'.format(db_name, query_id)
    cached_data = r.get(key)

    if((cached_data is None) | (force_refresh is True)):
        conn = db_conn(name=db_name)
        df = pd.read_sql_query(text(query), conn)

        r.set(key, df.to_json(orient='records'))
        r.expire(key, expire_time)
    else:
        df = pd.read_json(path_or_buf=cached_data, orient='records')
    return df
