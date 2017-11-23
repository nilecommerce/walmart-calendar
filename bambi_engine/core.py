from data_access import load_data


from sql.walmart_us.reports.sales_summary import query


data = load_data('wm_us_report_sales_summary', query(), 'acrox', force_refresh=False)

print(data)
