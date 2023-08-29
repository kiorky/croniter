#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta
from functools import partial
from time import sleep
import pytz
from croniter import (croniter, CroniterBadDateError,  CroniterBadCronError,
                      CroniterNotAlphaError, CroniterUnsupportedSyntaxError)
from croniter.tests import base
import dateutil.tz


class CroniterTest(base.TestCase):

    def testSecondSec(self):
        base = datetime(2012, 4, 6, 13, 26, 10)
        itr = croniter('* * * * * 15,25', base)
        n = itr.get_next(datetime)
        self.assertEqual(15, n.second)
        n = itr.get_next(datetime)
        self.assertEqual(25, n.second)
        n = itr.get_next(datetime)
        self.assertEqual(15, n.second)
        self.assertEqual(27, n.minute)

    def testSecond(self):
        base = datetime(2012, 4, 6, 13, 26, 10)
        itr = croniter('*/1 * * * * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(base.year, n1.year)
        self.assertEqual(base.month, n1.month)
        self.assertEqual(base.day, n1.day)
        self.assertEqual(base.hour, n1.hour)
        self.assertEqual(base.minute, n1.minute)
        self.assertEqual(base.second + 1, n1.second)

    def testSecondRepeat(self):
        base = datetime(2012, 4, 6, 13, 26, 36)
        itr = croniter('* * * * * */15', base)
        n1 = itr.get_next(datetime)
        n2 = itr.get_next(datetime)
        n3 = itr.get_next(datetime)
        self.assertEqual(base.year, n1.year)
        self.assertEqual(base.month, n1.month)
        self.assertEqual(base.day, n1.day)
        self.assertEqual(base.hour, n1.hour)
        self.assertEqual(base.minute, n1.minute)
        self.assertEqual(45, n1.second)
        self.assertEqual(base.year, n2.year)
        self.assertEqual(base.month, n2.month)
        self.assertEqual(base.day, n2.day)
        self.assertEqual(base.hour, n2.hour)
        self.assertEqual(base.minute + 1, n2.minute)
        self.assertEqual(0, n2.second)
        self.assertEqual(base.year, n3.year)
        self.assertEqual(base.month, n3.month)
        self.assertEqual(base.day, n3.day)
        self.assertEqual(base.hour, n3.hour)
        self.assertEqual(base.minute + 1, n3.minute)
        self.assertEqual(15, n3.second)

    def testMinute(self):
        # minute asterisk
        base = datetime(2010, 1, 23, 12, 18)
        itr = croniter('*/1 * * * *', base)
        n1 = itr.get_next(datetime)    # 19
        self.assertEqual(base.year, n1.year)
        self.assertEqual(base.month, n1.month)
        self.assertEqual(base.day, n1.day)
        self.assertEqual(base.hour, n1.hour)
        self.assertEqual(base.minute, n1.minute - 1)
        for i in range(39):  # ~ 58
            itr.get_next()
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.minute, 59)
        n3 = itr.get_next(datetime)
        self.assertEqual(n3.minute, 0)
        self.assertEqual(n3.hour, 13)

        itr = croniter('*/5 * * * *', base)
        n4 = itr.get_next(datetime)
        self.assertEqual(n4.minute, 20)
        for i in range(6):
            itr.get_next()
        n5 = itr.get_next(datetime)
        self.assertEqual(n5.minute, 55)
        n6 = itr.get_next(datetime)
        self.assertEqual(n6.minute, 0)
        self.assertEqual(n6.hour, 13)

    def testHour(self):
        base = datetime(2010, 1, 24, 12, 2)
        itr = croniter('0 */3 * * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.hour, 15)
        self.assertEqual(n1.minute, 0)
        for i in range(2):
            itr.get_next()
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.hour, 0)
        self.assertEqual(n2.day, 25)

    def testDay(self):
        base = datetime(2010, 2, 24, 12, 9)
        itr = croniter('0 0 */3 * *', base)
        n1 = itr.get_next(datetime)
        # 1 4 7 10 13 16 19 22 25 28
        self.assertEqual(n1.day, 25)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.day, 28)
        n3 = itr.get_next(datetime)
        self.assertEqual(n3.day, 1)
        self.assertEqual(n3.month, 3)

        # test leap year
        base = datetime(1996, 2, 27)
        itr = croniter('0 0 * * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.day, 28)
        self.assertEqual(n1.month, 2)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.day, 29)
        self.assertEqual(n2.month, 2)

        base2 = datetime(2000, 2, 27)
        itr2 = croniter('0 0 * * *', base2)
        n3 = itr2.get_next(datetime)
        self.assertEqual(n3.day, 28)
        self.assertEqual(n3.month, 2)
        n4 = itr2.get_next(datetime)
        self.assertEqual(n4.day, 29)
        self.assertEqual(n4.month, 2)

    def testWeekDay(self):
        base = datetime(2010, 2, 25)
        itr = croniter('0 0 * * sat', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.isoweekday(), 6)
        self.assertEqual(n1.day, 27)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.isoweekday(), 6)
        self.assertEqual(n2.day, 6)
        self.assertEqual(n2.month, 3)

        base = datetime(2010, 1, 25)
        itr = croniter('0 0 1 * wed', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.month, 1)
        self.assertEqual(n1.day, 27)
        self.assertEqual(n1.year, 2010)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.month, 2)
        self.assertEqual(n2.day, 1)
        self.assertEqual(n2.year, 2010)
        n3 = itr.get_next(datetime)
        self.assertEqual(n3.month, 2)
        self.assertEqual(n3.day, 3)
        self.assertEqual(n3.year, 2010)

    def testNthWeekDay(self):
        base = datetime(2010, 2, 25)
        itr = croniter('0 0 * * sat#1', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.isoweekday(), 6)
        self.assertEqual(n1.day, 6)
        self.assertEqual(n1.month, 3)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.isoweekday(), 6)
        self.assertEqual(n2.day, 3)
        self.assertEqual(n2.month, 4)

        base = datetime(2010, 1, 25)
        itr = croniter('0 0 * * wed#5', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.month, 3)
        self.assertEqual(n1.day, 31)
        self.assertEqual(n1.year, 2010)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.month, 6)
        self.assertEqual(n2.day, 30)
        self.assertEqual(n2.year, 2010)
        n3 = itr.get_next(datetime)
        self.assertEqual(n3.month, 9)
        self.assertEqual(n3.day, 29)
        self.assertEqual(n3.year, 2010)

    def testWeekDayDayAnd(self):
        base = datetime(2010, 1, 25)
        itr = croniter('0 0 1 * mon', base, day_or=False)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.month, 2)
        self.assertEqual(n1.day, 1)
        self.assertEqual(n1.year, 2010)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.month, 3)
        self.assertEqual(n2.day, 1)
        self.assertEqual(n2.year, 2010)
        n3 = itr.get_next(datetime)
        self.assertEqual(n3.month, 11)
        self.assertEqual(n3.day, 1)
        self.assertEqual(n3.year, 2010)

    def testMonth(self):
        base = datetime(2010, 1, 25)
        itr = croniter('0 0 1 * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.month, 2)
        self.assertEqual(n1.day, 1)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.month, 3)
        self.assertEqual(n2.day, 1)
        for i in range(8):
            itr.get_next()
        n3 = itr.get_next(datetime)
        self.assertEqual(n3.month, 12)
        self.assertEqual(n3.year, 2010)
        n4 = itr.get_next(datetime)
        self.assertEqual(n4.month, 1)
        self.assertEqual(n4.year, 2011)

    def testLastDayOfMonth(self):
        base = datetime(2015, 9, 4)
        itr = croniter('0 0 l * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.month, 9)
        self.assertEqual(n1.day, 30)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.month, 10)
        self.assertEqual(n2.day, 31)
        n3 = itr.get_next(datetime)
        self.assertEqual(n3.month, 11)
        self.assertEqual(n3.day, 30)
        n4 = itr.get_next(datetime)
        self.assertEqual(n4.month, 12)
        self.assertEqual(n4.day, 31)

    def testRangeWithUppercaseLastDayOfMonth(self):
        base = datetime(2015, 9, 4)
        itr = croniter('0 0 29-L * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.month, 9)
        self.assertEqual(n1.day, 29)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.month, 9)
        self.assertEqual(n2.day, 30)

    def testPrevLastDayOfMonth(self):
        base = datetime(2009, 12, 31, hour=20)
        itr = croniter('0 0 l * *', base)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 12)
        self.assertEqual(n1.day, 31)

        base = datetime(2009, 12, 31)
        itr = croniter('0 0 l * *', base)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 11)
        self.assertEqual(n1.day, 30)

        base = datetime(2010, 1, 5)
        itr = croniter('0 0 l * *', base)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 12)
        self.assertEqual(n1.day, 31)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 11)
        self.assertEqual(n1.day, 30)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 10)
        self.assertEqual(n1.day, 31)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 9)
        self.assertEqual(n1.day, 30)

        base = datetime(2010, 1, 31, minute=2)
        itr = croniter('* * l * *', base)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 1)
        self.assertEqual(n1.day, 31)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 1)
        self.assertEqual(n1.day, 31)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 12)
        self.assertEqual(n1.day, 31)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.month, 12)
        self.assertEqual(n1.day, 31)

    def testError(self):
        itr = croniter('* * * * *')
        self.assertRaises(TypeError, itr.get_next, str)
        self.assertRaises(ValueError, croniter, '* * * *')
        self.assertRaises(ValueError, croniter, '* * 5-1 * *')
        self.assertRaises(ValueError, croniter, '-90 * * * *')
        self.assertRaises(ValueError, croniter, 'a * * * *')
        self.assertRaises(ValueError, croniter, '* * * janu-jun *')
        self.assertRaises(ValueError, croniter, '1-1_0 * * * *')
        self.assertRaises(ValueError, croniter, '0-10/ * * * *')
        self.assertRaises(CroniterBadCronError, croniter, "0-1& * * * *", datetime.now())

    def testSundayToThursdayWithAlphaConversion(self):
        base = datetime(2010, 8, 25, 15, 56)  # wednesday
        itr = croniter("30 22 * * sun-thu", base)
        next = itr.get_next(datetime)

        self.assertEqual(base.year, next.year)
        self.assertEqual(base.month, next.month)
        self.assertEqual(base.day, next.day)
        self.assertEqual(22, next.hour)
        self.assertEqual(30, next.minute)

    def testOptimizeCronExpressions(self):
        """ Non-optimal cron expressions that can be simplified."""
        wildcard = ['*']
        m, h, d, mon, dow, s = range(6)
        # Test each field individually
        self.assertEqual(croniter('0-59 0 1 1 0').expanded[m], wildcard)
        self.assertEqual(croniter('0 0-23 1 1 0').expanded[h], wildcard)
        self.assertEqual(croniter('0 0 1-31 1 0').expanded[d], wildcard)
        self.assertEqual(croniter('0 0 1 1-12 0').expanded[mon], wildcard)
        self.assertEqual(croniter('0 0 1 1 0-6').expanded[dow], wildcard)
        self.assertEqual(croniter('0 0 1 1 1-7').expanded[dow], wildcard)
        self.assertEqual(croniter('0 0 1 1 1-7,sat#3').expanded[dow], wildcard)
        self.assertEqual(croniter('0 0 1 1 0 0-59').expanded[s], wildcard)
        # Real life examples
        self.assertEqual(croniter('30 1-12,0,10-23 15-21 * fri').expanded[h], wildcard)
        self.assertEqual(croniter('30 1-23,0 15-21 * fri').expanded[h], wildcard)

    def testBlockDupRanges(self):
        """ Ensure that duplicate/overlapping ranges are squashed """
        m, h, d, mon, dow, s = range(6)
        self.assertEqual(croniter('* 5,5,1-6 * * *').expanded[h], [1,2,3,4,5,6])
        self.assertEqual(croniter('* * * * 2-3,4-5,3,3,3').expanded[dow], [2,3,4,5])
        self.assertEqual(croniter('* * * * * 1,5,*/20,20,15').expanded[s], [0, 1, 5, 15, 20, 40])
        self.assertEqual(croniter('* 4,1-4,5,4 * * *').expanded[h], [1, 2, 3, 4, 5])
        # Real life example
        self.assertEqual(croniter('59 23 * 1 wed,fri,mon-thu,tue,tue').expanded[dow], [1,2,3,4,5])

    def testPrevMinute(self):
        base = datetime(2010, 8, 25, 15, 56)
        itr = croniter('*/1 * * * *', base)
        prev = itr.get_prev(datetime)
        self.assertEqual(base.year, prev.year)
        self.assertEqual(base.month, prev.month)
        self.assertEqual(base.day, prev.day)
        self.assertEqual(base.hour, prev.hour)
        self.assertEqual(base.minute, prev.minute + 1)

        base = datetime(2010, 8, 25, 15, 0)
        itr = croniter('*/1 * * * *', base)
        prev = itr.get_prev(datetime)
        self.assertEqual(base.year, prev.year)
        self.assertEqual(base.month, prev.month)
        self.assertEqual(base.day, prev.day)
        self.assertEqual(base.hour, prev.hour + 1)
        self.assertEqual(59, prev.minute)

        base = datetime(2010, 8, 25, 0, 0)
        itr = croniter('*/1 * * * *', base)
        prev = itr.get_prev(datetime)
        self.assertEqual(base.year, prev.year)
        self.assertEqual(base.month, prev.month)
        self.assertEqual(base.day, prev.day + 1)
        self.assertEqual(23, prev.hour)
        self.assertEqual(59, prev.minute)

    def testPrevDayOfMonthWithCrossing(self):
        """
        Test getting previous occurrence that crosses into previous month.
        """
        base = datetime(2012, 3, 15, 0, 0)
        itr = croniter('0 0 22 * *', base)
        prev = itr.get_prev(datetime)
        self.assertEqual(prev.year, 2012)
        self.assertEqual(prev.month, 2)
        self.assertEqual(prev.day, 22)
        self.assertEqual(prev.hour, 0)
        self.assertEqual(prev.minute, 0)

    def testPrevWeekDay(self):
        base = datetime(2010, 8, 25, 15, 56)
        itr = croniter('0 0 * * sat,sun', base)
        prev1 = itr.get_prev(datetime)
        self.assertEqual(prev1.year, base.year)
        self.assertEqual(prev1.month, base.month)
        self.assertEqual(prev1.day, 22)
        self.assertEqual(prev1.hour, 0)
        self.assertEqual(prev1.minute, 0)

        prev2 = itr.get_prev(datetime)
        self.assertEqual(prev2.year, base.year)
        self.assertEqual(prev2.month, base.month)
        self.assertEqual(prev2.day, 21)
        self.assertEqual(prev2.hour, 0)
        self.assertEqual(prev2.minute, 0)

        prev3 = itr.get_prev(datetime)
        self.assertEqual(prev3.year, base.year)
        self.assertEqual(prev3.month, base.month)
        self.assertEqual(prev3.day, 15)
        self.assertEqual(prev3.hour, 0)
        self.assertEqual(prev3.minute, 0)

    def testPrevNthWeekDay(self):
        base = datetime(2010, 8, 25, 15, 56)
        itr = croniter('0 0 * * sat#1,sun#2', base)
        prev1 = itr.get_prev(datetime)
        self.assertEqual(prev1.year, base.year)
        self.assertEqual(prev1.month, base.month)
        self.assertEqual(prev1.day, 8)
        self.assertEqual(prev1.hour, 0)
        self.assertEqual(prev1.minute, 0)

        prev2 = itr.get_prev(datetime)
        self.assertEqual(prev2.year, base.year)
        self.assertEqual(prev2.month, base.month)
        self.assertEqual(prev2.day, 7)
        self.assertEqual(prev2.hour, 0)
        self.assertEqual(prev2.minute, 0)

        prev3 = itr.get_prev(datetime)
        self.assertEqual(prev3.year, base.year)
        self.assertEqual(prev3.month, 7)
        self.assertEqual(prev3.day, 11)
        self.assertEqual(prev3.hour, 0)
        self.assertEqual(prev3.minute, 0)

    def testPrevWeekDay2(self):
        base = datetime(2010, 8, 25, 15, 56)
        itr = croniter('10 0 * * 0', base)
        prev = itr.get_prev(datetime)
        self.assertEqual(prev.day, 22)
        self.assertEqual(prev.hour, 0)
        self.assertEqual(prev.minute, 10)

    def testISOWeekday(self):
        base = datetime(2010, 2, 25)
        itr = croniter('0 0 * * 7', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.isoweekday(), 7)
        self.assertEqual(n1.day, 28)
        n2 = itr.get_next(datetime)
        self.assertEqual(n2.isoweekday(), 7)
        self.assertEqual(n2.day, 7)
        self.assertEqual(n2.month, 3)

    def testBug1(self):
        base = datetime(2012, 2, 24)
        itr = croniter('5 0 */2 * *', base)
        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.hour, 0)
        self.assertEqual(n1.minute, 5)
        self.assertEqual(n1.month, 2)
        # month starts from 1, 3 .... then 21, 23
        # so correct is not 22  but 23
        self.assertEqual(n1.day, 23)

    def testBug2(self):
        base = datetime(2012, 1, 1, 0, 0)
        iter = croniter('0 * * 3 *', base)
        n1 = iter.get_next(datetime)
        self.assertEqual(n1.year, base.year)
        self.assertEqual(n1.month, 3)
        self.assertEqual(n1.day, base.day)
        self.assertEqual(n1.hour, base.hour)
        self.assertEqual(n1.minute, base.minute)

        n2 = iter.get_next(datetime)
        self.assertEqual(n2.year, base.year)
        self.assertEqual(n2.month, 3)
        self.assertEqual(n2.day, base.day)
        self.assertEqual(n2.hour, base.hour + 1)
        self.assertEqual(n2.minute, base.minute)

        n3 = iter.get_next(datetime)
        self.assertEqual(n3.year, base.year)
        self.assertEqual(n3.month, 3)
        self.assertEqual(n3.day, base.day)
        self.assertEqual(n3.hour, base.hour + 2)
        self.assertEqual(n3.minute, base.minute)

    def testBug3(self):
        base = datetime(2013, 3, 1, 12, 17, 34, 257877)
        c = croniter('00 03 16,30 * *', base)

        n1 = c.get_next(datetime)
        self.assertEqual(n1.month, 3)
        self.assertEqual(n1.day, 16)

        n2 = c.get_next(datetime)
        self.assertEqual(n2.month, 3)
        self.assertEqual(n2.day, 30)

        n3 = c.get_next(datetime)
        self.assertEqual(n3.month, 4)
        self.assertEqual(n3.day, 16)

        n4 = c.get_prev(datetime)
        self.assertEqual(n4.month, 3)
        self.assertEqual(n4.day, 30)

        n5 = c.get_prev(datetime)
        self.assertEqual(n5.month, 3)
        self.assertEqual(n5.day, 16)

        n6 = c.get_prev(datetime)
        self.assertEqual(n6.month, 2)
        self.assertEqual(n6.day, 16)

    def test_bug34(self):
        base = datetime(2012, 2, 24, 0, 0, 0)
        itr = croniter('* * 31 2 *', base)
        try:
            itr.get_next(datetime)
        except (CroniterBadDateError,) as ex:
            self.assertEqual("{0}".format(ex),
                             'failed to find next date')

    def testBug57(self):
        base = datetime(2012, 2, 24, 0, 0, 0)
        itr = croniter('0 4/6 * * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.hour, 4)
        self.assertEqual(n1.minute, 0)
        self.assertEqual(n1.month, 2)
        self.assertEqual(n1.day, 24)

        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.hour, 22)
        self.assertEqual(n1.minute, 0)
        self.assertEqual(n1.month, 2)
        self.assertEqual(n1.day, 23)

        itr = croniter('0 0/6 * * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.hour, 6)
        self.assertEqual(n1.minute, 0)
        self.assertEqual(n1.month, 2)
        self.assertEqual(n1.day, 24)

        n1 = itr.get_prev(datetime)
        self.assertEqual(n1.hour, 0)
        self.assertEqual(n1.minute, 0)
        self.assertEqual(n1.month, 2)
        self.assertEqual(n1.day, 24)

    def test_multiple_months(self):
        base = datetime(2016, 3, 1, 0, 0, 0)
        itr = croniter('0 0 1 3,6,9,12 *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.hour, 0)
        self.assertEqual(n1.month, 6)
        self.assertEqual(n1.day, 1)
        self.assertEqual(n1.year, 2016)

        base = datetime(2016, 2, 15, 0, 0, 0)
        itr = croniter('0 0 1 3,6,9,12 *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.hour, 0)
        self.assertEqual(n1.month, 3)
        self.assertEqual(n1.day, 1)
        self.assertEqual(n1.year, 2016)

        base = datetime(2016, 12, 3, 10, 0, 0)
        itr = croniter('0 0 1 3,6,9,12 *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.hour, 0)
        self.assertEqual(n1.month, 3)
        self.assertEqual(n1.day, 1)
        self.assertEqual(n1.year, 2017)

        # The result with this parameters was incorrect.
        # self.assertEqual(p1.month, 12
        # AssertionError: 9 != 12
        base = datetime(2016, 3, 1, 0, 0, 0)
        itr = croniter('0 0 1 3,6,9,12 *', base)
        p1 = itr.get_prev(datetime)
        self.assertEqual(p1.hour, 0)
        self.assertEqual(p1.month, 12)
        self.assertEqual(p1.day, 1)
        self.assertEqual(p1.year, 2015)

        # check my change resolves another hidden bug.
        base = datetime(2016, 2, 1, 0, 0, 0)
        itr = croniter('0 0 1,15,31 * *', base)
        p1 = itr.get_prev(datetime)
        self.assertEqual(p1.hour, 0)
        self.assertEqual(p1.month, 1)
        self.assertEqual(p1.day, 31)
        self.assertEqual(p1.year, 2016)

        base = datetime(2016, 6, 1, 0, 0, 0)
        itr = croniter('0 0 1 3,6,9,12 *', base)
        p1 = itr.get_prev(datetime)
        self.assertEqual(p1.hour, 0)
        self.assertEqual(p1.month, 3)
        self.assertEqual(p1.day, 1)
        self.assertEqual(p1.year, 2016)

        base = datetime(2016, 3, 1, 0, 0, 0)
        itr = croniter('0 0 1 1,3,6,9,12 *', base)
        p1 = itr.get_prev(datetime)
        self.assertEqual(p1.hour, 0)
        self.assertEqual(p1.month, 1)
        self.assertEqual(p1.day, 1)
        self.assertEqual(p1.year, 2016)

        base = datetime(2016, 3, 1, 0, 0, 0)
        itr = croniter('0 0 1 1,3,6,9,12 *', base)
        p1 = itr.get_prev(datetime)
        self.assertEqual(p1.hour, 0)
        self.assertEqual(p1.month, 1)
        self.assertEqual(p1.day, 1)
        self.assertEqual(p1.year, 2016)

    def test_rangeGenerator(self):
        base = datetime(2013, 3, 4, 0, 0)
        itr = croniter('1-9/2 0 1 * *', base)
        n1 = itr.get_next(datetime)
        n2 = itr.get_next(datetime)
        n3 = itr.get_next(datetime)
        n4 = itr.get_next(datetime)
        n5 = itr.get_next(datetime)
        self.assertEqual(n1.minute, 1)
        self.assertEqual(n2.minute, 3)
        self.assertEqual(n3.minute, 5)
        self.assertEqual(n4.minute, 7)
        self.assertEqual(n5.minute, 9)

    def testPreviousHour(self):
        base = datetime(2012, 6, 23, 17, 41)
        itr = croniter('* 10 * * *', base)
        prev1 = itr.get_prev(datetime)
        self.assertEqual(prev1.year, base.year)
        self.assertEqual(prev1.month, base.month)
        self.assertEqual(prev1.day, base.day)
        self.assertEqual(prev1.hour, 10)
        self.assertEqual(prev1.minute, 59)

    def testPreviousDay(self):
        base = datetime(2012, 6, 27, 0, 15)
        itr = croniter('* * 26 * *', base)
        prev1 = itr.get_prev(datetime)
        self.assertEqual(prev1.year, base.year)
        self.assertEqual(prev1.month, base.month)
        self.assertEqual(prev1.day, 26)
        self.assertEqual(prev1.hour, 23)
        self.assertEqual(prev1.minute, 59)

    def testPreviousMonth(self):
        base = datetime(2012, 6, 18, 0, 15)
        itr = croniter('* * * 5 *', base)
        prev1 = itr.get_prev(datetime)
        self.assertEqual(prev1.year, base.year)
        self.assertEqual(prev1.month, 5)
        self.assertEqual(prev1.day, 31)
        self.assertEqual(prev1.hour, 23)
        self.assertEqual(prev1.minute, 59)

    def testPreviousDow(self):
        base = datetime(2012, 5, 13, 18, 48)
        itr = croniter('* * * * sat', base)
        prev1 = itr.get_prev(datetime)
        self.assertEqual(prev1.year, base.year)
        self.assertEqual(prev1.month, base.month)
        self.assertEqual(prev1.day, 12)
        self.assertEqual(prev1.hour, 23)
        self.assertEqual(prev1.minute, 59)

    def testGetCurrent(self):
        base = datetime(2012, 9, 25, 11, 24)
        itr = croniter('* * * * *', base)
        res = itr.get_current(datetime)
        self.assertEqual(base.year, res.year)
        self.assertEqual(base.month, res.month)
        self.assertEqual(base.day, res.day)
        self.assertEqual(base.hour, res.hour)
        self.assertEqual(base.minute, res.minute)

    def testTimezone(self):
        base = datetime(2013, 3, 4, 12, 15)
        itr = croniter('* * * * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.tzinfo, None)

        tokyo = pytz.timezone('Asia/Tokyo')
        itr2 = croniter('* * * * *', tokyo.localize(base))
        n2 = itr2.get_next(datetime)
        self.assertEqual(n2.tzinfo.zone, 'Asia/Tokyo')

    def testTimezoneDateutil(self):
        tokyo = dateutil.tz.gettz('Asia/Tokyo')
        base = datetime(2013, 3, 4, 12, 15, tzinfo=tokyo)
        itr = croniter('* * * * *', base)
        n1 = itr.get_next(datetime)
        self.assertEqual(n1.tzinfo.tzname(n1), 'JST')

    def testInitNoStartTime(self):
        itr = croniter('* * * * *')
        sleep(.01)
        itr2 = croniter('* * * * *')
        # Greater does not exists in py26
        self.assertTrue(itr2.cur > itr.cur)

    def assertScheduleTimezone(self, callback, expected_schedule):
        for expected_date, expected_offset in expected_schedule:
            d = callback()
            self.assertEqual(expected_date, d.replace(tzinfo=None))
            self.assertEqual(expected_offset,
                             croniter._timedelta_to_seconds(d.utcoffset()))

    def testTimezoneWinterTime(self):
        tz = pytz.timezone('Europe/Athens')

        expected_schedule = [
            (datetime(2013, 10, 27, 2, 30, 0), 10800),
            (datetime(2013, 10, 27, 3, 0, 0), 10800),
            (datetime(2013, 10, 27, 3, 30, 0), 10800),
            (datetime(2013, 10, 27, 3, 0, 0), 7200),
            (datetime(2013, 10, 27, 3, 30, 0), 7200),
            (datetime(2013, 10, 27, 4, 0, 0), 7200),
            (datetime(2013, 10, 27, 4, 30, 0), 7200),
            ]

        start = datetime(2013, 10, 27, 2, 0, 0)
        ct = croniter('*/30 * * * *', tz.localize(start))
        self.assertScheduleTimezone(lambda: ct.get_next(datetime), expected_schedule)

        start = datetime(2013, 10, 27, 5, 0, 0)
        ct = croniter('*/30 * * * *', tz.localize(start))
        self.assertScheduleTimezone(lambda: ct.get_prev(datetime), reversed(expected_schedule))

    def testTimezoneSummerTime(self):
        tz = pytz.timezone('Europe/Athens')

        expected_schedule = [
            (datetime(2013, 3, 31, 1, 30, 0), 7200),
            (datetime(2013, 3, 31, 2, 0, 0), 7200),
            (datetime(2013, 3, 31, 2, 30, 0), 7200),
            (datetime(2013, 3, 31, 4, 0, 0), 10800),
            (datetime(2013, 3, 31, 4, 30, 0), 10800),
            ]

        start = datetime(2013, 3, 31, 1, 0, 0)
        ct = croniter('*/30 * * * *', tz.localize(start))
        self.assertScheduleTimezone(lambda: ct.get_next(datetime), expected_schedule)

        start = datetime(2013, 3, 31, 5, 0, 0)
        ct = croniter('*/30 * * * *', tz.localize(start))
        self.assertScheduleTimezone(lambda: ct.get_prev(datetime), reversed(expected_schedule))

    def test_std_dst(self):
        """
        DST tests

        This fixes https://github.com/taichino/croniter/issues/82

        """
        tz = pytz.timezone('Europe/Warsaw')
        # -> 2017-03-26 01:59+1:00 -> 03:00+2:00
        local_date = tz.localize(datetime(2017, 3, 26))
        val = croniter('0 0 * * *', local_date).get_next(datetime)
        self.assertEqual(val, tz.localize(datetime(2017, 3, 27)))
        #
        local_date = tz.localize(datetime(2017, 3, 26, 1))
        cr = croniter('0 * * * *', local_date)
        val = cr.get_next(datetime)
        self.assertEqual(val, tz.localize(datetime(2017, 3, 26, 3)))
        val = cr.get_current(datetime)
        self.assertEqual(val, tz.localize(datetime(2017, 3, 26, 3)))

        # -> 2017-10-29 02:59+2:00 -> 02:00+1:00
        local_date = tz.localize(datetime(2017, 10, 29))
        val = croniter('0 0 * * *', local_date).get_next(datetime)
        self.assertEqual(val, tz.localize(datetime(2017, 10, 30)))
        local_date = tz.localize(datetime(2017, 10, 29, 1, 59))
        val = croniter('0 * * * *', local_date).get_next(datetime)
        self.assertEqual(
            val.replace(tzinfo=None),
            tz.localize(datetime(2017, 10, 29, 2)).replace(tzinfo=None))
        local_date = tz.localize(datetime(2017, 10, 29, 2))
        val = croniter('0 * * * *', local_date).get_next(datetime)
        self.assertEqual(val, tz.localize(datetime(2017, 10, 29, 3)))
        local_date = tz.localize(datetime(2017, 10, 29, 3))
        val = croniter('0 * * * *', local_date).get_next(datetime)
        self.assertEqual(val, tz.localize(datetime(2017, 10, 29, 4)))
        local_date = tz.localize(datetime(2017, 10, 29, 4))
        val = croniter('0 * * * *', local_date).get_next(datetime)
        self.assertEqual(val, tz.localize(datetime(2017, 10, 29, 5)))
        local_date = tz.localize(datetime(2017, 10, 29, 5))
        val = croniter('0 * * * *', local_date).get_next(datetime)
        self.assertEqual(val, tz.localize(datetime(2017, 10, 29, 6)))

    def test_std_dst2(self):
        """
        DST tests

        This fixes https://github.com/taichino/croniter/issues/87

        São Paulo, Brazil: 18/02/2018 00:00 -> 17/02/2018 23:00

        """
        tz = pytz.timezone("America/Sao_Paulo")
        local_dates = [
            # 17-22: 00 -> 18-00:00
            (tz.localize(datetime(2018, 2, 17, 21, 0, 0)),
             '2018-02-18 00:00:00-03:00'),
            # 17-23: 00 -> 18-00:00
            (tz.localize(datetime(2018, 2, 17, 22, 0, 0)),
             '2018-02-18 00:00:00-03:00'),
            # 17-23: 00 -> 18-00:00
            (tz.localize(datetime(2018, 2, 17, 23, 0, 0)),
             '2018-02-18 00:00:00-03:00'),
            # 18-00: 00 -> 19-00:00
            (tz.localize(datetime(2018, 2, 18, 0, 0, 0)),
             '2018-02-19 00:00:00-03:00'),
            # 17-22: 00 -> 18-00:00
            (tz.localize(datetime(2018, 2, 17, 21, 5, 0)),
             '2018-02-18 00:00:00-03:00'),
            # 17-23: 00 -> 18-00:00
            (tz.localize(datetime(2018, 2, 17, 22, 5, 0)),
             '2018-02-18 00:00:00-03:00'),
            # 17-23: 00 -> 18-00:00
            (tz.localize(datetime(2018, 2, 17, 23, 5, 0)),
             '2018-02-18 00:00:00-03:00'),
            # 18-00: 00 -> 19-00:00
            (tz.localize(datetime(2018, 2, 18, 0, 5, 0)),
             '2018-02-19 00:00:00-03:00'),
        ]
        ret1 = [croniter("0 0 * * *", d[0]).get_next(datetime)
                for d in local_dates]
        sret1 = ['{0}'.format(d) for d in ret1]
        lret1 = ['{0}'.format(d[1]) for d in local_dates]
        self.assertEqual(sret1, lret1)

    def test_std_dst3(self):
        """
        DST tests

        This fixes https://github.com/taichino/croniter/issues/90

        Adelaide, Australia: 15/04/2020 00:00 -> 15/03/2020

        """

        tz = pytz.timezone('Australia/Adelaide')

        schedule = croniter('0 0 24 * *', tz.localize(datetime(2020, 4,15)))
        val1 = schedule.get_prev(datetime)
        dt1 = tz.localize(datetime(2020, 3, 24))
        self.assertEqual(val1, dt1)

        val2 = schedule.get_next(datetime)
        dt2 = tz.localize(datetime(2020, 4, 24))
        self.assertEqual(val2, dt2)

    def test_error_alpha_cron(self):
        self.assertRaises(CroniterNotAlphaError, croniter.expand,
                          '* * * janu-jun *')

    def test_error_bad_cron(self):
        self.assertRaises(CroniterBadCronError, croniter.expand,
                          '* * * *')
        self.assertRaises(CroniterBadCronError, croniter.expand,
                          '* * * * * * *')

    def test_is_valid(self):
        self.assertTrue(croniter.is_valid('0 * * * *'))
        self.assertFalse(croniter.is_valid('0 * *'))
        self.assertFalse(croniter.is_valid('* * * janu-jun *'))

    def test_exactly_the_same_minute(self):
        base = datetime(2018, 3, 5, 12, 30, 50)
        itr = croniter('30 7,12,17 * * *', base)
        n1 = itr.get_prev(datetime)
        self.assertEqual(12, n1.hour)

        n2 = itr.get_prev(datetime)
        self.assertEqual(7, n2.hour)

        n3 = itr.get_next(datetime)
        self.assertEqual(12, n3.hour)

    def test_next_when_now_satisfies_cron(self):
        ts_a = datetime(2018, 5, 21, 0, 3, 0)
        ts_b = datetime(2018, 5, 21, 0, 4, 20)
        test_cron = '4 * * * *'

        next_a = croniter(test_cron, start_time=ts_a).get_next()
        next_b = croniter(test_cron, start_time=ts_b).get_next()

        self.assertTrue(next_b > next_a)

    def test_milliseconds(self):
        """
        https://github.com/taichino/croniter/issues/107
        """

        _croniter = partial(croniter, "0 10 * * *", ret_type=datetime)

        dt = datetime(2018, 1, 2, 10, 0, 0, 500)
        self.assertEqual(
            _croniter(start_time=dt).get_prev(),
            datetime(2018, 1, 2, 10, 0),
        )
        self.assertEqual(
            _croniter(start_time=dt).get_next(),
            datetime(2018, 1, 3, 10, 0),
        )

        dt = datetime(2018, 1, 2, 10, 0, 1, 0)
        self.assertEqual(
            _croniter(start_time=dt).get_prev(),
            datetime(2018, 1, 2, 10, 0),
        )
        self.assertEqual(
            _croniter(start_time=dt).get_next(),
            datetime(2018, 1, 3, 10, 0),
        )

        dt = datetime(2018, 1, 2, 9, 59, 59, 999999)
        self.assertEqual(
            _croniter(start_time=dt).get_prev(),
            datetime(2018, 1, 1, 10, 0),
        )
        self.assertEqual(
            _croniter(start_time=dt).get_next(),
            datetime(2018, 1, 2, 10, 0),
        )

    def test_invalid_zerorepeat(self):
        self.assertFalse(croniter.is_valid('*/0 * * * *'))

    def test_weekday_range(self):
        ret = []
        # jan 14 is monday
        dt = datetime(2019, 1, 14, 0, 0, 0, 0)
        for i in range(10):
            c = croniter("0 0 * * 2-4 *", start_time=dt)
            dt = datetime.utcfromtimestamp(c.get_next())
            ret.append(dt)
            dt += timedelta(days=1)
        sret = ["{0}".format(r) for r in ret]
        self.assertEqual(
            sret,
            ['2019-01-15 00:00:00',
             '2019-01-16 00:00:01',
             '2019-01-17 00:00:02',
             '2019-01-22 00:00:00',
             '2019-01-23 00:00:01',
             '2019-01-24 00:00:02',
             '2019-01-29 00:00:00',
             '2019-01-30 00:00:01',
             '2019-01-31 00:00:02',
             '2019-02-05 00:00:00'])
        ret = []
        dt = datetime(2019, 1, 14, 0, 0, 0, 0)
        for i in range(10):
            c = croniter("0 0 * * 1-7 *", start_time=dt)
            dt = datetime.utcfromtimestamp(c.get_next())
            ret.append(dt)
            dt += timedelta(days=1)
        sret = ["{0}".format(r) for r in ret]
        self.assertEqual(
            sret,
            ['2019-01-14 00:00:01',
             '2019-01-15 00:00:02',
             '2019-01-16 00:00:03',
             '2019-01-17 00:00:04',
             '2019-01-18 00:00:05',
             '2019-01-19 00:00:06',
             '2019-01-20 00:00:07',
             '2019-01-21 00:00:08',
             '2019-01-22 00:00:09',
             '2019-01-23 00:00:10'])

    def test_issue_monsun_117(self):
        ret = []
        dt = datetime(2019, 1, 14, 0, 0, 0, 0)
        for i in range(10):
            # c = croniter("0 0 * * Mon-Sun *", start_time=dt)
            c = croniter("0 0 * * Wed-Sun *", start_time=dt)
            dt = datetime.utcfromtimestamp(c.get_next())
            ret.append(dt)
            dt += timedelta(days=1)
        sret = ["{0}".format(r) for r in ret]
        self.assertEqual(
            sret,
            ['2019-01-16 00:00:00',
             '2019-01-17 00:00:01',
             '2019-01-18 00:00:02',
             '2019-01-19 00:00:03',
             '2019-01-23 00:00:00',
             '2019-01-24 00:00:01',
             '2019-01-25 00:00:02',
             '2019-01-26 00:00:03',
             '2019-01-30 00:00:00',
             '2019-01-31 00:00:01'])

    def test_mixdow(self):
        base = datetime(2018, 10, 1, 0, 0)
        itr = croniter('1 1 7,14,21,L * *', base)
        self.assertTrue(isinstance(itr.get_next(), float))

    def test_match(self):
        self.assertTrue(croniter.match(
            "0 0 * * *",
            datetime(2019, 1, 14, 0, 0, 0, 0)
        ))
        self.assertFalse(croniter.match(
            "0 0 * * *",
            datetime(2019, 1, 14, 0, 1, 0, 0)
        ))
        self.assertTrue(croniter.match(
            "31 * * * *",
            datetime(2019, 1, 14, 1, 31, 0, 0)
        ))
        self.assertTrue(croniter.match(
            "0 0 10 * wed",
            datetime(2020, 6, 10, 0, 0, 0, 0),
            day_or=True
        ))
        self.assertTrue(croniter.match(
            "0 0 10 * fri",
            datetime(2020, 6, 10, 0, 0, 0, 0),
            day_or=True
        ))
        self.assertTrue(croniter.match(
            "0 0 10 * fri",
            datetime(2020, 6, 12, 0, 0, 0, 0),
            day_or=True
        ))
        self.assertTrue(croniter.match(
            "0 0 10 * wed",
            datetime(2020, 6, 10, 0, 0, 0, 0),
            day_or=False
        ))
        self.assertFalse(croniter.match(
            "0 0 10 * fri",
            datetime(2020, 6, 10, 0, 0, 0, 0),
            day_or=False
        ))
        self.assertFalse(croniter.match(
            "0 0 10 * fri",
            datetime(2020, 6, 12, 0, 0, 0, 0),
            day_or=False
        ))


    def test_dst_issue90_st31ny(self):
        tz = pytz.timezone("Europe/Paris")
        now = datetime(2020, 3, 29, 1, 59, 55, tzinfo=tz)
        it = croniter('1 2 * * *', now)
        #
        # Taking around DST @ 29/03/20 01:59
        #
        ret = [
            it.get_next(datetime).isoformat(),
            it.get_prev(datetime).isoformat(),
            it.get_prev(datetime).isoformat(),
            it.get_next(datetime).isoformat(),
            it.get_next(datetime).isoformat(),
        ]
        self.assertEqual(ret, [
            '2020-03-30T02:01:00+02:00',
            '2020-03-29T01:01:00+01:00',
            '2020-03-28T03:01:00+01:00',
            '2020-03-29T02:01:00+02:00',
            '2020-03-29T03:01:00+02:00'])
        #
        nowp = datetime(2020, 3, 28, 1, 58, 55, tzinfo=tz)
        itp = croniter('1 2 * * *', nowp)
        retp = [
            itp.get_next(datetime).isoformat(),
            itp.get_prev(datetime).isoformat(),
            itp.get_prev(datetime).isoformat(),
            itp.get_next(datetime).isoformat(),
            itp.get_next(datetime).isoformat(),
        ]
        self.assertEqual(retp, [
            '2020-03-29T02:01:00+02:00',
            '2020-03-28T02:01:00+01:00',
            '2020-03-27T02:01:00+01:00',
            '2020-03-28T02:01:00+01:00',
            '2020-03-29T03:01:00+02:00'])
        #
        nowt = datetime(2020, 3, 29, 2, 0, 0, tzinfo=tz)
        itt = croniter('1 2 * * *', nowt)
        rett = [
            itt.get_next(datetime).isoformat(),
            itt.get_prev(datetime).isoformat(),
            itt.get_prev(datetime).isoformat(),
            itt.get_next(datetime).isoformat(),
            itt.get_next(datetime).isoformat(),
        ]
        self.assertEqual(rett, [
            '2020-03-30T02:01:00+02:00',
            '2020-03-29T01:01:00+01:00',
            '2020-03-28T03:01:00+01:00',
            '2020-03-29T02:01:00+02:00',
            '2020-03-29T03:01:00+02:00'])


    def test_nth_wday_simple(self):
        f = lambda y,m,w: croniter._get_nth_weekday_of_month(y,m,w)
        sun, mon, tue, wed, thu, fri, sat = range(7)

        self.assertEqual(f(2000, 1, mon), (3, 10, 17, 24, 31))
        self.assertEqual(f(2000, 2, tue), (1, 8, 15, 22, 29)) # Leap year
        self.assertEqual(f(2000, 3, wed), (1, 8, 15, 22, 29))
        self.assertEqual(f(2000, 4, thu), (6, 13, 20, 27))
        self.assertEqual(f(2000, 2, fri), (4, 11, 18, 25))
        self.assertEqual(f(2000, 2, sat), (5, 12, 19, 26))

    def test_nth_as_last_wday_simple(self):
        f = lambda y,m,w: croniter._get_nth_weekday_of_month(y,m,w)[-1]
        sun, mon, tue, wed, thu, fri, sat = range(7)
        self.assertEqual(f(2000, 2, tue), 29)
        self.assertEqual(f(2000, 2, sun), 27)
        self.assertEqual(f(2000, 2, mon), 28)
        self.assertEqual(f(2000, 2, wed), 23)
        self.assertEqual(f(2000, 2, thu), 24)
        self.assertEqual(f(2000, 2, fri), 25)
        self.assertEqual(f(2000, 2, sat), 26)

    def test_wdom_core_leap_year(self):
        f = lambda y,m,w: croniter._get_nth_weekday_of_month(y,m,w)[-1]
        sun, mon, tue, wed, thu, fri, sat = range(7)
        self.assertEqual(f(2000, 2, tue), 29)
        self.assertEqual(f(2000, 2, sun), 27)
        self.assertEqual(f(2000, 2, mon), 28)
        self.assertEqual(f(2000, 2, wed), 23)
        self.assertEqual(f(2000, 2, thu), 24)
        self.assertEqual(f(2000, 2, fri), 25)
        self.assertEqual(f(2000, 2, sat), 26)

    def test_lwom_friday(self):
        it = croniter("0 0 * * L5", datetime(1987, 1, 15), ret_type=datetime)
        items = [next(it) for i in range(12)]
        self.assertListEqual(items, [
            datetime(1987, 1, 30),
            datetime(1987, 2, 27),
            datetime(1987, 3, 27),
            datetime(1987, 4, 24),
            datetime(1987, 5, 29),
            datetime(1987, 6, 26),
            datetime(1987, 7, 31),
            datetime(1987, 8, 28),
            datetime(1987, 9, 25),
            datetime(1987, 10, 30),
            datetime(1987, 11, 27),
            datetime(1987, 12, 25),
        ])

    def test_lwom_friday_2hours(self):
        # This works with +/- 'days=1' in proc_day_of_week_last() and I don't know WHY?!?
        it = croniter("0 1,5 * * L5", datetime(1987, 1, 15), ret_type=datetime)
        items = [next(it) for i in range(12)]
        self.assertListEqual(items, [
            datetime(1987, 1, 30, 1),
            datetime(1987, 1, 30, 5),
            datetime(1987, 2, 27, 1),
            datetime(1987, 2, 27, 5),
            datetime(1987, 3, 27, 1),
            datetime(1987, 3, 27, 5),
            datetime(1987, 4, 24, 1),
            datetime(1987, 4, 24, 5),
            datetime(1987, 5, 29, 1),
            datetime(1987, 5, 29, 5),
            datetime(1987, 6, 26, 1),
            datetime(1987, 6, 26, 5),
        ])

    def test_lwom_friday_2xh_2xm(self):
        it = croniter("0,30 1,5 * * L5", datetime(1987, 1, 15), ret_type=datetime)
        items = [next(it) for i in range(12)]
        self.assertListEqual(items, [
            datetime(1987, 1, 30, 1, 0),
            datetime(1987, 1, 30, 1, 30),
            datetime(1987, 1, 30, 5, 0),
            datetime(1987, 1, 30, 5, 30),
            datetime(1987, 2, 27, 1, 0),
            datetime(1987, 2, 27, 1, 30),
            datetime(1987, 2, 27, 5, 0),
            datetime(1987, 2, 27, 5, 30),
            datetime(1987, 3, 27, 1, 0),
            datetime(1987, 3, 27, 1, 30),
            datetime(1987, 3, 27, 5, 0),
            datetime(1987, 3, 27, 5, 30),
        ])

    def test_lwom_saturday_rev(self):
        it = croniter("0 0 * * L6", datetime(2017, 12, 31), ret_type=datetime, is_prev=True)
        items = [next(it) for i in range(12)]
        self.assertListEqual(items, [
            datetime(2017, 12, 30),
            datetime(2017, 11, 25),
            datetime(2017, 10, 28),
            datetime(2017, 9, 30),
            datetime(2017, 8, 26),
            datetime(2017, 7, 29),
            datetime(2017, 6, 24),
            datetime(2017, 5, 27),
            datetime(2017, 4, 29),
            datetime(2017, 3, 25),
            datetime(2017, 2, 25),
            datetime(2017, 1, 28),
        ])

    def test_lwom_tue_thu(self):
        it = croniter("0 0 * * L2,L4", datetime(2016, 6, 1), ret_type=datetime)
        items = [next(it) for i in range(10)]
        self.assertListEqual(items, [
            datetime(2016, 6, 28),
            datetime(2016, 6, 30),
            datetime(2016, 7, 26),
            datetime(2016, 7, 28),
            datetime(2016, 8, 25),  # last tuesday comes before the last thursday
            datetime(2016, 8, 30),
            datetime(2016, 9, 27),
            datetime(2016, 9, 29),
            datetime(2016, 10, 25),
            datetime(2016, 10, 27),
        ])

    def test_hash_mixup_all_fri_3rd_sat(self):
        # It appears that it's not possible to MIX a literal dow with a `dow#n` format
        cron_a = "0 0 * * 6#3"
        cron_b = "0 0 * * 5"
        cron_c = "0 0 * * 5,6#3"
        start = datetime(2021, 3, 1)
        expect_a = [ datetime(2021, 3, 20) ]
        expect_b = [
            datetime(2021, 3, 5),
            datetime(2021, 3, 12),
            datetime(2021, 3, 19),
            datetime(2021, 3, 26),
        ]
        expect_c = sorted(set(expect_a) & set(expect_b))
        def getn(expr, n):
            it = croniter(expr, start, ret_type=datetime)
            return [next(it) for i in range(n)]
        self.assertListEqual(getn(cron_a, 1), expect_a)
        self.assertListEqual(getn(cron_b, 4), expect_b)
        with self.assertRaises(CroniterUnsupportedSyntaxError):
            self.assertListEqual(getn(cron_c, 5), expect_c)

    def test_lwom_mixup_all_fri_last_sat(self):
        # Based on the failure of test_hash_mixup_all_fri_3rd_sat, we should expect this to fail too as this implementation simply extends nth_weekday_of_month
        cron_a = "0 0 * * L6"
        cron_b = "0 0 * * 5"
        cron_c = "0 0 * * 5,L6"
        start = datetime(2021, 3, 1)
        expect_a = [ datetime(2021, 3, 27) ]
        expect_b = [
            datetime(2021, 3, 5),
            datetime(2021, 3, 12),
            datetime(2021, 3, 19),
            datetime(2021, 3, 26),
        ]
        expect_c = sorted(set(expect_a) | set(expect_b))
        def getn(expr, n):
            it = croniter(expr, start, ret_type=datetime)
            return [next(it) for i in range(n)]
        self.assertListEqual(getn(cron_a, 1), expect_a)
        self.assertListEqual(getn(cron_b, 4), expect_b)
        with self.assertRaises(CroniterUnsupportedSyntaxError):
            self.assertListEqual(getn(cron_c, 5), expect_c)

    def test_lwom_mixup_firstlast_sat(self):
        # First saturday, last saturday
        start = datetime(2021, 3, 1)
        cron_a = "0 0 * * 6#1"
        cron_b = "0 0 * * L6"
        cron_c = "0 0 * * L6,6#1"
        expect_a = [
            datetime(2021, 3, 6),
            datetime(2021, 4, 3),
            datetime(2021, 5, 1),
        ]
        expect_b = [
            datetime(2021, 3, 27),
            datetime(2021, 4, 24),
            datetime(2021, 5, 29),
        ]
        expect_c = sorted(expect_a + expect_b)
        def getn(expr, n):
            it = croniter(expr, start, ret_type=datetime)
            return [next(it) for i in range(n)]
        self.assertListEqual(getn(cron_a, 3), expect_a)
        self.assertListEqual(getn(cron_b, 3), expect_b)
        self.assertListEqual(getn(cron_c, 6), expect_c)

    def test_lwom_mixup_4th_and_last(self):
        # 4th and last monday
        start = datetime(2021, 11, 1)
        cron_a = "0 0 * * 1#4"
        cron_b = "0 0 * * L1"
        cron_c = "0 0 * * 1#4,L1"
        expect_a = [
            datetime(2021, 11, 22),
            datetime(2021, 12, 27),
            datetime(2022, 1, 24)
        ]
        expect_b = [
            datetime(2021, 11, 29),
            datetime(2021, 12, 27),
            datetime(2022, 1, 31),
        ]
        expect_c = sorted(set(expect_a) | set(expect_b))

        def getn(expr, n):
            it = croniter(expr, start, ret_type=datetime)
            return [next(it) for i in range(n)]

        self.assertListEqual(getn(cron_a, 3), expect_a)
        self.assertListEqual(getn(cron_b, 3), expect_b)
        self.assertListEqual(getn(cron_c, 5), expect_c)

    def test_nth_out_of_range(self):
        with self.assertRaises(CroniterBadCronError):
            croniter("0 0 * * 1#7")
        with self.assertRaises(CroniterBadCronError):
            croniter("0 0 * * 1#0")

    def test_last_out_of_range(self):
        with self.assertRaises(CroniterBadCronError):
            croniter("0 0 * * L-1")
        with self.assertRaises(CroniterBadCronError):
            croniter("0 0 * * L8")

    def test_issue_47(self):
        base = datetime(2021, 3, 30, 4, 0)
        itr = croniter('0 6 30 3 *', base)
        prev1 = itr.get_prev(datetime)
        self.assertEqual(prev1.year, base.year-1)
        self.assertEqual(prev1.month, 3)
        self.assertEqual(prev1.day, 30)
        self.assertEqual(prev1.hour, 6)
        self.assertEqual(prev1.minute, 0)

    maxDiff = None
    def test_issue_142_dow(self):
        ret = []
        for i in range(1, 31):
            ret.append((i,
                croniter('35 * 1-l/8 * *', datetime(2020, 1, i),
                         ret_type=datetime).get_next())
            )
            i += 1
        self.assertEqual(
            ret,
            [(1, datetime(2020, 1, 1, 0, 35)),
             (2, datetime(2020, 1, 9, 0, 35)),
             (3, datetime(2020, 1, 9, 0, 35)),
             (4, datetime(2020, 1, 9, 0, 35)),
             (5, datetime(2020, 1, 9, 0, 35)),
             (6, datetime(2020, 1, 9, 0, 35)),
             (7, datetime(2020, 1, 9, 0, 35)),
             (8, datetime(2020, 1, 9, 0, 35)),
             (9, datetime(2020, 1, 9, 0, 35)),
             (10, datetime(2020, 1, 17, 0, 35)),
             (11, datetime(2020, 1, 17, 0, 35)),
             (12, datetime(2020, 1, 17, 0, 35)),
             (13, datetime(2020, 1, 17, 0, 35)),
             (14, datetime(2020, 1, 17, 0, 35)),
             (15, datetime(2020, 1, 17, 0, 35)),
             (16, datetime(2020, 1, 17, 0, 35)),
             (17, datetime(2020, 1, 17, 0, 35)),
             (18, datetime(2020, 1, 25, 0, 35)),
             (19, datetime(2020, 1, 25, 0, 35)),
             (20, datetime(2020, 1, 25, 0, 35)),
             (21, datetime(2020, 1, 25, 0, 35)),
             (22, datetime(2020, 1, 25, 0, 35)),
             (23, datetime(2020, 1, 25, 0, 35)),
             (24, datetime(2020, 1, 25, 0, 35)),
             (25, datetime(2020, 1, 25, 0, 35)),
             (26, datetime(2020, 2, 1, 0, 35)),
             (27, datetime(2020, 2, 1, 0, 35)),
             (28, datetime(2020, 2, 1, 0, 35)),
             (29, datetime(2020, 2, 1, 0, 35)),
             (30, datetime(2020, 2, 1, 0, 35))])

    def test_issue145_getnext(self):
        # Example of quarterly event cron schedule
        start = datetime(2020, 9, 24)
        cron = "0 13 8 1,4,7,10 wed"
        with self.assertRaises(CroniterBadDateError):
            it = croniter(cron, start, day_or=False, max_years_between_matches=1)
            it.get_next()
        # New functionality (0.3.35) allowing croniter to find spare matches of cron patterns across multiple years
        it = croniter(cron, start, day_or=False, max_years_between_matches=5)
        self.assertEqual(it.get_next(datetime), datetime(2025, 1, 8, 13))

    def test_explicit_year_forward(self):
        start = datetime(2020, 9, 24)
        cron = "0 13 8 1,4,7,10 wed"

        # Expect exception because no explicit range was provided.  Therefore, the caller should be made aware that an implicit limit was hit.
        ccron = croniter(cron, start, day_or=False)
        ccron._max_years_between_matches = 1
        iterable = ccron.all_next()
        with self.assertRaises(CroniterBadDateError):
            next(iterable)

        iterable = croniter(cron, start, day_or=False, max_years_between_matches=5).all_next(datetime)
        n = next(iterable)
        self.assertEqual(n, datetime(2025, 1, 8, 13))

        # If the explicitly given lookahead isn't enough to reach the next date, that's fine.  The caller specified the maximum gap, so no just stop iteration
        iterable = croniter(cron, start, day_or=False, max_years_between_matches=2).all_next(datetime)
        with self.assertRaises(StopIteration):
            next(iterable)

    def test_issue151(self):
        """."""
        self.assertTrue(
            croniter.match("* * * * *", datetime(2019, 1, 14, 11, 0, 59, 999999)))

    def test_overflow(self):
        """."""
        self.assertRaises(CroniterBadCronError, croniter , "0-10000000 * * * *", datetime.now())

    def test_issue156(self):
        """."""
        dt = croniter("* * * * *,0", datetime(2019, 1, 14, 11, 0, 59, 999999)).get_next()
        self.assertEqual(1547463660.0, dt)
        self.assertRaises(CroniterBadCronError, croniter, "* * * * *,b")
        dt = croniter("0 0 * * *,sat#3", datetime(2019, 1, 14, 11, 0, 59, 999999)).get_next()
        self.assertEqual(1547856000.0, dt)

    def test_confirm_sort(self):
        m, h, d, mon, dow, s = range(6)
        self.assertListEqual(croniter('0 8,22,10,23 1 1 0').expanded[h], [8, 10, 22, 23])
        self.assertListEqual(croniter('0 0 25-L 1 0').expanded[d], [25, 26, 27, 28, 29, 30, 31])
        self.assertListEqual(croniter("1 1 7,14,21,L * *").expanded[d], [7, 14, 21, "l"])
        self.assertListEqual(croniter("0 0 * * *,sat#3").expanded[dow], ["*", 6])

    def test_issue_k6(self):
        self.assertRaises(CroniterBadCronError, croniter, '0 0 0 0 0')
        self.assertRaises(CroniterBadCronError, croniter, '0 0 0 1 0')

    def test_issue_k11(self):
        now = pytz.timezone('America/New_York').localize(datetime(2019, 1, 14, 11, 0, 59))
        nextnow = croniter('* * * * * ').next(datetime, start_time=now)
        nextnow2 = croniter('* * * * * ', now).next(datetime)
        for nt in nextnow, nextnow2:
            self.assertEqual(nt.tzinfo.zone, 'America/New_York')
            self.assertEqual(int(croniter._datetime_to_timestamp(nt)), 1547481660)


if __name__ == '__main__':
    unittest.main()
