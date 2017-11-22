from sqlalchemy.sql import text

from db import connection
from sql.walmart_us.sp.report_sales_summary import query

conn = connection()
q = text('SELECT * FROM Client')

data = conn.execute(q).fetchall()
print(data)

# print(query())
