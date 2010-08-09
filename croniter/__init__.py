# -*- coding: utf-8 -*-

"""
    Simple example of usage is followings

    >>> from croniter import croniter
    >>> from datetime import datetime
    >>> base = datetime(2010, 1, 25, 4, 46)
    >>> iter = croniter('*/5 * * * *', base)  # every 5 minites
    >>> print iter.get_next(datetime)   # 2010-01-25 04:50:00
    >>> print iter.get_next(datetime)   # 2010-01-25 04:55:00
    >>> print iter.get_next(datetime)   # 2010-01-25 05:00:00
    >>>
    >>> iter = croniter('2 4 * * mon,fri', base)  # 04:02 on every Monday and Friday
    >>> print iter.get_next(datetime)   # 2010-01-26 04:02:00
    >>> print iter.get_next(datetime)   # 2010-01-30 04:02:00
    >>> print iter.get_next(datetime)   # 2010-02-02 04:02:00

    All you need to know is constructor and get_next, these signature are following.

    >>> def __init__(self, cron_format, start_time=time.time())
    
    croniter iterate along with 'cron_format' from 'start_time'.
    cron_format is 'min hour day month day_of_week', and please refer to
    http://en.wikipedia.org/wiki/Cron for details.

    >>> def get_next(self, ret_type=float)
    
    get_next return next time in iteration with 'ret_type'.
    And ret_type accept only 'float' or 'datetime'.
    
"""

__author__  = "Matsumoto Taichi"
__version__ = "0.1.6"
__license__ = "MIT License"

from croniter import croniter
