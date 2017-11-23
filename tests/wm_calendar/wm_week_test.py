from datetime import date, timedelta

from bambi_engine.wm_calendar.wm_week import WalmartWeek

ww = WalmartWeek(date(2017, 2, 13))

def wm_week_test():
    assert ww.wm_week == 201703

def lw_test():
    assert ww.lw() == 201702

def lylw_test():
    assert ww.lylw() == 201602

def l4w_test():
    assert ww.l4w() == (201651, 201652, 201701, 201702)
