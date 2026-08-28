"""One definition of "today" for the whole app.

Anything that needs a day boundary calls clock.today(). Do not call
date.today(), SQLite's datetime('now') (UTC), or build a date in a route —
four disagreeing definitions of "today" is a bug zimmy-life-tracker already
paid for, and every cell inherits the fix instead of the bug."""

from datetime import date


def today():
    return date.today()
