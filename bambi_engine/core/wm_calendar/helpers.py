from datetime import datetime, date, timedelta
import math

def get_following_friday(date_obj):
    '''
    Returns the Friday immediately following the date passed in.
    If the date passed in is a Friday it should return itself.
    '''
    # In Python isoweekday Monday is 1 and Sunday is 7
    weekday = date_obj.isoweekday()
    if weekday > 5:
        distance_from_fri = 7 - abs(5 - weekday)
    else:
        distance_from_fri = abs(5 - weekday)
    return date_obj + timedelta(days=distance_from_fri)

def get_previous_saturday(date_obj):
    '''
    Returns the Saturday prior to the date passed in.
    If the date passed in is a Saturday it should return itself.
    '''
    # In Python isoweekday Monday is 1 and Sunday is 7
    weekday = date_obj.isoweekday()
    if weekday < 6:
        distance_from_sat = 7 - abs(6 - weekday)
    else:
        distance_from_sat = abs(6 - weekday)
    return date_obj - timedelta(days=distance_from_sat)

def get_fiscal_year_start_date(date_obj):
    '''
    Returns the start date of the fiscal year of the date passed in.
    ** Walmarts fiscal year starts with the first WM Week that ends in Feburary
    ** WM Weeks start on Saturday and end on Friday
    '''
    # Find the next Friday that follows the given date
    following_friday = get_following_friday(date_obj)

    # Determine Walmart fiscal year
    if date_obj.month == 1 & following_friday.month != 2:
        fiscal_year = date_obj.year - 1
    else:
        fiscal_year = date_obj.year

    # Find the first Friday in Feburary of the fiscal year we just found
    feb_1 = date(fiscal_year, 2, 1)
    first_feb_friday = get_following_friday(feb_1)

    # Get the first day of the WM Week that ends on the first Friday we just found
    fiscal_year_start_date = first_feb_friday - timedelta(days=6)
    return fiscal_year_start_date


def get_wm_week(d):
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

def get_weeks_between_dates_inclusive(start_date, end_date):
    '''
    Returns tuple of the WM Weeks between the two days passed to the method,
    including the weeks that the dates are in.
    '''
    weeks = []
    weeks_start = get_previous_saturday(start_date)
    weeks_end = get_following_friday(end_date)
    nbr_of_weeks = math.ceil(((weeks_end - weeks_start).days + 1) / 7)

    for i in range(nbr_of_weeks):
      d = start_date + timedelta(weeks=i)
      weeks.append(get_wm_week(d))

    return tuple(weeks)
