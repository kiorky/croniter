Introduction
============

.. contents::


croniter provides iteration for the datetime object with a cron like format.

::

                          _ _
      ___ _ __ ___  _ __ (_) |_ ___ _ __
     / __| '__/ _ \| '_ \| | __/ _ \ '__|
    | (__| | | (_) | | | | | ||  __/ |
     \___|_|  \___/|_| |_|_|\__\___|_|


Website: https://github.com/kiorky/croniter

Travis badge
=============
.. image:: https://travis-ci.org/kiorky/croniter.png
    :target: http://travis-ci.org/kiorky/croniter

Usage
============

A simple example::

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

All you need to know is how to use the constructor and the get_next 
method, the signature of these methods are listed below::

    >>> def __init__(self, cron_format, start_time=time.time())

croniter iterates along with 'cron_format' from 'start_time'.
cron_format is 'min hour day month day_of_week', you can refer to
http://en.wikipedia.org/wiki/Cron for more details.::

    >>> def get_next(self, ret_type=float)

get_next calculates the next value according to the cron expression and
returns an object of type 'ret_type'. ret_type should be a 'float' or a 
'datetime' object.

Supported added for get_prev method. (>= 0.2.0)::

    >>> base = datetime(2010, 8, 25)
    >>> itr = croniter('0 0 1 * *', base)
    >>> print itr.get_prev(datetime)  # 2010-08-01 00:00:00
    >>> print itr.get_prev(datetime)  # 2010-07-01 00:00:00
    >>> print itr.get_prev(datetime)  # 2010-06-01 00:00:00


Develop this package
====================

::

    git clone https://github.com/kiorky/croniter.git
    cd croniter
    python bootstrap.py -d
    bin/buildout -vvvvvvN
    bin/test


Make a new release
====================
We use zest.fullreleaser, a great release infrastructure.

Do and follow these instructions
::

    bin/fullrelease


Contributors
===============
Thanks to all who have contributed to this project!
If you have contributed and your name is not listed below please let me know.

    - mrmachine
    - Hinnack
    - shazow
    - kiorky
    - jlsandell
    - mag009
    - djmitche
    - GreatCombinator
    - chris-baynes
    - ipartola
    - yuzawa-san

