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
.. image:: https://travis-ci.org/kiorky/croniter.svg?branch=master
    :target: https://travis-ci.org/kiorky/croniter


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
Be sure to init your croniter instance with a TZ aware datetime for this to work!

Example using pytz::

    >>> import pytz
    >>> tz = pytz.timezone("Europe/Paris")
    >>> local_date = tz.localize(datetime(2017, 3, 26))
    >>> val = croniter('0 0 * * *', local_date).get_next(datetime)

Example using python_dateutil::

    >>> import dateutil.tz
    >>> tz = dateutil.tz.gettz('Asia/Tokyo')
    >>> local_date = datetime(2017, 3, 26, tzinfo=tz)
    >>> val = croniter('0 0 * * *', local_date).get_next(datetime)


About second repeats
=====================
Croniter is able to do second repeatition crontabs form::

    >>> croniter('* * * * * 1', local_date).get_next(datetime)
    >>> base = datetime(2012, 4, 6, 13, 26, 10)
    >>> itr = croniter('* * * * * 15,25', base)
    >>> itr.get_next(datetime) # 4/6 13:26:15
    >>> itr.get_next(datetime) # 4/6 13:26:25
    >>> itr.get_next(datetime) # 4/6 13:27:15

You can also note that this expression will repeat every second from the start datetime.::

    >>> croniter('* * * * * *', local_date).get_next(datetime)

Testing if a date matchs a crontab
==================================
Test for a match with (>=0.3.32)::

    >>> croniter.match("0 0 * * *", datetime(2019, 1, 14, 0, 0, 0, 0))
    True
    >>> croniter.match("0 0 * * *", datetime(2019, 1, 14, 0, 2, 0, 0))
    False
    >>>
    >>> croniter.match("2 4 1 * wed", datetime(2019, 1, 1, 4, 2, 0, 0)) # 04:02 on every Wednesday OR on 1st day of month
    True
    >>> croniter.match("2 4 1 * wed", datetime(2019, 1, 1, 4, 2, 0, 0), day_or=False) # 04:02 on every 1st day of the month if it is a Wednesday
    False

Gaps between date matches
=========================
For performance reasons, croniter limits the amount of CPU cycles spent attempting to find the next match.
By default croniter stops looking for dates more than 50 years away from the current time, and if the next cannot be reached within that span then ``CroniterBadDateError`` is raised.
This works fine for most "normal" cron expressions, but can be limiting for very rare cron expressions.

For example, say you're looking to match 4AM Friday January 1st.
Since January 1 isn't often a Friday, it can be a few years between each occurrence.
Starting in v0.3.35, croniter provides a ``max_years_between_matches`` parameter that allows more than 50 years default to be extended for scenarios like this::

    >>> it = croniter("0 4 1 1 fri", datetime(2000,1,1), day_or=False, max_years_between_matches=100).all_next(datetime)
    >>> for i in range(5):
    ...     print(next(it))
    ...
    2010-01-01 04:00:00
    2016-01-01 04:00:00
    2021-01-01 04:00:00
    2027-01-01 04:00:00
    2038-01-01 04:00:00

Trying this without ``max_years_between_matches`` results in an exception, because there's a full decade between the 2000 start date and the first match in 2010::

    >>> it = croniter("0 4 1 1 fri", datetime(2000,1,1), day_or=False).all_next()
    >>> next(it)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      ...
    croniter.CroniterBadDateError: failed to find next date

One advantage of explicitly specifying ``max_years_between_matches`` is that it simplifies the various iterable interfaces.
Specifically ``all_next()``, ``all_prev()`` and ``iter()``) stop raising the ``CroniterBadDateError`` exception when a window is specified.
The rationale is that since you've explicitly told croniter how far to look into the future (or past) to find the next/previous date, there's no need for a special exception.
Instead, if no match is found then iteration is stopped.
This makes the these iterable interfaces act as more like normal Python iterators without having to deal with any extra exceptions.
This distinction allows v0.3.35 and later to keep the same default behavior as earlier versions.

In summary:  For many cron expressions this will never matter.  Use ``max_years_between_matches`` to make iteration simplier.

Iterating over a range using cron
=================================
Find matches within a range using the ``croniter_range()`` function.  This is much like the builtin ``range(start,stop,step)`` function, but for dates.  The `step` argument is a cron expression.
Added in (>=0.3.34)

List the first Saturday of every month in 2019::

    >>> from croniter import croniter_range
    >>> for dt in croniter_range(datetime(2019, 1, 1), datetime(2019, 12, 31), "0 0 * * sat#1"):
    >>>     print(dt)


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
    ./release.sh


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
    - lowell80
