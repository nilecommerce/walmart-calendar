from datetime import datetime, date, timedelta

import bambi_engine.core.wm_calendar.helpers as h

def get_following_friday_test():
    sat = date(2017, 5, 20)
    sun = date(2017, 5, 21)
    mon = date(2017, 5, 22)
    tues = date(2017, 5, 23)
    wed = date(2017, 5, 24)
    thurs = date(2017, 5, 25)
    fri = date(2017, 5, 26)

    following_friday = date(2017, 5, 26)

    assert h.get_following_friday(sat) == following_friday
    assert h.get_following_friday(sun) == following_friday
    assert h.get_following_friday(mon) == following_friday
    assert h.get_following_friday(tues) == following_friday
    assert h.get_following_friday(wed) == following_friday
    assert h.get_following_friday(thurs) == following_friday
    assert h.get_following_friday(fri) == following_friday

def get_previous_saturday_test():
    sat = date(2017, 5, 20)
    sun = date(2017, 5, 21)
    mon = date(2017, 5, 22)
    tues = date(2017, 5, 23)
    wed = date(2017, 5, 24)
    thurs = date(2017, 5, 25)
    fri = date(2017, 5, 26)

    previous_saturday = date(2017, 5, 20)

    assert h.get_previous_saturday(sat) == previous_saturday
    assert h.get_previous_saturday(sun) == previous_saturday
    assert h.get_previous_saturday(mon) == previous_saturday
    assert h.get_previous_saturday(tues) == previous_saturday
    assert h.get_previous_saturday(wed) == previous_saturday
    assert h.get_previous_saturday(thurs) == previous_saturday
    assert h.get_previous_saturday(fri) == previous_saturday

def get_fiscal_year_start_date_test():
    d1 = date(2018, 1, 4)
    d2 = date(2017, 4, 12)
    start_date = date(2017, 1, 28)
    assert h.get_fiscal_year_start_date(d1) == start_date
    assert h.get_fiscal_year_start_date(d2) == start_date

def wm_week_test():
    assert h.get_wm_week(date(2018, 1, 26)) == 201752
    assert h.get_wm_week(date(2018, 1, 30)) == 201801
    assert h.get_wm_week(date(2020, 1, 31)) == 201953
    assert h.get_wm_week(date(2017, 2, 2)) == 201701

def get_weeks_between_dates_inclusive_test():
    start_date = date(2016, 4, 24)
    end_date = date(2017, 3, 12)

    assert h.get_weeks_between_dates_inclusive(start_date, end_date) == (
        201613, 201614, 201615, 201616, 201617, 201618, 201619,
        201620, 201621, 201622, 201623, 201624, 201625, 201626,
        201627, 201628, 201629, 201630, 201631, 201632, 201633,
        201634, 201635, 201636, 201637, 201638, 201639, 201640,
        201641, 201642, 201643, 201644, 201645, 201646, 201647,
        201648, 201649, 201650, 201651, 201652, 201701, 201702,
        201703, 201704, 201705, 201706, 201707)
