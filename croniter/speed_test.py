#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import datetime, date
from croniter import croniter

class timerTest(object):
    def __init__(self):
        self.tests = tuple(getattr(self, m) for m in dir(self) if m.lower().startswith('test'))

    def run(self):
        for test in self.tests:
            test()
                

class CroniterTest(timerTest):
    def testMinute(self):
        # minute asterisk
        base = datetime(2010, 1, 23, 12, 18)
        itr = croniter('*/1 * * * *', base)
        n1 = itr.get_next(datetime)    # 19
        base.year == n1.year
        base.month == n1.month
        base.day == n1.day
        base.hour == n1.hour
        base.minute == n1.minute - 1
        for i in range(39): # ~ 58
            itr.get_next()

        n2 = itr.get_next(datetime)
        n2.minute == 59

        n3 = itr.get_next(datetime)

        n3.minute == 0
        n3.hour == 13

        itr = croniter('*/5 * * * *', base)
        n4 = itr.get_next(datetime)
        n4.minute == 20
        for i in range(6):
            itr.get_next()
        n5 = itr.get_next(datetime)
        n5.minute == 55

        n6 = itr.get_next(datetime)
        n6.minute == 0
        n6.hour == 13

    def testHour(self):
        base = datetime(2010, 1, 24, 12, 2)
        itr = croniter('0 */3 * * *', base)
        n1 = itr.get_next(datetime)

        n1.hour == 15
        n1.minute == 0

        for i in range(2):
            itr.get_next()

        n2 = itr.get_next(datetime)
        n2.hour == 0
        n2.day == 25

    def testDay(self):
        base = datetime(2010, 2, 24, 12, 9)
        itr = croniter('0 0 */3 * *', base)
        n1 = itr.get_next(datetime)
        n1.day == 27
        n2 = itr.get_next(datetime)
        n2.day == 3

        # test leap year
        base = datetime(1996, 2, 27)
        itr = croniter('0 0 * * *', base)
        n1 = itr.get_next(datetime)
        n1.day == 28
        n1.month == 2
        n2 = itr.get_next(datetime)
        n2.day == 29
        n2.month == 2

        base2 = datetime(2000, 2, 27)
        itr2 = croniter('0 0 * * *', base2)
        n3 = itr2.get_next(datetime)
        n3.day == 28
        n3.month == 2
        n4 = itr2.get_next(datetime)
        n4.day == 29
        n4.month == 2

    def testWeekDay(self):
        base = datetime(2010, 2, 25)
        itr = croniter('0 0 * * sat', base)
        n1 = itr.get_next(datetime)
        n1.isoweekday() == 6
        n1.day == 27

        n2 = itr.get_next(datetime)
        n2.isoweekday() == 6
        n2.day == 6
        n2.month == 3

        base = datetime(2010, 1, 25)
        itr = croniter('0 0 1 * wed', base)
        n1 = itr.get_next(datetime)
        n1.month == 1
        n1.day == 27
        n1.year == 2010

        n2 = itr.get_next(datetime)
        n2.month == 2
        n2.day == 1
        n2.year == 2010

        n3 = itr.get_next(datetime)
        n3.month == 2
        n3.day == 3
        n3.year == 2010

    def testMonth(self):
        base = datetime(2010, 1, 25)
        itr = croniter('0 0 1 * *', base)
        n1 = itr.get_next(datetime)

        n1.month == 2
        n1.day == 1

        n2 = itr.get_next(datetime)
        n2.month == 3
        n2.day == 1

        for i in range(8):
            itr.get_next()

        n3 = itr.get_next(datetime)
        n3.month == 12
        n3.year == 2010

        n4 = itr.get_next(datetime)
        n4.month == 1
        n4.year == 2011


    def testPrevMinute(self):
        base = datetime(2010, 8, 25, 15, 56)
        itr = croniter('*/1 * * * *', base)
        prev = itr.get_prev(datetime)
        base.year == prev.year
        base.month == prev.month
        base.day == prev.day
        base.hour == prev.hour
        base.minute, prev.minute+1

        base = datetime(2010, 8, 25, 15, 0)
        itr = croniter('*/1 * * * *', base)
        prev = itr.get_prev(datetime)
        base.year == prev.year
        base.month == prev.month
        base.day == prev.day
        base.hour == prev.hour+1
        59 == prev.minute

        base = datetime(2010, 8, 25, 0, 0)
        itr = croniter('*/1 * * * *', base)
        prev = itr.get_prev(datetime)
        base.year == prev.year
        base.month == prev.month
        base.day == prev.day+1
        23 == prev.hour
        59 == prev.minute

    def testPrevWeekDay(self):
        base = datetime(2010, 8, 25, 15, 56)
        itr = croniter('0 0 * * sat,sun', base)
        prev1 = itr.get_prev(datetime)
        prev1.year == base.year
        prev1.month == base.month
        prev1.day == 22
        prev1.hour == 0
        prev1.minute == 0

        prev2 = itr.get_prev(datetime)
        prev2.year == base.year
        prev2.month == base.month
        prev2.day == 21
        prev2.hour == 0
        prev2.minute == 0

        prev3 = itr.get_prev(datetime)
        prev3.year == base.year
        prev3.month == base.month
        prev3.day == 15
        prev3.hour == 0
        prev3.minute == 0

    def testISOWeekday(self):
        base = datetime(2010, 2, 25)
        itr = croniter('0 0 * * 7', base)
        n1 = itr.get_next(datetime)
        n1.isoweekday() ==  7
        n1.day == 28

        n2 = itr.get_next(datetime)
        n2.isoweekday() == 7
        n2.day == 7
        n2.month == 3        
        
if __name__ == '__main__':
    from timeit import Timer
    t = Timer('c=CroniterTest();c.run()', 'from __main__ import CroniterTest')
    print t.timeit(200)
