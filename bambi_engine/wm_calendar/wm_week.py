from datetime import datetime, date, timedelta
import math

from .helpers import get_fiscal_year_start_date

def wm_week(d=date.today()):
    '''
    Returns the WM Week for the date passed into the method.
    If no date is passed in, the methods defaults to today.
    '''
    fiscal_year_start_date = get_fiscal_year_start_date(d)

    # Get the day of WM fiscal year
    day_of_wm_year = (d - fiscal_year_start_date).days + 1

    # Get week number by dividing day number by 7 and rounding up
    wm_week_nbr = math.ceil(day_of_wm_year/7)
    fiscal_year = fiscal_year_start_date.year

    # Return WM Week as an int
    return (fiscal_year * 100) + wm_week_nbr

def lw():
    '''
    Returns the last WM Week
    '''
    lw_date = date.today() - timedelta(days=7)
    return wm_week(lw_date)

def week_offset(wks=0):
    '''
    Returns a WM Week offset by the passed in number of weeks from the current week
    '''
    d = date.today() + timedelta(weeks=wks)
    return wm_week(d)
