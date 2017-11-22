from datetime import datetime, date, timedelta

from bambi_engine.wm_calendar.helpers import get_following_friday, get_fiscal_year_start_date

def get_following_friday_test():
    sat = date(2017, 5, 20)
    sun = date(2017, 5, 21)
    mon = date(2017, 5, 22)
    tues = date(2017, 5, 23)
    wed = date(2017, 5, 24)
    thurs = date(2017, 5, 25)
    fri = date(2017, 5, 26)

    following_friday = date(2017, 5, 26)

    assert get_following_friday(sat) == following_friday
    assert get_following_friday(sun) == following_friday
    assert get_following_friday(mon) == following_friday
    assert get_following_friday(tues) == following_friday
    assert get_following_friday(wed) == following_friday
    assert get_following_friday(thurs) == following_friday
    assert get_following_friday(fri) == following_friday

def get_fiscal_year_start_date_test():
    d1 = date(2018, 1, 4)
    d2 = date(2017, 4, 12)
    start_date = date(2017, 1, 28)
    assert get_fiscal_year_start_date(d1) == start_date
    assert get_fiscal_year_start_date(d2) == start_date
