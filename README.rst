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
    >>> iter = croniter('*/5 * * * *', base)  # every 5 minutes
    >>> print(iter.get_next(datetime))   # 2010-01-25 04:50:00
    >>> print(iter.get_next(datetime))   # 2010-01-25 04:55:00
    >>> print(iter.get_next(datetime))   # 2010-01-25 05:00:00
    >>>
    >>> iter = croniter('2 4 * * mon,fri', base)  # 04:02 on every Monday and Friday
    >>> print(iter.get_next(datetime))   # 2010-01-26 04:02:00
    >>> print(iter.get_next(datetime))   # 2010-01-30 04:02:00
    >>> print(iter.get_next(datetime))   # 2010-02-02 04:02:00
    >>>
    >>> iter = croniter('2 4 1 * wed', base)  # 04:02 on every Wednesday OR on 1st day of month
    >>> print(iter.get_next(datetime))   # 2010-01-27 04:02:00
    >>> print(iter.get_next(datetime))   # 2010-02-01 04:02:00
    >>> print(iter.get_next(datetime))   # 2010-02-03 04:02:00
    >>>
    >>> iter = croniter('2 4 1 * wed', base, day_or=False)  # 04:02 on every 1st day of the month if it is a Wednesday
    >>> print(iter.get_next(datetime))   # 2010-09-01 04:02:00
    >>> print(iter.get_next(datetime))   # 2010-12-01 04:02:00
    >>> print(iter.get_next(datetime))   # 2011-06-01 04:02:00
    >>> iter = croniter('0 0 * * sat#1,sun#2', base)
    >>> print(iter.get_next(datetime))   # datetime.datetime(2010, 2, 6, 0, 0)

All you need to know is how to use the constructor and the ``get_next``
method, the signature of these methods are listed below::

    >>> def __init__(self, cron_format, start_time=time.time(), day_or=True)

croniter iterates along with ``cron_format`` from ``start_time``.
``cron_format`` is **min hour day month day_of_week**, you can refer to
http://en.wikipedia.org/wiki/Cron for more details. The ``day_or``
switch is used to control how croniter handles **day** and **day_of_week**
entries. Default option is the cron behaviour, which connects those
values using **OR**. If the switch is set to False, the values are connected
using **AND**. This behaves like fcron and enables you to e.g. define a job that
executes each 2nd friday of a month by setting the days of month and the
weekday.
::

    >>> def get_next(self, ret_type=float)

get_next calculates the next value according to the cron expression and
returns an object of type ``ret_type``. ``ret_type`` should be a ``float`` or a
``datetime`` object.

Supported added for ``get_prev`` method. (>= 0.2.0)::

    >>> base = datetime(2010, 8, 25)
    >>> itr = croniter('0 0 1 * *', base)
    >>> print(itr.get_prev(datetime))  # 2010-08-01 00:00:00
    >>> print(itr.get_prev(datetime))  # 2010-07-01 00:00:00
    >>> print(itr.get_prev(datetime))  # 2010-06-01 00:00:00

You can validate your crons using ``is_valid`` class method. (>= 0.3.18)::

    >>> croniter.is_valid('0 0 1 * *')  # True
    >>> croniter.is_valid('0 wrong_value 1 * *')  # False

About DST
=========
Be sure to init your croniter instance with a TZ aware datetime for this to work !::

    >>> local_date = tz.localize(datetime(2017, 3, 26))
    >>> val = croniter('0 0 * * *', local_date).get_next(datetime)

Develop this package
====================

::

    git clone https://github.com/kiorky/croniter.git
    cd croniter
    virtualenv --no-site-packages venv
    . venv/bin/activate
    pip install --upgrade -r requirements/test.txt
    py.test src


Make a new release
====================
We use zest.fullreleaser, a great release infrastructure.

Do and follow these instructions
::

    . venv/bin/activate
    pip install --upgrade -r requirements/release.txt
    fullrelease


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
