from datetime import date, timedelta
import math

from .helpers import get_wm_week, get_fiscal_year_start_date, get_weeks_between_dates_inclusive

class WalmartWeek(object):

    def __init__(self, d=date.today()):
        self.date = d
        self.wm_week = get_wm_week(d)

    def lw(self):
        d = self.date - timedelta(weeks=1)
        return get_wm_week(d)

    def lylw(self):
        d = self.date - timedelta(weeks=53)
        return get_wm_week(d)

    def l4w(self):
        d1 = self.date - timedelta(weeks=4)
        d2 = self.date - timedelta(weeks=1)
        return get_weeks_between_dates_inclusive(d1, d2)

    def n4w(self):
        d = self.date + timedelta(weeks=3)
        return get_weeks_between_dates_inclusive(self.date, d)

    def ytd(self):
        d1 = get_fiscal_year_start_date(self.date)
        d2 = self.date - timedelta(weeks=1)
        return get_weeks_between_dates_inclusive(d1, d2)

    def lyytd(self):
        d1 = get_fiscal_year_start_date(self.date - timedelta(weeks=53))
        d2 = self.date - timedelta(weeks=53)
        return get_weeks_between_dates_inclusive(d1, d2)
