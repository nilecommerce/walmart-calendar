from datetime import datetime, date, timedelta

from bambi_engine.wm_calendar.wm_week import wm_week, lw, week_offset

def wm_week_test():
    assert wm_week(date(2018, 1, 26)) == 201752
    assert wm_week(date(2018, 1, 30)) == 201801
    assert wm_week(date(2020, 1, 31)) == 201953

def lw_test():
    assert lw() == 201742

def week_offset_test():
    assert week_offset(1) == 201744
