#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime, date
from dateutil.relativedelta import *

class croniter:
  RANGES = (
    (0, 59),
    (0, 23),
    (1, 31),
    (1, 12),
    (0,  6),
    (0, 59)
  )
  DAYS = (
    31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
  )

  ALPHACONV = (
    { },
    { },
    { },
    { 'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5,  'jun':6,
      'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12 },
    { 'sun':0, 'mon':1, 'tue':2, 'wed':3, 'thu':4, 'fri':5, 'sat':6 },
    {  }
  )

  LOWMAP = ( 
    {},
    {},
    {0: 1},
    {0: 1},
    {7: 0},
    {},
  )
  
  def __init__(self, expr_format, start_time=time.time()):
    if isinstance(start_time, datetime):
      start_time = time.mktime(start_time.timetuple())
    self.cur   = start_time
    self.exprs = expr_format.split()
    if len(self.exprs) != 5 and len(self.exprs) != 6:
      raise ValueError("Exactly 5 or 6 columns has to be specified for iterator expression")
    expanded = []
    for i, expr in enumerate(self.exprs):
      e_list = expr.split(',')
      res = []
      while len(e_list) > 0:
        e = e_list.pop()
        t = re.sub(r'^\*(/.+)$', r'%d-%d\1' % (self.RANGES[i][0], self.RANGES[i][1]), str(e))
        m = re.search(r'^([^-]+)-([^-/]+)(/(.*))?$', t)
        if m:
          (low, high, step) = m.group(1), m.group(2), m.group(4) or 1
          if not re.search(r'^\d+', low):
            low = self.ALPHACONV[i][low.lower()]
          if not re.search(r'^\d+', high):
            high = self.ALPHACONV[i][high.lower()]
          if not low or not high or low > high or not re.search(r'^\d+$', str(step)):
            raise ValueError("[%s] is not acceptable" % expr_format)
          for j in range(int(low), int(high)+1):
            if j % int(step) == 0:
              e_list.append(j)
        else:
          if not re.search(r'^(\d+|\*)$', t):
            t = self.ALPHACONV[i][t.lower()]
          if t in self.LOWMAP[i]:
            t = self.LOWMAP[i][t]
          if t != '*' and (int(t) < self.RANGES[i][0] or int(t) > self.RANGES[i][1]):
            raise ValueError("[%s] is not acceptable, out of range" % expr_format)
          try:
            res.append(int(t))
          except:
            res.append(t)
      res.sort()
      expanded.append(['*'] if (len(res) == 1 and res[0] == '*') else res)
    self.expanded = expanded

  def get_next(self, ret_type=float):
    expanded = self.expanded[:]
    if ret_type not in [float, datetime]:
      raise TypeError("invalid ret_type, only 'float' or 'datetime' is acceptable")
    if expanded[2][0] != '*' and expanded[4][0] != '*':
      bak = expanded[4]
      expanded[4] = ['*']
      t1 = self._calc_time(self.cur, expanded)
      expanded[4] = bak
      expanded[2] = ['*']
      t2 = self._calc_time(self.cur, expanded)
      result = t1 if t1 < t2 else t2
    else:
      result = self._calc_time(self.cur, expanded)
    self.cur = result
    if ret_type == datetime:
      result = datetime.fromtimestamp(result)
    return result

  def _calc_time(self, now, expanded):
    offset = len(expanded) == 6 and 1 or 60
    dst = now = datetime.fromtimestamp(now + offset)
    while dst.year <= now.year + 1:
      # check month
      if expanded[3][0] != '*':
        diff_month = self._get_nearest_diff(dst.month, expanded[3], 12)
        if diff_month > 0:
          dst += relativedelta(months=diff_month, day=1, hour=0, minute=0, second=0)
          continue
      # check day of month
      if expanded[2][0] != '*':
        days = self.DAYS[dst.month - 1]
        if dst.month == 2 and self.is_leap(dst.year) == True:
          days += 1
        diff_day = self._get_nearest_diff(dst.day, expanded[2], days)
        if diff_day > 0:
          dst += relativedelta(days=diff_day, hour=0, minute=0, second=0)
          continue
      # check day of week
      if expanded[4][0] != '*':
        dst_day_of_week = self._get_nearest(dst.weekday(), expanded[4]) or expanded[4][0]
        if dst_day_of_week != dst.weekday():
          dst += relativedelta(weekday=dst_day_of_week, hour=0, minute=0, second=0)
          continue
      # check hour
      if expanded[1][0] != '*':
        diff_hour = self._get_nearest_diff(dst.hour, expanded[1], 24)
        if diff_hour > 0:
          dst += relativedelta(hours = diff_hour, minute=0, second=0)
          continue
      # check minute
      if expanded[0][0] != '*':
        diff_min = self._get_nearest_diff(dst.minute, expanded[0], 60)
        if diff_min > 0:
          dst += relativedelta(minutes = diff_min, second=0)
          continue
      # check second
      if len(expanded) == 6:
        if expanded[5][0] != '*':
          diff_sec = self._get_nearest_diff(dst.second, expanded[5], 60)
          if diff_sec > 0:
            dst += relativedelta(seconds = diff_sec)            
            continue
      return time.mktime(dst.timetuple())
    raise "failed to find next date"
        
  def _get_nearest(self, x, to_check):
    for i, d in enumerate(to_check):
      if d >= x:
        return d
    return None

  def _get_nearest_diff(self, x, to_check, range_val):
    for i, d in enumerate(to_check):
      if d >= x:
        return d - x
    return to_check[0] - x + range_val

  def is_leap(self, year):
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
      return True
    else:
      return False

if __name__ == '__main__':
  base = datetime(2010, 1, 25)
  itr = croniter('0 0 * * sun,mon', base)
  print itr.get_next(datetime)
  print itr.get_next(datetime)
  
  base = datetime(2010, 1, 25)
  itr = croniter('0 0 1 * 3', base)
  n1 = itr.get_next(datetime)
  n2 = itr.get_next(datetime)
  print n1
  print n2
  print "#" * 10
  
  base = datetime(2010, 1, 25)
  itr = croniter('0 0 1 * 3', base)
  n1 = itr.get_next(datetime)
  n2 = itr.get_next(datetime)
  
  base = datetime(2010, 2, 24, 12, 9)
  itr = croniter('0 0 */3 * *', base)
  n1 = itr.get_next(datetime)
  n2 = itr.get_next(datetime)
  print n1
  print n2
  base = datetime(1997, 2, 27)
  itr = croniter('0 0 * * *', base)
  n1 = itr.get_next(datetime)
  n2 = itr.get_next(datetime)
  print n1
  print n2
  base2 = datetime(2000, 2, 27)
  itr2 = croniter('0 0 * * *', base2)
  n3 = itr2.get_next(datetime)
  print n3
  n4 = itr2.get_next(datetime)
  print n4

