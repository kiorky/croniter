try:
    import unittest2 as unittest
except ImportError:
    import unittest

from croniter import cron_m


class TestCase(unittest.TestCase):
    """
    We use this base class for all the tests in this package.
    If necessary, we can put common utility or setup code in here.
    """

    maxDiff = 10 ** 10

    def tz_localize(self, dt, tz):
        return cron_m.tz_localize(dt, tz)

    def tz(self, tz):
        return cron_m.get_tz(tz)

    def as_tz(self, dt, tz):
        return cron_m.as_tz(dt, tz)
