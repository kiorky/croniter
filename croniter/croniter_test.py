#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import time
from datetime import datetime, date
from croniter import croniter

class CroniterTest(unittest.TestCase):
  def testMinute(self):
    # minute asterisk
    base = datetime(2010, 1, 23, 12, 18)
    itr = croniter('*/1 * * * *', base)
    n1 = itr.get_next(datetime)  # 19
    self.assertEqual(base.year,   n1.year)
    self.assertEqual(base.month,  n1.month)
    self.assertEqual(base.day,    n1.day)
    self.assertEqual(base.hour,   n1.hour)
    self.assertEqual(base.minute, n1.minute - 1)
    for i in range(39): # ~ 58
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
    self.assertEqual(n1.day, 27)
    n2 = itr.get_next(datetime)
    self.assertEqual(n2.day, 3)

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

  def testError(self):
    base = datetime(2010, 1, 25)
    itr = croniter('* * * * *')
    self.assertRaises(TypeError, itr.get_next, str)
    self.assertRaises(ValueError, croniter, '* * * *')
    self.assertRaises(ValueError, croniter, '* * 5-1 * *')
    self.assertRaises(KeyError, croniter, '* * * janu-jun *')

  def testPrevMinute(self):
    base = datetime(2010, 8, 25, 15, 56)
    itr = croniter('*/1 * * * *', base)
    prev = itr.get_prev(datetime)
    self.assertEqual(base.year,   prev.year)
    self.assertEqual(base.month,  prev.month)
    self.assertEqual(base.day,    prev.day)
    self.assertEqual(base.hour,   prev.hour)
    self.assertEqual(base.minute, prev.minute+1)

    base = datetime(2010, 8, 25, 15, 0)
    itr = croniter('*/1 * * * *', base)
    prev = itr.get_prev(datetime)
    self.assertEqual(base.year,   prev.year)
    self.assertEqual(base.month,  prev.month)
    self.assertEqual(base.day,    prev.day)
    self.assertEqual(base.hour,   prev.hour+1)
    self.assertEqual(59, prev.minute)

    base = datetime(2010, 8, 25, 0, 0)
    itr = croniter('*/1 * * * *', base)
    prev = itr.get_prev(datetime)
    self.assertEqual(base.year,   prev.year)
    self.assertEqual(base.month,  prev.month)
    self.assertEqual(base.day,    prev.day+1)
    self.assertEqual(23, prev.hour)
    self.assertEqual(59, prev.minute)

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

  def testPrevWeekDay(self):
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
    self.assertEqual(n1.day, 22)
    self.assertEqual(n1.hour, 0)
    self.assertEqual(n1.minute, 5)
    
    
if __name__ == '__main__':
  unittest.main()
