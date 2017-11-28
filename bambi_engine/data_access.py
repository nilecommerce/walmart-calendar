import os
from urllib.parse import quote_plus
import json

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
    # check redis cache for cached data
    cached_data = r.get(key)

    # if no data is found in the cache or the force refresh flag is true
    if((cached_data is None) | (force_refresh is True)):
        # query data from database
        conn = db_conn(name=db_name)
        df = pd.read_sql_query(text(query), conn)

        # prepare data for cache
        # saving column order is neccesary to reconstruct dataframes in the correct order
        data = {}
        data['column_order'] = list(df.keys())
        data['dataframe'] = df.to_dict(orient='records')

        # add data to the cache and set the expire time on the record
        r.set(key, json.dumps(data))
        r.expire(key, expire_time)
    else:
        # convert cached json back to dictionary
        data = json.loads(cached_data)
        df = pd.DataFrame.from_dict(data['dataframe'])
        
        # redorder columns to match original data structure
        df = df[data['column_order']]

    # return pandas dataframe object
    return df
