#!/usr/bin/env python
"""
All related DST croniter tests are isolated here.
"""
# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from collections import OrderedDict
from datetime import datetime, timedelta
import os
import time


from croniter import (
    HOUR_FIELD,
    CroniterBadCronError,
    CroniterBadDateError,
    CroniterBadTypeRangeError,
    CroniterError,
    croniter,
    croniter_range,
    datetime_to_timestamp,
    timestamp_to_datetime,
    get_tz_id,
    cron_m,
    reset_datetime_dst,
)
from croniter.tests import base

ORIG_OVERFLOW32B_MODE = cron_m.OVERFLOW32B_MODE


class CroniterDstTest(base.TestCase):

    def test_timezone_dst(self):
        """Test across DST transition, which technically is a timezone change."""
        tz = "US/Eastern"
        start = self.tz_localize(datetime(2020, 10, 30), tz)
        stop = self.tz_localize(datetime(2020, 11, 10), tz)
        res = list(croniter_range(start, stop, "0 0 * * *"))
        self.assertNotEqual(res[0].utcoffset(), res[-1].utcoffset())
        self.assertEqual(len(res), 12)

    def test_range_dst_backwards(self):
        tz = "US/Eastern"  # US/Eastern: 2020/03/08 02:00-4 EDT > 01:00-5 EST-1H
        rets, rrets = [], []
        start = self.tz_localize(datetime(2020, 10, 30), tz)
        end = self.tz_localize(datetime(2020, 11, 3), tz)
        forward_rets = [
            # fmt: off
            ((0, 0), ['2020-10-30T00:00:00-04:00', '2020-10-31T00:00:00-04:00',
                      '2020-11-01T00:00:00-04:00', '2020-11-02T00:00:00-05:00', '2020-11-03T00:00:00-05:00']),
            ((0, 30), ['2020-10-30T00:30:00-04:00', '2020-10-31T00:30:00-04:00',
                       '2020-11-01T00:30:00-04:00', '2020-11-02T00:30:00-05:00']),
            ((1, 0), ['2020-10-30T01:00:00-04:00', '2020-10-31T01:00:00-04:00',
                      '2020-11-01T01:00:00-04:00', '2020-11-02T01:00:00-05:00']),
            ((1, 30), ['2020-10-30T01:30:00-04:00', '2020-10-31T01:30:00-04:00',
                       '2020-11-01T01:30:00-04:00', '2020-11-02T01:30:00-05:00']),
            ((2, 0), ['2020-10-30T02:00:00-04:00', '2020-10-31T02:00:00-04:00',
                      '2020-11-01T02:00:00-05:00', '2020-11-02T02:00:00-05:00']),
            ((2, 30), ['2020-10-30T02:30:00-04:00', '2020-10-31T02:30:00-04:00',
                       '2020-11-01T02:30:00-05:00', '2020-11-02T02:30:00-05:00']),
            ((3, 0), ['2020-10-30T03:00:00-04:00', '2020-10-31T03:00:00-04:00',
                      '2020-11-01T03:00:00-05:00', '2020-11-02T03:00:00-05:00']),
            ((3, 30), ['2020-10-30T03:30:00-04:00', '2020-10-31T03:30:00-04:00',
                       '2020-11-01T03:30:00-05:00', '2020-11-02T03:30:00-05:00'])
            # fmt: on
        ]
        reverse_rets = [
            # fmt: off
            ((0, 0), ['2020-11-03T00:00:00-05:00', '2020-11-02T00:00:00-05:00',
                      '2020-11-01T00:00:00-04:00', '2020-10-31T00:00:00-04:00', '2020-10-30T00:00:00-04:00']),
            ((0, 30), ['2020-11-02T00:30:00-05:00', '2020-11-01T00:30:00-04:00',
                       '2020-10-31T00:30:00-04:00', '2020-10-30T00:30:00-04:00']),
            ((1, 0), ['2020-11-02T01:00:00-05:00', '2020-11-01T01:00:00-04:00',
                      '2020-10-31T01:00:00-04:00', '2020-10-30T01:00:00-04:00']),
            ((1, 30), ['2020-11-02T01:30:00-05:00', '2020-11-01T01:30:00-04:00',
                       '2020-10-31T01:30:00-04:00', '2020-10-30T01:30:00-04:00']),
            ((2, 0), ['2020-11-02T02:00:00-05:00', '2020-11-01T02:00:00-05:00',
                      '2020-10-31T02:00:00-04:00', '2020-10-30T02:00:00-04:00']),
            ((2, 30), ['2020-11-02T02:30:00-05:00', '2020-11-01T02:30:00-05:00',
                       '2020-10-31T02:30:00-04:00', '2020-10-30T02:30:00-04:00']),
            ((3, 0), ['2020-11-02T03:00:00-05:00', '2020-11-01T03:00:00-05:00',
                      '2020-10-31T03:00:00-04:00', '2020-10-30T03:00:00-04:00']),
            ((3, 30), ['2020-11-02T03:30:00-05:00', '2020-11-01T03:30:00-05:00',
                       '2020-10-31T03:30:00-04:00', '2020-10-30T03:30:00-04:00'])
            # fmt: on
        ]
        # fmt: off
        for hour in (0, 1, 2, 3,):
            for minute in (0, 30,):
                rets.append((
                    (hour, minute),
                    [a.isoformat() for a in croniter_range(
                        start, end, "{1} {0} * * *".format(hour, minute)
                    )]
                ))
                rrets.append((
                    (hour, minute),
                    [a.isoformat() for a in croniter_range(
                        end, start, "{1} {0} * * *".format(hour, minute)
                    )]
                ))
        # fmt: on
        self.assertEqual(rrets, reverse_rets)
        self.assertEqual(rets, forward_rets)

    def test_range_dst_forward(self):
        tz = "US/Eastern"  # US/Eastern: 2020/03/08 02:00-5 EST > 03:00-4 EDT+1H
        rets, rrets = [], []
        start = self.tz_localize(datetime(2020, 3, 7), tz)
        end = self.tz_localize(datetime(2020, 3, 11), tz)
        forward_rets = [
            # fmt: off
            ((1, 0), ['2020-03-07T01:00:00-05:00', '2020-03-08T01:00:00-05:00',
                      '2020-03-09T01:00:00-04:00', '2020-03-10T01:00:00-04:00']),
            ((1, 30), ['2020-03-07T01:30:00-05:00', '2020-03-08T01:30:00-05:00',
                       '2020-03-09T01:30:00-04:00', '2020-03-10T01:30:00-04:00']),
            ((2, 0), ['2020-03-07T02:00:00-05:00', '2020-03-08T03:00:00-04:00',
                      '2020-03-09T02:00:00-04:00', '2020-03-10T02:00:00-04:00']),
            ((2, 30), ['2020-03-07T02:30:00-05:00', '2020-03-08T03:30:00-04:00',
                       '2020-03-09T02:30:00-04:00', '2020-03-10T02:30:00-04:00']),
            ((3, 0), ['2020-03-07T03:00:00-05:00', '2020-03-08T03:00:00-04:00',
                      '2020-03-09T03:00:00-04:00', '2020-03-10T03:00:00-04:00']),
            ((3, 30), ['2020-03-07T03:30:00-05:00', '2020-03-08T03:30:00-04:00',
                       '2020-03-09T03:30:00-04:00', '2020-03-10T03:30:00-04:00']),
            ((4, 0), ['2020-03-07T04:00:00-05:00', '2020-03-08T04:00:00-04:00',
                      '2020-03-09T04:00:00-04:00', '2020-03-10T04:00:00-04:00']),
            ((4, 30), ['2020-03-07T04:30:00-05:00', '2020-03-08T04:30:00-04:00',
                       '2020-03-09T04:30:00-04:00', '2020-03-10T04:30:00-04:00'])
            # fmt: on
        ]
        reverse_rets = [
            # fmt: off
            ((1, 0), ['2020-03-10T01:00:00-04:00', '2020-03-09T01:00:00-04:00',
                      '2020-03-08T01:00:00-05:00', '2020-03-07T01:00:00-05:00']),
            ((1, 30), ['2020-03-10T01:30:00-04:00', '2020-03-09T01:30:00-04:00',
                       '2020-03-08T01:30:00-05:00', '2020-03-07T01:30:00-05:00']),
            ((2, 0), ['2020-03-10T02:00:00-04:00', '2020-03-09T02:00:00-04:00',
                      '2020-03-08T03:00:00-04:00', '2020-03-07T02:00:00-05:00']),
            ((2, 30), ['2020-03-10T02:30:00-04:00', '2020-03-09T02:30:00-04:00',
                       '2020-03-08T03:30:00-04:00', '2020-03-07T02:30:00-05:00']),
            ((3, 0), ['2020-03-10T03:00:00-04:00', '2020-03-09T03:00:00-04:00',
                      '2020-03-08T03:00:00-04:00', '2020-03-07T03:00:00-05:00']),
            ((3, 30), ['2020-03-10T03:30:00-04:00', '2020-03-09T03:30:00-04:00',
                       '2020-03-08T03:30:00-04:00', '2020-03-07T03:30:00-05:00']),
            ((4, 0), ['2020-03-10T04:00:00-04:00', '2020-03-09T04:00:00-04:00',
                      '2020-03-08T04:00:00-04:00', '2020-03-07T04:00:00-05:00']),
            ((4, 30), ['2020-03-10T04:30:00-04:00', '2020-03-09T04:30:00-04:00',
                       '2020-03-08T04:30:00-04:00', '2020-03-07T04:30:00-05:00'])
            # fmt: on
        ]
        # for hour in (1,):
        # for hour in (1, 2, 3, 4,) :
        for hour in (2,):
            # for minute in (0,) :
            # for minute in (0, 30,):
            for minute in (30,):
                # rets.append((
                #     (hour, minute),
                #     [a.isoformat() for a in croniter_range(
                #         start, end, "{1} {0} * * *".format(hour, minute)
                #     )]
                # ))
                rrets.append((
                    (hour, minute),
                    [a.isoformat() for a in croniter_range(
                        end, start, "{1} {0} * * *".format(hour, minute)
                    )]
                ))
        self.assertEqual(rrets, reverse_rets)
        self.assertEqual(rets, forward_rets)

    def _add_dst_tests(self, dst, tz, offset_from_dst, tests, expected, offset_seconds=3600):
        dt = dst + timedelta(seconds=offset_from_dst * offset_seconds)
        test_serie = tests.setdefault((dst.isoformat(), dt.isoformat(), offset_from_dst), [])
        for offset, expected_result in expected:
            test_serie.append((dt.replace(tzinfo=tz), [(dst.hour + offset) % 24], offset, expected_result))

    def _add_test_prev_non_dst(self, dst, tests):
        # fmt: off
        for i in (-18, -10, -6, -2, -1, 2, 6, 10, 18,):  # days not around dst
            d = dst + timedelta(days=i)
            for h in (0, 1, 2, 3, 4, 5, 6, 10, 15, 22, 23,):
                for c in (0, 1, 3, 4, 5, 6, 10, 15, 22, 23, 24, 25, 26, 27, None,):
                    # fmt: on
                    test_serie = tests["Not on DST: {0}/{1}/{2}".format(d.isoformat(), h, c)] = []
                    val = c
                    if val is not None and val <= h:
                        val = val - h
                    elif val is None:
                        val = None
                    else:
                        if val > 24:
                            val = -(val % 24)
                        else:
                            val = val - h - 24
                    test_serie.append(
                        (d.replace(hour=h), [c if c is not None else h + 1], None, val,)
                    )

    def _test_nearest_diff_forward(self, all_dsts, all_tests, to_round=True):
        cron = croniter('* * * * *')
        for dst, tests in all_tests.items():
            for tsname, test_serie in tests.items():
                rets = []
                for dt, c, offset, ret in test_serie:
                    rets.append(
                        [
                            offset,
                            cron._get_prev_nearest_diff(
                                dt.hour,
                                c,
                                None if ret is None else 24,
                                field=HOUR_FIELD if dt.tzinfo else None,
                                current=dt if dt.tzinfo else None,
                            )
                        ]
                    )
                    if to_round and rets[-1][1]:
                        rets[-1][1] = int(rets[-1][1])
                try:
                    asserts = [[a[2], a[3]] for a in test_serie]
                    self.assertEqual(rets, asserts, "{0}: test serie failed".format(tsname))
                except:
                    import pdb;pdb.set_trace()  ## Breakpoint ##
                    raise

    def test_prev_half_nearest_diff_forward(self):
        all_dsts = [
            (datetime(2024, 10, 6, 2, 0, 0), self.tz('Australia/Lord_Howe')),  # +1/2h change !
        ]
        all_tests = OrderedDict()
        for dst, tz in all_dsts:
            tests = all_tests.setdefault(repr(dst), OrderedDict())
            # fmt: off
            expected = [
                [-23, -19], [-22, -18], [-21, -17], [-20, -16], [-15, -11], [-10, -6],
                [-8, -4], [-5, -1], [-4, 0], [-3, -23], [-2, -22], [-1, -21],
                [0, -20], [1, -19], [2, -18], [3, -17], [4, -16], [5, -15], [8, -12], [10, -10],
                [15, -5], [20, 0], [21, -23], [22, -22], [23, -21],
            ]
            self._add_dst_tests(dst, tz, -4, tests, expected)
            expected = [
                [-23, -20], [-22, -19], [-21, -18], [-20, -17], [-15, -12], [-10, -7],
                [-8, -5], [-5, -2], [-4, -1], [-3, 0], [-2, -23], [-1, -22],
                [0, -21], [1, -20], [2, -19], [3, -18], [4, -17], [5, -16], [8, -13],
                [10, -11], [15, -6], [20, -1], [21, -0], [22, -23], [23, -22],
            ]
            self._add_dst_tests(dst, tz, -3, tests, expected)
            expected = [
                [-23, -21], [-22, -20], [-21, -19], [-20, -18], [-15, -13], [-10, -8],
                [-8, -6], [-5, -3], [-4, -2], [-3, -1], [-2, 0], [-1, -23],
                [0, -22], [1, -21], [2, -20], [3, -19], [4, -18], [5, -17], [8, -14],
                [10, -12], [15, -7], [20, -2], [21, -1], [22, 0], [23, -23],
            ]
            self._add_dst_tests(dst, tz, -2, tests, expected)
            expected = [
                [-23, -22], [-22, -21], [-21, -20], [-20, -19], [-15, -14], [-10, -9],
                [-8, -7], [-5, -4], [-4, -3], [-3, -2], [-2, -1], [-1, 0],
                [0, -23], [1, -22], [2, -21], [3, -20], [4, -19], [5, -18], [8, -15],
                [10, -13], [15, -8], [20, -3], [21, -2], [22, -1], [23, -0],
            ]
            self._add_dst_tests(dst, tz, -1, tests, expected)
            expected = [
                [-23, -22.5], [-22, -21.5], [-21, -20.5], [-20, -19.5], [-15, -14.5], [-10, -9.5],
                [-8, -7.5], [-5, -4.5], [-4, -3.5], [-3, -2.5], [-2, -1.5], [-1, -0.5],
                [0, 0], [1, -22.5], [2, -21.5], [3, -20.5], [4, -19.5], [5, -18.5], [8, -15.5],
                [10, -13.5], [15, -8.5], [20, -3.5], [21, -2.5], [22, -1.5], [23, -0.5],
            ]
            self._add_dst_tests(dst, tz, 0, tests, expected)
            expected = [
                [-23, 0], [-22, -22.5], [-21, -21.5], [-20, -20.5], [-15, -15.5], [-10, -10.5],
                [-8, -8.5], [-5, -5.5], [-4, -4.5], [-3, -3.5], [-2, -2.5], [-1, -1.5],
                [0, -1], [1, 0], [2, -22.5], [3, -21.5], [4, -20.5], [5, -19.5], [8, -16.5],
                [10, -14.5], [15, -9.5], [20, -4.5], [21, -3.5], [22, -2.5], [23, -1.5],
            ]
            self._add_dst_tests(dst, tz, 1, tests, expected)
            expected = [
                (-23, -1), (-22, 0), (-21, -22.5), (-20, -21.5), (-15, -16.5), (-10, -11.5),
                (-8, -9.5), (-5, -6.5), (-3, -4.5), (-2, -3.5), (-1, -2.5),
                (0, -2), (1, -1), (2, 0), (3, -22.5), (4, -21.5), (5, -20.5), (8, -17.5),
                (10, -15.5), (15, -10.5), (20, -5.5), (21, -4.5), (22, -3.5), (23, -2.5),
            ]
            self._add_dst_tests(dst, tz, 2, tests, expected)
            expected = [
                [-23, -2], [-22, -1], [-21, 0], [-20, -22.5], [-15, -17.5], [-10, -12.5], [-8, -10.5],
                [-5, -7.5], [-3, -5.5], [-2, -4.5], [-1, -3.5],
                [0, -3.0], [1, -2], [2, -1], [3, 0], [4, -22.5], [5, -21.5], [8, -18.5], [10, -16.5],
                [15, -11.5], [20, -6.5], [21, -5.5], [22, -4.5], [23, -3.5]
            ]
            self._add_dst_tests(dst, tz, 3, tests, expected)
            expected = [
                [-23, -4], [-22, -3], [-21, -2], [-20, -1], [-15, -19.5], [-10, -14.5], [-8, -12.5],
                [-5, -9.5], [-3, -7.5], [-2, -6.5], [-1, -5.5],
                [0, -5.0], [1, -4], [2, -3], [3, -2], [4, -1], [5, 0], [8, -20.5], [10, -18.5],
                [15, -13.5], [20, -8.5], [21, -7.5], [22, -6.5], [23, -5.5]
            ]
            self._add_dst_tests(dst, tz, 5, tests, expected)
            expected = [
                [-23, -20], [-22, -19], [-21, -18], [-20, -17], [-15, -12], [-10, -7], [-8, -5],
                [-5, -2], [-3, 0], [-2, -22.5], [-1, -21.5],
                [0, -21.0], [1, -20], [2, -19], [3, -18], [4, -17], [5, -16], [8, -13], [10, -11],
                [15, -6], [20, -1], [21, 0], [22, -22.5], [23, -21.5]
            ]
            self._add_dst_tests(dst, tz, 21, tests, expected)
            expected = [
                [-23, -21], [-22, -20], [-21, -19], [-20, -18], [-15, -13], [-10, -8], [-8, -6],
                [-5, -3], [-3, -1], [-2, 0], [-1, -22.5],
                [0, -22.0], [1, -21], [2, -20], [3, -19], [4, -18], [5, -17], [8, -14], [10, -12],
                [15, -7], [20, -2], [21, -1], [22, 0], [23, -22.5]
            ]
            self._add_dst_tests(dst, tz, 22, tests, expected)
            expected = [
                [-23, -22], [-22, -21], [-21, -20], [-20, -19], [-15, -14], [-10, -9], [-8, -7],
                [-5, -4], [-3, -2], [-2, -1], [-1, 0],
                [0, -23.0], [1, -22], [2, -21], [3, -20], [4, -19], [5, -18], [8, -15], [10, -13],
                [15, -8], [20, -3], [21, -2], [22, -1], [23, 0]
            ]
            self._add_dst_tests(dst, tz, 23, tests, expected)
            expected = [
                [-23, -23], [-22, -22], [-21, -21], [-20, -20], [-15, -15], [-10, -10], [-8, -8],
                [-5, -5], [-3, -3], [-2, -2], [-1, -1],
                [0, 0], [1, -23], [2, -22], [3, -21], [4, -20], [5, -19], [8, -16], [10, -14],
                [15, -9], [20, -4], [21, -3], [22, -2], [23, -1]
            ]
            self._add_dst_tests(dst, tz, 24, tests, expected)
            expected = [
                [-23, 0], [-22, -23], [-21, -22], [-20, -21], [-15, -16], [-10, -11], [-8, -9],
                [-5, -6], [-3, -4], [-2, -3], [-1, -2],
                [0, -1], [1, 0], [2, -23], [3, -22], [4, -21], [5, -20], [8, -17], [10, -15],
                [15, -10], [20, -5], [21, -4], [22, -3], [23, -2]
            ]
            self._add_dst_tests(dst, tz, 25, tests, expected)
            expected = [
                [-23, -1], [-22, 0], [-21, -23], [-20, -22], [-15, -17], [-10, -12], [-8, -10],
                [-5, -7], [-3, -5], [-2, -4], [-1, -3],
                [0, -2], [1, -1], [2, 0], [3, -23], [4, -22], [5, -21], [8, -18], [10, -16],
                [15, -11], [20, -6], [21, -5], [22, -4], [23, -3]
            ]
            self._add_dst_tests(dst, tz, 26, tests, expected)
            expected = [
                [-23, -2], [-22, -1], [-21, 0], [-20, -23], [-15, -18], [-10, -13], [-8, -11],
                [-5, -8], [-3, -6], [-2, -5], [-1, -4],
                [0, -3], [1, -2], [2, -1], [3, 0], [4, -23], [5, -22], [8, -19], [10, -17],
                [15, -12], [20, -7], [21, -6], [22, -5], [23, -4]
            ]
            self._add_dst_tests(dst, tz, 27, tests, expected)
            expected = [
                [-23, -9], [-22, -8], [-21, -7], [-20, -6], [-15, -1], [-10, -20], [-8, -18],
                [-5, -15], [-3, -13], [-2, -12], [-1, -11],
                [0, -10], [1, -9], [2, -8], [3, -7], [4, -6], [5, -5], [8, -2], [10, 0],
                [15, -19], [20, -14], [21, -13], [22, -12], [23, -11]
            ]
            self._add_dst_tests(dst, tz, 34, tests, expected)
            expected = [
                [-23, -20], [-22, -19], [-21, -18], [-20, -17], [-15, -12], [-10, -7], [-8, -5],
                [-5, -2], [-3, 0], [-2, -23], [-1, -22],
                [0, -21], [1, -20], [2, -19], [3, -18], [4, -17], [5, -16], [8, -13],
                [10, -11], [15, -6], [20, -1], [21, 0], [22, -23], [23, -22]
            ]
            self._add_dst_tests(dst, tz, 45, tests, expected)
            expected = [
                [-23, -21], [-22, -20], [-21, -19], [-20, -18], [-15, -13], [-10, -8], [-8, -6],
                [-5, -3], [-3, -1], [-2, 0], [-1, -23],
                [0, -22], [1, -21], [2, -20], [3, -19], [4, -18], [5, -17], [8, -14], [10, -12],
                [15, -7], [20, -2], [21, -1], [22, 0], [23, -23]
            ]
            self._add_dst_tests(dst, tz, 46, tests, expected)
            expected = [
                [-23, -22], [-22, -21], [-21, -20], [-20, -19], [-15, -14], [-10, -9], [-8, -7],
                [-5, -4], [-3, -2], [-2, -1], [-1, 0],
                [0, -23], [1, -22], [2, -21], [3, -20], [4, -19], [5, -18], [8, -15], [10, -13],
                [15, -8], [20, -3], [21, -2], [22, -1], [23, 0]
            ]
            self._add_dst_tests(dst, tz, 47, tests, expected)
            self._add_test_prev_non_dst(dst, tests)
        # fmt: on
        self._test_nearest_diff_forward(all_dsts, all_tests, to_round=False)

    def test_prev_nearest_diff_forward(self):
        all_dsts = [
            (datetime(2020, 3, 8, 2, 0, 0), self.tz('US/Eastern')),  # +1h
            (datetime(2010, 3, 27, 22, 0), self.tz('America/Godthab')),  # +1h
            (datetime(2008, 10, 19, 0, 0), self.tz('America/Buenos_Aires')),  # +1h
            (datetime(2018, 11, 4, 0, 0, 0), self.tz('America/Sao_Paulo')),  # +1h
            (datetime(2024, 3, 31, 3, 0, 0), self.tz('Europe/Athens')),  # +1h
        ]
        all_tests = OrderedDict()
        for dst, tz in all_dsts:
            tests = all_tests.setdefault(repr(dst), OrderedDict())
            # fmt: off
            expected = [
                [-23, -19], [-22, -18], [-21, -17], [-20, -16], [-15, -11], [-10, -6],
                [-8, -4], [-5, -1], [-4, 0], [-3, -23], [-2, -22], [-1, -21],
                [0, -20], [1, -19], [2, -18], [3, -17], [4, -16], [5, -15], [8, -12], [10, -10],
                [15, -5], [20, 0], [21, -23], [22, -22], [23, -21],
            ]
            self._add_dst_tests(dst, tz, -4, tests, expected)
            expected = [
                [-22, -19], [-21, -18], [-20, -17], [-15, -12], [-10, -7],
                [-8, -5], [-5, -2], [-4, -1], [-3, 0], [-2, -23], [-1, -22],
                [0, -21], [1, -20], [2, -19], [3, -18], [4, -17], [5, -16], [8, -13],
                [10, -11], [15, -6], [20, -1], [21, -0], [22, -23], [23, -22],
            ]
            self._add_dst_tests(dst, tz, -3, tests, expected)
            expected = [
                [-23, -21], [-22, -20], [-21, -19], [-20, -18], [-15, -13], [-10, -8],
                [-8, -6], [-5, -3], [-4, -2], [-3, -1], [-2, 0], [-1, -23],
                [0, -22], [1, -21], [2, -20], [3, -19], [4, -18], [5, -17], [8, -14],
                [10, -12], [15, -7], [20, -2], [21, -1], [22, 0], [23, -23],
            ]
            self._add_dst_tests(dst, tz, -2, tests, expected)
            expected = [
                [-23, -22], [-22, -21], [-21, -20], [-20, -19], [-15, -14], [-10, -9],
                [-8, -7], [-5, -4], [-4, -3], [-3, -2], [-2, -1], [-1, 0],
                [0, -23], [1, -22], [2, -21], [3, -20], [4, -19], [5, -18], [8, -15],
                [10, -13], [15, -8], [20, -3], [21, -2], [22, -1], [23, -0],
            ]
            self._add_dst_tests(dst, tz, -1, tests, expected)
            expected = [
                [-23, 0], [-22, -22], [-21, -21], [-20, -20], [-15, -15], [-10, -10],
                [-8, -8], [-5, -5], [-4, -4], [-3, -3], [-2, -2], [-1, -1],
                [0, 0], [1, 0], [2, -22], [3, -21], [4, -20], [5, -19], [8, -16], [10, -14],
                [15, -9], [20, -4], [21, -3], [22, -2], [23, -1],
            ]
            for h in (0, 1):  # DST hour-h is synonym as DST hour-h+1
                self._add_dst_tests(dst, tz, h, tests, expected)
            expected = [
                [-23, -1], [-22, 0], [-21, -22], [-20, -21], [-15, -16], [-10, -11],
                [-8, -9], [-5, -6], [-3, -4], [-2, -3], [-1, -2],
                [0, -1], [1, -1], [2, 0], [3, -22], [4, -21], [5, -20], [8, -17],
                [10, -15], [15, -10], [20, -5], [21, -4], [22, -3], [23, -2],
            ]
            self._add_dst_tests(dst, tz, 2, tests, expected)
            expected = [
                [-23, -2], [-22, -1], [-21, -0], [-20, -22], [-15, -17], [-10, -12],
                [-8, -10], [-5, -7], [-3, -5], [-2, -4], [-1, -3],
                [0, -2], [1, -2], [2, -1], [3, 0], [4, -22], [5, -21], [8, -18],
                [10, -16], [15, -11], [20, -6], [21, -5], [22, -4], [23, -3],
            ]
            self._add_dst_tests(dst, tz, 3, tests, expected)
            expected = [
                [-23, -4], [-22, -3], [-21, -2], [-20, -1], [-15, -19], [-10, -14],
                [-8, -12], [-5, -9], [-3, -7], [-2, -6], [-1, -5],
                [0, -4], [1, -4], [2, -3], [3, -2], [4, -1], [5, 0], [8, -20], [10, -18],
                [15, -13], [20, -8], [21, -7], [22, -6], [23, -5],
            ]
            self._add_dst_tests(dst, tz, 5, tests, expected)
            expected = [
                [-23, -20], [-22, -19], [-21, -18], [-20, -17], [-15, -12], [-10, -7],
                [-8, -5], [-5, -2], [-3, 0], [-2, -22], [-1, -21],
                [0, -20], [1, -20], [2, -19], [3, -18], [4, -17], [5, -16], [8, -13],
                [10, -11], [15, -6], [20, -1], [21, 0], [22, -22], [23, -21],
            ]
            self._add_dst_tests(dst, tz, 21, tests, expected)
            expected = [
                [-23, -21], [-22, -20], [-21, -19], [-20, -18], [-15, -13], [-10, -8],
                [-8, -6], [-5, -3], [-3, -1], [-2, 0], [-1, -22],
                [0, -21], [1, -21], [2, -20], [3, -19], [4, -18], [5, -17], [8, -14],
                [10, -12], [15, -7], [20, -2], [21, -1], [22, 0], [23, -22],
            ]
            self._add_dst_tests(dst, tz, 22, tests, expected)
            expected = [
                [-23, -22], [-22, -21], [-21, -20], [-20, -19], [-15, -14], [-10, -9],
                [-8, -7], [-5, -4], [-3, -2], [-2, -1], [-1, 0],
                [0, -22], [1, -22], [2, -21], [3, -20], [4, -19], [5, -18], [8, -15],
                [10, -13], [15, -8], [20, -3], [21, -2], [22, -1], [23, 0],
            ]
            self._add_dst_tests(dst, tz, 23, tests, expected)
            expected = [
                [-23, -23], [-22, -22], [-21, -21], [-20, -20], [-15, -15], [-10, -10],
                [-8, -8], [-5, -5], [-3, -3], [-2, -2], [-1, -1],
                [0, 0], [1, -23], [2, -22], [3, -21], [4, -20], [5, -19], [8, -16],
                [10, -14], [15, -9], [20, -4], [21, -3], [22, -2], [23, -1],
            ]
            self._add_dst_tests(dst, tz, 24, tests, expected)
            expected = [
                [-23, 0], [-22, -23], [-21, -22], [-20, -21], [-15, -16], [-10, -11],
                [-8, -9], [-5, -6], [-3, -4], [-2, -3], [-1, -2],
                [0, -1], [1, 0], [2, -23], [3, -22], [4, -21], [5, -20], [8, -17], [10, -15],
                [15, -10], [20, -5], [21, -4], [22, -3], [23, -2],
            ]
            self._add_dst_tests(dst, tz, 25, tests, expected)
            expected = [
                [-23, -1], [-22, 0], [-21, -23], [-20, -22], [-15, -17], [-10, -12],
                [-8, -10], [-5, -7], [-3, -5], [-2, -4], [-1, -3],
                [0, -2], [1, -1], [2, 0], [3, -23], [4, -22], [5, -21], [8, -18],
                [10, -16], [15, -11], [20, -6], [21, -5], [22, -4], [23, -3],
            ]
            self._add_dst_tests(dst, tz, 26, tests, expected)
            expected = [
                [-23, -2], [-22, -1], [-21, 0], [-20, -23], [-15, -18], [-10, -13],
                [-8, -11], [-5, -8], [-3, -6], [-2, -5], [-1, -4],
                [0, -3], [1, -2], [2, -1], [3, 0], [4, -23], [5, -22], [8, -19],
                [10, -17], [15, -12], [20, -7], [21, -6], [22, -5], [23, -4],
            ]
            self._add_dst_tests(dst, tz, 27, tests, expected)
            expected = [
                [-23, -9], [-22, -8], [-21, -7], [-20, -6], [-15, -1], [-10, -20],
                [-8, -18], [-5, -15], [-3, -13], [-2, -12], [-1, -11],
                [0, -10], [1, -9], [2, -8], [3, -7], [4, -6], [5, -5], [8, -2], [10, 0],
                [15, -19], [20, -14], [21, -13], [22, -12], [23, -11],
            ]
            self._add_dst_tests(dst, tz, 34, tests, expected)
            expected = [
                [-23, -20], [-22, -19], [-21, -18], [-20, -17], [-15, -12], [-10, -7],
                [-8, -5], [-5, -2], [-3, 0], [-2, -23], [-1, -22],
                [0, -21], [1, -20], [2, -19], [3, -18], [4, -17], [5, -16], [8, -13],
                [10, -11], [15, -6], [20, -1], [21, 0], [22, -23], [23, -22],
            ]
            self._add_dst_tests(dst, tz, 45, tests, expected)
            expected = [
                [-23, -21], [-22, -20], [-21, -19], [-20, -18], [-15, -13], [-10, -8],
                [-8, -6], [-5, -3], [-3, -1], [-2, 0], [-1, -23],
                [0, -22], [1, -21], [2, -20], [3, -19], [4, -18], [5, -17], [8, -14], [10, -12],
                [15, -7], [20, -2], [21, -1], [22, 0], [23, -23],
            ]
            self._add_dst_tests(dst, tz, 46, tests, expected)
            expected = [
                [-23, -22], [-22, -21], [-21, -20], [-20, -19], [-15, -14], [-10, -9],
                [-8, -7], [-5, -4], [-3, -2], [-2, -1], [-1, 0],
                [0, -23], [1, -22], [2, -21], [3, -20], [4, -19], [5, -18], [8, -15], [10, -13],
                [15, -8], [20, -3], [21, -2], [22, -1], [23, 0],
            ]
            self._add_dst_tests(dst, tz, 47, tests, expected)
            self._add_test_prev_non_dst(dst, tests)
        # fmt: on
        self._test_nearest_diff_forward(all_dsts, all_tests)

    def test_prev_nearest_diff_backwards(self):
        all_dsts = [
            (datetime(2020, 11, 1, 2, 0, 0), self.tz('US/Eastern')),  # -1h
            #(datetime(2010, 3, 27, 22, 0), self.tz('America/Godthab')),  # -1h
            #(datetime(2008, 10, 19, 0, 0), self.tz('America/Buenos_Aires')),  # -1h
            #(datetime(2018, 11, 4, 0, 0, 0), self.tz('America/Sao_Paulo')),  # -1h
            #(datetime(2024, 3, 31, 3, 0, 0), self.tz('Europe/Athens')),  # -1h
        ]
        all_tests = OrderedDict()
        for dst, tz in all_dsts:
            tests = all_tests.setdefault(repr(dst), OrderedDict())
            # fmt: off
            # expected = [
            #     [-23, -19], [-22, -18], [-21, -17], [-20, -16], [-15, -11], [-10, -6],
            #     [-8, -4], [-5, -1], [-4, 0], [-3, -23], [-2, -22], [-1, -21],
            #     [0, -20], [1, -19], [2, -18], [3, -17], [4, -16], [5, -15], [8, -12], [10, -10],
            #     [15, -5], [20, 0], [21, -23], [22, -22], [23, -21],
            # ]
            # self._add_dst_tests(dst, tz, -4, tests, expected)
            # expected = [
            #     [-22, -19], [-21, -18], [-20, -17], [-15, -12], [-10, -7],
            #     [-8, -5], [-5, -2], [-4, -1], [-3, 0], [-2, -23], [-1, -22],
            #     [0, -21], [1, -20], [2, -19], [3, -18], [4, -17], [5, -16], [8, -13],
            #     [10, -11], [15, -6], [20, -1], [21, -0], [22, -23], [23, -22],
            # ]
            # self._add_dst_tests(dst, tz, -3, tests, expected)
            # expected = [
            #     [-23, -21], [-22, -20], [-21, -19], [-20, -18], [-15, -13], [-10, -8],
            #     [-8, -6], [-5, -3], [-4, -2], [-3, -1], [-2, 0], [-1, -23],
            #     [0, -22], [1, -21], [2, -20], [3, -19], [4, -18], [5, -17], [8, -14],
            #     [10, -12], [15, -7], [20, -2], [21, -1], [22, 0], [23, -23],
            # ]
            # self._add_dst_tests(dst, tz, -2, tests, expected)
            # expected = [
            #     [-23, -22], [-22, -21], [-21, -20], [-20, -19], [-15, -14], [-10, -9],
            #     [-8, -7], [-5, -4], [-4, -3], [-3, -2], [-2, -1], [-1, 0],
            #     [0, -23], [1, -22], [2, -21], [3, -20], [4, -19], [5, -18], [8, -15],
            #     [10, -13], [15, -8], [20, -3], [21, -2], [22, -1], [23, -0],
            # ]
            # self._add_dst_tests(dst, tz, -1, tests, expected)
            expected = [
                #[-23, -22], [-22, -21], [-21, -20], [-20, -19], [-15, -14], [-10, -9],
                #[-8, -7], [-5, -4], [-4, -3], [-3, -2], [-2, -1], [-1, -1],
                [0, 0], [1, -22], [2, -21], [3, -20], [4, -19], [5, -18], [8, -15],
                [10, -13], [15, -8], [20, -3], [21, -2], [22, -1], [23, -1]
            ]
            for h in (0, 1):  # DST hour-h is synonym as DST hour-h+1
                self._add_dst_tests(dst, tz, h, tests, expected)
            self._add_dst_tests(dst, tz, 2, tests, expected)
            self._add_dst_tests(dst, tz, 3, tests, expected)
            self._add_dst_tests(dst, tz, 5, tests, expected)
            self._add_dst_tests(dst, tz, 21, tests, expected)
            self._add_dst_tests(dst, tz, 22, tests, expected)
            self._add_dst_tests(dst, tz, 23, tests, expected)
            self._add_dst_tests(dst, tz, 24, tests, expected)
            self._add_dst_tests(dst, tz, 25, tests, expected)
            self._add_dst_tests(dst, tz, 26, tests, expected)
            self._add_dst_tests(dst, tz, 27, tests, expected)
            self._add_dst_tests(dst, tz, 34, tests, expected)
            self._add_dst_tests(dst, tz, 45, tests, expected)
            self._add_dst_tests(dst, tz, 46, tests, expected)
            self._add_dst_tests(dst, tz, 47, tests, expected)
            self._add_test_prev_non_dst(dst, tests)
        # fmt: on
        self._test_nearest_diff_forward(all_dsts, all_tests)



    def assertScheduleTimezone(self, callback, expected_schedule):
        for expected_date, expected_offset in expected_schedule:
            d = callback()
            self.assertEqual(expected_date, d.replace(tzinfo=None))
            self.assertEqual(expected_offset, croniter._timedelta_to_seconds(d.utcoffset()))

    def testTimezoneWinterTime(self):
        expected_schedules = [
            (
                "Europe/Athens",  # Europe/Athens: 2013/10/27 04:00+3 EEST > 03:00+2 EET
                # datetime(2013, 10, 27, 2, 0, 0),
                # datetime(2013, 10, 27, 5, 0, 0),
                datetime(2013, 10, 27, 2, 30, 0),
                datetime(2013, 10, 27, 4, 30, 0),
                [
                    (datetime(2013, 10, 27, 2, 30, 0), 10800),
                    (datetime(2014, 10, 27, 3, 0, 0), 10800),
                    (datetime(2013, 10, 27, 3, 30, 0), 10800),
                    (datetime(2013, 10, 27, 3, 0, 0), 7200),
                    (datetime(2013, 10, 27, 3, 30, 0), 7200),
                    (datetime(2013, 10, 27, 4, 0, 0), 7200),
                    (datetime(2013, 10, 27, 4, 30, 0), 7200),
                ],
                [
                    (datetime(2013, 10, 27, 4, 30, 0), 7200),
                    (datetime(2013, 10, 27, 4, 0, 0), 7200),
                    (datetime(2013, 10, 27, 3, 30, 0), 7200),
                    (datetime(2013, 10, 27, 3, 0, 0), 7200),
                    (datetime(2013, 10, 27, 3, 30, 0), 10800),
                    (datetime(2014, 10, 27, 3, 0, 0), 10800),
                    (datetime(2013, 10, 27, 2, 30, 0), 10800),
                ],
            )
        ]
        grets = []
        for tz, start, end, rstart, rend in expected_schedules:
            for i, expected in (start, rstart), (end, rend):
                rets = []
                ct = croniter("*/30 * * * *", self.tz_localize(i, tz))
                rets.append([
                    (
                        (ct.get_next if i == start else ct.get_prev)(datetime).isoformat(),
                        ct.get_current()
                    )
                    for j in range(len(list(expected)))
                ])
                grets.append((expected, rets))

    def testTimezoneSummerTime(self):
        tz = self.tz("Europe/Athens")

        expected_schedule = [
            (datetime(2013, 3, 31, 1, 30, 0), 7200),
            (datetime(2013, 3, 31, 2, 0, 0), 7200),
            (datetime(2013, 3, 31, 2, 30, 0), 7200),
            (datetime(2013, 3, 31, 4, 0, 0), 10800),
            (datetime(2013, 3, 31, 4, 30, 0), 10800),
        ]

        start = datetime(2013, 3, 31, 1, 0, 0)
        ct = croniter("*/30 * * * *", self.tz_localize(start, tz))
        self.assertScheduleTimezone(lambda: ct.get_next(datetime), expected_schedule)

        start = datetime(2013, 3, 31, 5, 0, 0)
        ct = croniter("*/30 * * * *", self.tz_localize(start, tz))
        self.assertScheduleTimezone(lambda: ct.get_prev(datetime), reversed(expected_schedule))

    def test_timestamp_timezone_is_respected_around_dst(self):
        cron = croniter('* * * * *')
        tz = 'US/Eastern'  # US/Eastern: 2020/03/08: 02:00-5 EST > 03:00-4 EDT +1H
        dt1 = datetime(2020, 3, 8, 1, 0)
        dt2 = datetime(2020, 3, 8, 4, 0)
        dst1 = self.tz_localize(dt1, tz)
        dst2 = self.tz_localize(dt2, tz)
        ts1 = cron.datetime_to_timestamp(dst1)
        ts2 = cron.datetime_to_timestamp(dst2)
        rets = [
            cron.timestamp_to_datetime(ts1, tzinfo=dst1.tzinfo).isoformat(),
            cron.timestamp_to_datetime(ts1, tzinfo=dst2.tzinfo).isoformat(),
            cron.timestamp_to_datetime(ts2, tzinfo=dst1.tzinfo).isoformat(),
            cron.timestamp_to_datetime(ts2, tzinfo=dst2.tzinfo).isoformat(),
        ]
        self.assertEqual(
            rets,
            [
                '2020-03-08T01:00:00-05:00',
                '2020-03-08T01:00:00-05:00',
                '2020-03-08T04:00:00-04:00',
                '2020-03-08T04:00:00-04:00',
            ]
        )

    def test_search_dst_bounds(self):
        # test DST bounds
        tests = [
            # fmt: off
            (
                "US/Eastern",
                datetime(2020, 3, 8, 2, 0),  # US/Eastern: 2020/03/08 02:00-5 EST > 03:00-4 EDT+1H
                ['2020-03-08T03:00:00-04:00', 1583650800, '2020-03-08T04:00:00-04:00', 1583654400, 3600.0],
                datetime(2020, 11, 1, 1, 0),  # US/Eastern: 2020/03/08 02:00-4 EDT > 01:00-5 EST-1H
                ['2020-11-01T01:00:00-05:00', 1604210400, '2020-11-01T02:00:00-05:00', 1604214000, -3600.0],
            ),
            (
                "America/Sao_Paulo",
                datetime(2018, 2, 18, 0, 0, 0),  # America/Sao_Paulo: 18/02/2018 00:00-2 AMT > 17/02/2018 23:00-3 BRT-1H
                ['2018-02-17T23:00:00-03:00', 1518919200, '2018-02-18T00:00:00-03:00', 1518922800, -3600.0],
                datetime(2018, 11, 4, 0, 0, 0),  # America/Sao_Paulo: 03/11/2018 00:00-3 BRT > 03/11/2018 01:00-2 AMT+1H
                ['2018-11-04T01:00:00-02:00', 1541300400, '2018-11-04T02:00:00-02:00', 1541304000, 3600.0],
            ),
            (
                "Europe/Warsaw",
                datetime(2017, 3, 26, 2, 0),   # Europe/Warsaw: 2017/03/26 02:00+1 CET  > 03:00+2 CEST +1H
                ['2017-03-26T03:00:00+02:00', 1490490000, '2017-03-26T04:00:00+02:00', 1490493600, 3600.0],
                datetime(2017, 10, 29, 2, 0),  # Europe/Warsaw: 2017/10/29 03:00+2 CEST > 02:00+1 CET  -1H
                ['2017-10-29T02:00:00+01:00', 1509238800, '2017-10-29T03:00:00+01:00', 1509242400, -3600.0],
            ),
            # fmt: on
        ]
        cron = croniter('0 0 * * *')
        for tzname, dst, test_dst, std, test_std in tests:
            tz = self.tz(tzname)
            for d, test in ((dst, test_dst), (std, test_std)):
                rets = []
                ts = cron.datetime_to_timestamp(self.tz_localize(d, tzname))
                # verify that result is not tempered by being inside or near DST window
                for i in range(0, 300 + 1, 30):
                    for sign in (1, -1):
                        if sign == -1 and not i:
                            continue
                        its = ts + i * sign
                        ldst = self.as_tz(datetime.fromtimestamp(its), tz)
                        rets.append([
                            b.isoformat() if isinstance(b, datetime) else b
                            for b in cron.search_dst_bounds(ldst)
                        ])
                        for r in rets:
                            if not r:
                                raise Exception("Here in WIP")

                for ret in rets:
                    self.assertEqual(ret, test)

        # test limit cases
        self.assertRaises(CroniterError, cron.search_dst_bounds, dst.replace(tzinfo=None))
        self.assertRaises(CroniterError, cron.search_dst_bounds, None)
        self.assertRaises(CroniterError, cron.search_dst_bounds, (None, None))
        self.assertRaises(CroniterError, cron.search_dst_bounds, (1, None))
        self.assertRaises(CroniterError, cron.search_dst_bounds, (None, 1))

    def test_get_surrounding_months(self):
        tz = self.tz('Europe/Paris')
        tests = [
            (
                datetime(2021, 3, 1, tzinfo=tz),
                (datetime(2021, 2, 1, tzinfo=tz), datetime(2021, 4, 30, tzinfo=tz)),
            ),
            (
                datetime(2021, 5, 31, tzinfo=tz),
                (datetime(2021, 4, 1, tzinfo=tz), datetime(2021, 6, 30, tzinfo=tz)),
            ),
            (
                datetime(2021, 1, 31, tzinfo=tz),
                (datetime(2020, 12, 1, tzinfo=tz), datetime(2021, 2, 28, tzinfo=tz)),
            ),
            (
                datetime(2021, 1, 15, tzinfo=tz),
                (datetime(2020, 12, 1, tzinfo=tz), datetime(2021, 2, 28, tzinfo=tz)),
            ),
            (
                datetime(2021, 12, 15, tzinfo=tz),
                (datetime(2021, 11, 1, tzinfo=tz), datetime(2022, 1, 31, tzinfo=tz)),
            ),
        ]
        rets = []
        for t, ret in tests:
            rets.append(cron_m.get_surrounding_months(t))
        self.assertEqual([a[1] for a in tests], rets)

    def test_std_dst2(self):
        """
        DST tests

        This fixes:
        - https://github.com/taichino/croniter/issues/87
        - https://github.com/taichino/croniter/issues/90
        - https://github.com/kiorky/croniter/issues/1
        - https://github.com/taichino/croniter/issues/82

        """
        tests = [
            # America/Sao_Paulo: 18/02/2018 00:00 (UTC-2) -> 17/02/2018 23:00 (UTC-3) BACKWARD 1H
            (
                "America/Sao_Paulo",
                datetime(2018, 2, 18, 0, 0),
                "2018-02-17T23:00:00-02:00",
            ),
            (
                "America/Sao_Paulo",
                datetime(2018, 2, 18, 0, 5),
                "2018-02-18T00:05:00-03:00",
            ),
            # Europe/Warsaw: 2017/03/26 02:00 (UTC+1) -> 2017/03/26 03:00 (UTC+2) ONWARD 1H
            (
                "Europe/Warsaw",
                datetime(2017, 3, 26, 2, 0),
                "2017-03-26T04:00:00+02:00",
            ),
            (
                "Europe/Warsaw",
                datetime(2017, 3, 26, 2, 5),
                "2017-03-26T04:05:00+02:00",
            ),
            # Australia/Adelaide: 05/04/2020 03:00 (UTC+10h30) -> 05/04/2020 02:00 (UTC+9h30) BACKWARDS 1H
            (
                "Australia/Adelaide",
                datetime(2020, 4, 5, 3, 0),
                "2020-04-05T02:00:00+10:30",
            ),
            (
                "Australia/Adelaide",
                datetime(2020, 4, 5, 3, 5),
                "2020-04-05T03:05:00+09:30",
            ),
        ]
        rets = []
        td = timedelta(minutes=30)
        for tzname, dt, wanted in tests:
            cron = croniter("0 * * * *".replace("0", str(dt.minute)))
            tz = self.tz(tzname)
            dst = self.tz_localize(dt, tz)
            pt = cron.get_prev(datetime, start_time=dst + td).isoformat()
            nt = cron.get_next(datetime, start_time=dst - td).isoformat()
            rets.append((dst.isoformat(), wanted, nt, pt))
        for dst, w, nt, pt in rets:
            self.assertEqual(w, nt, "test failed '{0}' expected '{1}'!='{2}'".format(dst, w, nt))
            self.assertEqual(w, pt, "test failed '{0}' expected '{1}'!='{2}'".format(dst, w, pt))

    def test_std_dst3(self):
        """
        DST tests

        This fixes:
        - https://github.com/taichino/croniter/issues/87
        - https://github.com/taichino/croniter/issues/90
        - https://github.com/kiorky/croniter/issues/1
        - https://github.com/taichino/croniter/issues/82

        """
        tests = [
            # -2: 01 00 23 22 21
            # -3: 00 23 22 21 20
            # America/Sao_Paulo: 18/02/2018 00:00 (UTC-2) -> 17/02/2018 23:00 (UTC-3) BACKWARD 1H
            (
                "America/Sao_Paulo",
                datetime(2018, 2, 18, 0, 0),
                ["2018-02-17T23:59:00-02:00"],
            ),
            # Europe/Warsaw: 2017/03/26 02:00 (UTC+1) -> 2017/03/26 03:00 (UTC+2) ONWARD 1H
            (
                "Europe/Warsaw",
                datetime(2017, 3, 26, 2, 0),
                ["2017-03-26T04:01:00+02:00"],
            ),
            (
                "Asia/Hebron",
                datetime(2022, 3, 26, 0, 0, 0),
                [],
            ),
        ]
        grets = {}
        td = timedelta(minutes=30)
        for tzname, dt, wanted in tests:
            tz = self.tz(tzname)
            rets = grets.setdefault(tzname, [])
            rets.append(self.tz_localize(dt, tz).isoformat())
            rets.append(wanted)
            for minute in (0, 5,):
                for m, sign in (
                    ("get_next", -1),
                    ("get_prev", 1),
                ):
                    dst = dt.replace(minute=minute, tzinfo=tz) + td * 6 * sign
                    cron = croniter("0 * * * *".replace("0", str(dst.minute)), start_time=dst)
                    irets = []
                    for i in range(10):
                        ret = getattr(cron, m)(datetime)
                        irets.append((cron.timestamp_to_datetime(dst.timestamp(), tzinfo=None).isoformat(),
                                      ret.isoformat()))
                        dst = ret
                    rets.append(irets)

    def test_dst_issue90_st31ny(self):
        tz = self.tz("Europe/Paris")
        now = datetime(2020, 3, 29, 1, 59, 55, tzinfo=tz)
        it = croniter("1 2 * * *", now)
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
        self.assertEqual(
            ret,
            [
                "2020-03-30T02:01:00+02:00",
                "2020-03-29T01:01:00+01:00",
                "2020-03-28T03:01:00+01:00",
                "2020-03-29T03:01:00+02:00",
                "2020-03-30T02:01:00+02:00",
            ],
        )
        #
        nowp = datetime(2020, 3, 28, 1, 58, 55, tzinfo=tz)
        itp = croniter("1 2 * * *", nowp)
        retp = [
            itp.get_next(datetime).isoformat(),
            itp.get_prev(datetime).isoformat(),
            itp.get_prev(datetime).isoformat(),
            itp.get_next(datetime).isoformat(),
            itp.get_next(datetime).isoformat(),
        ]
        self.assertEqual(
            retp,
            [
                "2020-03-29T03:01:00+02:00",
                "2020-03-29T01:01:00+01:00",
                "2020-03-28T03:01:00+01:00",
                "2020-03-29T03:01:00+02:00",
                "2020-03-30T02:01:00+02:00",
            ],
        )
        #
        nowt = datetime(2020, 3, 29, 2, 0, 0, tzinfo=tz)
        itt = croniter("1 2 * * *", nowt)
        rett = [
            itt.get_next(datetime).isoformat(),
            itt.get_prev(datetime).isoformat(),
            itt.get_prev(datetime).isoformat(),
            itt.get_next(datetime).isoformat(),
            itt.get_next(datetime).isoformat(),
        ]
        self.assertEqual(
            rett,
            [
                "2020-03-30T02:01:00+02:00",
                "2020-03-29T01:01:00+01:00",
                "2020-03-28T03:01:00+01:00",
                "2020-03-29T03:01:00+02:00",
                "2020-03-30T02:01:00+02:00",
            ],
        )

    def test_issue_k11(self):
        now = self.tz_localize(datetime(2019, 1, 14, 11, 0, 59), "America/New_York")
        nextnow = croniter("* * * * * ").next(datetime, start_time=now)
        nextnow2 = croniter("* * * * * ", now).next(datetime)
        for nt in nextnow, nextnow2:
            self.assertTrue("america" in get_tz_id(nt.tzinfo).lower())
            self.assertEqual(int(croniter._datetime_to_timestamp(nt)), 1547481660)

    def test_issue_k12(self):
        tz = self.tz("Europe/Athens")
        base = datetime(2010, 1, 23, 12, 18, tzinfo=tz)
        itr = croniter("* * * * *")
        itr.set_current(start_time=base)

        n1 = itr.get_next()  # 19

        self.assertEqual(n1, datetime_to_timestamp(base) + 60)


class CroniterDST138Test(base.TestCase):
    """
    See https://github.com/kiorky/croniter/issues/138.
    """
    _tz = 'UTC'

    def setUp(self):
        self._time = os.environ.setdefault("TZ", "")
        self.base = datetime(2024, 1, 25, 4, 46)
        self.iter = croniter("*/5 * * * *", self.base)
        self.results = [
            datetime(2024, 1, 25, 4, 50),
            datetime(2024, 1, 25, 4, 55),
            datetime(2024, 1, 25, 5, 0),
        ]
        self.tzname, self.timezone = time.tzname, time.timezone

    def tearDown(self):
        cron_m.OVERFLOW32B_MODE = ORIG_OVERFLOW32B_MODE
        if not self._time:
            del os.environ["TZ"]
        else:
            os.environ["TZ"] = self._time
        time.tzset()

    def test_issue_138_dt_to_ts_32b(self):
        """
        test local tz, forcing 32b mode.
        """
        self._test(m32b=True)

    def test_issue_138_dt_to_ts_n(self):
        """
        test local tz, forcing non 32b mode.
        """
        self._test(m32b=False)

    def _test(self, tz='UTC', m32b=True):
        cron_m.OVERFLOW32B_MODE = m32b
        os.environ["TZ"] = tz
        time.tzset()
        res = [self.iter.get_next(datetime) for i in range(3)]
        self.assertEqual(res, self.results)


class CroniterDST138TestLocal(CroniterDST138Test):
    _tz = 'UTC-8'


if __name__ == "__main__":
    unittest.main()
