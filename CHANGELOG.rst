Changelog
==============

1.4.1 (unreleased)
------------------

- Make a retrocompatible version of 1.4.0 change about supporting VIXIECRON bug. (fix #47)
  [kiorky]


1.4.0 (2023-06-15)
------------------

- Added "implement_cron_bug" flag to make the cron parser compatible with a bug in Vixie/ISC Cron
  [kiorky, David White <dwhite2@cisco.com>]
  *WARNING*: EXPAND METHOD CHANGES RETURN VALUE


1.3.15 (2023-05-25)
-------------------

- Fix hashed expressions omitting some entries
  [@waltervos/Walter Vos <walter.vos@ns.nl>]
- Enhance .match() precision for 6 position expressions
  [@szpol/szymon <szymon.polinkiewicz@gmail.com>]

1.3.14 (2023-04-12)
-------------------

- Lint


1.3.13 (2023-04-12)
-------------------

- Add check for range begin/end



1.3.12 (2023-04-12)
-------------------

- restore py2 compat


1.3.11 (2023-04-12)
-------------------

-  Do not expose `i` into global namespace


1.3.10 (2023-04-07)
-------------------

- Fix DOW hash parsing [kiorky]
- better error handling on py3 [kiorky]

1.3.8 (2022-11-22)
------------------

- Add Python 3.11 support and move docs files to main folder [rafsaf]


1.3.7 (2022-09-06)
------------------

- fix tests
- Fix croniter_range infinite loop  [Shachar Snapiri <ssnapiri@paloaltonetworks.com>]


1.3.5 (2022-05-14)
------------------

- Add Python 3.10 support [eelkevdbos]


1.3.4 (2022-02-18)
------------------

- Really fix compat for tests under py27
  [kiorky]


1.3.3 (2022-02-18)
------------------

- Fix compat for tests under py27
  [kiorky]


1.3.2 (2022-02-18)
------------------

- Fix #12: regressions with set_current
  [kiorky, agateblue]


1.3.1 (2022-02-15)
------------------

- Restore compat with python2
  [kiorky]


1.3.0 (2022-02-15)
------------------

- Add a way to make next() easier to use. This fixes #11
  [kiorky]


1.2.0 (2022-01-14)
------------------

- Enforce validation for day=1. Before this release we used to support day=0 and it was silently glided to day=1 to support having both day in day in 4th field when it came to have 6fields cron forms (second repeat). It will now raises a CroniterBadDateError. See https://github.com/kiorky/croniter/issues/6
  [kiorky]

1.1.0 (2021-12-03)
------------------

- Enforce validation for month=1. Before this release we used to support month=0 and it was silently glided to month=1 to support having both day in month in 4th field when it came to have 6fields cron forms (second repeat). It will now raises a CroniterBadDateError. See https://github.com/kiorky/croniter/issues/6
  [kiorky]

1.0.15 (2021-06-25)
-------------------

- restore py2 [kiorky]


1.0.14 (2021-06-25)
-------------------

- better type checks [kiorky]


1.0.13 (2021-05-06)
-------------------

- Fix ZeroDivisionError with ``* * R/0 * *``
  [cuu508]

1.0.12 (2021-04-13)
-------------------

- Add support for hashed/random/keyword expressions
  Ryan Finnie (rfinnie)
- Review support support for hashed/random/keyword expression and add expanders reactor
  [ kiorky ]


1.0.11 (2021-04-07)
-------------------

- fix bug: bad case:``0 6 30 3 *``
  [zed2015(zhangchi)]
- Add support for ``L`` in the day_of_week component.  This enable expressions like ``* * * * L4``, which means last Thursday of the month.  This resolves #159.
  [Kintyre]
- Create ``CroniterUnsupportedSyntaxError`` exception for situations where CRON syntax may be valid but some combinations of features is not supported.
  Currently, this is used when the ``day_of_week`` component has a combination of literal values and nth/last syntax at the same time.
  For example, ``0 0 * * 1,L6`` or ``0 0 * * 15,sat#1`` will both raise this exception because of mixing literal days of the week with nth-weekday or last-weekday syntax.
  This *may* impact existing cron expressions in prior releases, because ``0 0 * * 15,sat#1`` was previously allowed but incorrectly handled.
  [Kintyre]

- Update ``croniter_range()`` to allow an alternate ``croniter`` class to be used.  Helpful when using a custom class derived from croniter.
  [Kintyre]


1.0.10 (2021-03-25)
-------------------

- Remove external library ``natsort``.
  Sorting of cron expression components now handled with ``sorted()`` with a custom ``key`` function.
  [Kintyre]



1.0.9 (2021-03-23)
------------------

- Remove futures dependency
  [kiorky]


1.0.8 (2021-03-06)
------------------

- Update `_expand` to lowercase each component of the expression.
  This is in relation to #157. With this change, croniter accepts and correctly handles `* * 10-L * *`.
  [cuu508]


1.0.7 (2021-03-02)
------------------

- Fix _expand to reject int literals with underscores
  [cuu508]
- Remove a debug statement to make flake8 happy
  [cuu508]

1.0.6 (2021-02-01)
------------------

- Fix combination of star and invalid expression bugs
  [kiorky]


1.0.5 (2021-01-29)
------------------

- Security fix: fix overflow when using cron ranges
  [kiorky]

1.0.4 (2021-01-29)
------------------

- Spelling fix release


1.0.3 (2021-01-29)
------------------

- Fix #155: raise CroniterBadCronError when error syntax
  [kiorky]


1.0.2 (2021-01-19)
------------------

- Fix match when datetime has microseconds
  [kiorky]

1.0.1 (2021-01-06)
------------------
- no changes, just to make sense with new semver2 (making croniter on a stable state)
  [kiorky]


0.3.37 (2020-12-31)
-------------------

- Added Python 3.8 and 3.9 support
  [eumiro]


0.3.36 (2020-11-02)
-------------------

- Updated docs section regarding ``max_years_between_matches`` to be more shorter and hopefully more relevant.
  [Kintyre]
- Don't install tests
  [scop]


0.3.35 (2020-10-11)
-------------------

- Handle L in ranges. This fixes #142.
  [kiorky]
- Add a new initialization parameter ``max_years_between_matches`` to support finding the next/previous date beyond the default 1 year window, if so desired.  Updated README to include additional notes and example of this usage.  Fixes #145.
  [Kintyre]
- The ``croniter_range()`` function was updated to automatically determines the appropriate ``max_years_between_matches`` value, this preventing handling of the ``CroniterBadDateError`` exception.
  [Kintyre]
- Updated exception handling classes:  ``CroniterBadDateError`` now only
  applies during date finding operations (next/prev), and all parsing errors can now be caught using ``CroniterBadCronError``.  The ``CroniterNotAlphaError`` exception is now a subclass of ``CroniterBadCronError``.  A brief description of each exception class was added as an inline docstring.
  [Kintyre]
- Updated iterable interfaces to replace the ``CroniterBadDateError`` with ``StopIteration`` if (and only if) the ``max_years_between_matches`` argument is provided.  The rationale here is that if the user has specified the max tolerance between matches, then there's no need to further inform them of no additional matches.  Just stop the iteration.  This also keeps backwards compatibility.
  [Kintyre]
- Minor docs update
  [Kintyre]


0.3.34 (2020-06-19)
-------------------

- Feat ``croniter_range(start, stop, cron)``
  [Kintyre]
- Optimization for poorly written cron expression
  [Kintyre]

0.3.33 (2020-06-15)
-------------------

- Make dateutil tz support more official
  [Kintyre]
- Feat/support for day or
  [田口信元]

0.3.32 (2020-05-27)
-------------------

- document seconds repeats, fixes #122
  [kiorky]
- Implement match method, fixes #54
  [kiorky]
- Adding tests for #127 (test more DSTs and croniter behavior around)
  [kiorky]
- Changed lag_hours comparison to absolute to manage dst boundary when getting previous
  [Sokkka]

0.3.31 (2020-01-02)
-------------------

- Fix get_next() when start_time less then 1s before next instant
  [AlexHill]


0.3.30 (2019-04-20)
-------------------

- credits


0.3.29 (2019-03-26)
-------------------

- credits
- history stripping (security)
- Handle -Sun notation, This fixes `#119 <https://github.com/taichino/croniter/issues/119>`_.
  [kiorky]
- Handle invalid ranges correctly,  This fixes `#114 <https://github.com/taichino/croniter/issues/114>`_.
  [kiorky]

0.3.25 (2018-08-07)
-------------------
- Pypi hygiene
  [hugovk]


0.3.24 (2018-06-20)
-------------------
- fix `#107 <https://github.com/taichino/croniter/issues/107>`_: microsecond threshold
  [kiorky]


0.3.23 (2018-05-23)
-------------------

- fix ``get_next`` while preserving the fix of ``get_prev`` in 7661c2aaa
  [Avikam Agur <avikam@pagaya-inv.com>]


0.3.22 (2018-05-16)
-------------------
- Don't count previous minute if now is dynamic
  If the code is triggered from 5-asterisk based cron
  ``get_prev`` based on ``datetime.now()`` is expected to return
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
- DOW occurrence sharp style support.
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

- The functionality of 'l' as day of month was broken, since the month variable
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
  Default value for ``start_time`` parameter is calculated at module init time rather than call time.
- Fix timezone support and stop depending on the system time zone



0.3.5 (2014-08-01)
------------------

- support for 'l' (last day of month)


0.3.4 (2014-01-30)
------------------

- Python 3 compat
- QA Release


0.3.3 (2012-09-29)
------------------
- proper packaging

