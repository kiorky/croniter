try:
    import unittest2 as unittest
except ImportError:
    import unittest

from croniter import ZoneInfo, pytz


class TestCase(unittest.TestCase):
    """
    We use this base class for all the tests in this package.
    If necessary, we can put common utility or setup code in here.
    """

    def tz_localize(self, dt, tz):
        tz = self.tz(tz)
        if ZoneInfo:
            return dt.replace(tzinfo=tz)
        if pytz:
            return tz.localize(dt)
        raise SystemError("We should either have pytz or ZoneInfo")

    def tz(self, tz):
        if isinstance(tz, str):
            if ZoneInfo:
                return ZoneInfo(tz)
            if pytz:
                return pytz.timezone(tz)
            raise SystemError("We should either have pytz or ZoneInfo")
        return tz

    def as_tz(self, dt, tz):
        return dt.astimezone(self.tz(tz))
