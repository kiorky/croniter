Changelog
==============

0.3.23 (2018-05-23)
-------------------

- fix `get_next` while perserving the fix of `get_prev` in 7661c2aaa
  [Avikam Agur <avikam@pagaya-inv.com>]


0.3.22 (2018-05-16)
-------------------
- Don't count previous minute if now is dynamic
  If the code is triggered from 5-asterisk based cron
  `get_prev` based on `datetime.now()` is expected to return
  current cron iteration and not previous execution.
  [Igor Khrol <igor.khrol@toptal.com>]

0.3.20 (2017-11-06)
-------------------

- More DST fixes
  [Kevin Rose <kbrose@github>]


0.3.19 (2017-08-31)
-------------------

- fix #87: backward dst changes
  [kiorky]


0.3.18 (2017-08-31)
-------------------

- Add is valid method, refactor errors
  [otherpirate, Mauro Murari <mauro_murari@hotmail.com>]


0.3.17 (2017-05-22)
-------------------
- DOW occurence sharp style support.
  [kiorky, Kengo Seki <sekikn@apache.org>]


0.3.16 (2017-03-15)
-------------------

- Better test suite [mrcrilly@github]
- DST support [kiorky]

0.3.15 (2017-02-16)
-------------------

- fix bug around multiple conditions and range_val in
  _get_prev_nearest_diff.
  [abeja-yuki@github]

0.3.14 (2017-01-25)
-------------------

- issue #69: added day_or option to change behavior when day-of-month and
  day-of-week is given
  [Andreas Vogl <a.vogl@hackner-security.com>]



0.3.13 (2016-11-01)
-------------------

- `Real fix for #34 <https://github.com/taichino/croniter/pull/73>`_
  [kiorky@github]
- `Modernize test infra <https://github.com/taichino/croniter/pull/72>`_
  [kiorky@github]
- `Release as a universal wheel <https://github.com/kiorky/croniter/pull/16>`_
  [adamchainz@github]
- `Raise ValueError on negative numbers <https://github.com/taichino/croniter/pull/63>`_
  [josegonzalez@github]
- `Compare types using "issubclass" instead of exact match <https://github.com/taichino/croniter/pull/70>`_
  [darkk@github]
- `Implement step cron with a variable base <https://github.com/taichino/croniter/pull/60>`_
  [josegonzalez@github]

0.3.12 (2016-03-10)
-------------------
- support setting ret_type in __init__ [Brent Tubbs <brent.tubbs@gmail.com>]

0.3.11 (2016-01-13)
-------------------

- Bug fix: The get_prev API crashed when last day of month token was used. Some
  essential logic was missing.
  [Iddo Aviram <iddo.aviram@similarweb.com>]


0.3.10 (2015-11-29)
-------------------

- The fuctionality of 'l' as day of month was broken, since the month variable
  was not properly updated
  [Iddo Aviram <iddo.aviram@similarweb.com>]

0.3.9 (2015-11-19)
------------------

- Don't use datetime functions python 2.6 doesn't support
  [petervtzand]

0.3.8 (2015-06-23)
------------------
- Truncate microseconds by setting to 0
  [Corey Wright]


0.3.7 (2015-06-01)
------------------

- converting sun in range sun-thu transforms to int 0 which is
  recognized as empty string; the solution was to convert sun to string "0"

0.3.6 (2015-05-29)
------------------

- Fix default behavior when no start_time given
  Default value for `start_time` parameter is calculated at module init time rather than call time.
- Fix timezone support and stop depending on the system time zone



0.3.5 (2014-08-01)
------------------

- support for 'l' (last day of month)


0.3.4 (2014-01-30)
------------------

- Python 3 compat
- QA Relase


0.3.3 (2012-09-29)
------------------
- proper packaging

