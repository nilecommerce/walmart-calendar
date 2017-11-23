import pandas as pd
from sqlalchemy.sql import text

from db import connection
from sql.walmart_us.reports.sales_summary import query

conn = connection(name="acrox")
q = text(query())
df = pd.read_sql_query(q, conn)

print(df)
