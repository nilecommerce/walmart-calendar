from flask import Flask

from bambi_engine.data_access import load_data
from bambi_engine.sql.walmart_us.reports.sales_summary import query

app = Flask(__name__)

@app.route('/')
def hello_world():
    data = load_data('wm_us_report_sales_summary', query(), 'acrox', force_refresh=False)
    return data.to_json(orient='records')
