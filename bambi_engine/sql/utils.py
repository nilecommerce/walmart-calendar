
def get_week_filter(weeks):
    week_filter = 'IN {}'.format(weeks) if isinstance(weeks, tuple) else '= {}'.format(weeks)
    return week_filter

def combine_weeks(*args):
    weeks = []
    for x in args:
        weeks.append(x) if isinstance(x, int) else weeks.extend(x)
    return tuple(weeks)
