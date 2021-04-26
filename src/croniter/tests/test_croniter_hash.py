from datetime import datetime, timedelta

from croniter import croniter, CroniterNotAlphaError, CroniterBadCronError
from croniter.tests import base


class CroniterHashBase(base.TestCase):
    epoch = datetime(2020, 1, 1, 0, 0)
    hash_id = 'hello'

    def _test_iter(
        self, definition, expectations, delta, epoch=None, hash_id=None, next_type=None
    ):
        if epoch is None:
            epoch = self.epoch
        if hash_id is None:
            hash_id = self.hash_id
        if next_type is None:
            next_type = datetime
        if not isinstance(expectations, (list, tuple)):
            expectations = (expectations,)
        obj = croniter(definition, epoch, hash_id=hash_id)
        testval = obj.get_next(next_type)
        self.assertIn(testval, expectations)
        if delta is not None:
            self.assertEqual(obj.get_next(next_type), testval + delta)


class CroniterHashTest(CroniterHashBase):
    def test_hash_hourly(self):
        """Test manually-defined hourly"""
        self._test_iter('H * * * *', datetime(2020, 1, 1, 0, 10), timedelta(hours=1))

    def test_hash_daily(self):
        """Test manually-defined daily"""
        self._test_iter('H H * * *', datetime(2020, 1, 1, 11, 10), timedelta(days=1))

    def test_hash_weekly(self):
        """Test manually-defined weekly"""
        # croniter 1.0.5 changes the defined weekly range from (0, 6)
        # to (0, 7), to match cron's behavior that Sunday is 0 or 7.
        # This changes the hash, so test for either.
        self._test_iter(
            'H H * * H',
            (datetime(2020, 1, 3, 11, 10), datetime(2020, 1, 5, 11, 10)),
            timedelta(weeks=1),
        )

    def test_hash_monthly(self):
        """Test manually-defined monthly"""
        self._test_iter('H H H * *', datetime(2020, 1, 1, 11, 10), timedelta(days=31))

    def test_hash_yearly(self):
        """Test manually-defined yearly"""
        self._test_iter('H H H H *', datetime(2020, 9, 1, 11, 10), timedelta(days=365))

    def test_hash_second(self):
        """Test seconds

        If a sixth field is provided, seconds are included in the datetime()
        """
        self._test_iter(
            'H H * * * H', datetime(2020, 1, 1, 11, 10, 32), timedelta(days=1)
        )

    def test_hash_id_change(self):
        """Test a different hash_id returns different results given same definition and epoch"""
        self._test_iter('H H * * *', datetime(2020, 1, 1, 11, 10), timedelta(days=1))
        self._test_iter(
            'H H * * *',
            datetime(2020, 1, 1, 0, 24),
            timedelta(days=1),
            hash_id='different id',
        )

    def test_hash_epoch_change(self):
        """Test a different epoch returns different results given same definition and hash_id"""
        self._test_iter('H H * * *', datetime(2020, 1, 1, 11, 10), timedelta(days=1))
        self._test_iter(
            'H H * * *',
            datetime(2011, 11, 12, 11, 10),
            timedelta(days=1),
            epoch=datetime(2011, 11, 11, 11, 11),
        )

    def test_hash_range(self):
        """Test a hashed range definition"""
        self._test_iter(
            'H H H(3-5) * *', datetime(2020, 1, 5, 11, 10), timedelta(days=31)
        )

    def test_hash_division(self):
        """Test a hashed division definition"""
        self._test_iter('H H/3 * * *', datetime(2020, 1, 1, 3, 10), timedelta(hours=3))

    def test_hash_range_division(self):
        """Test a hashed range + division definition"""
        self._test_iter(
            'H(30-59)/10 H * * *', datetime(2020, 1, 1, 11, 31), timedelta(minutes=10)
        )

    def test_hash_id_bytes(self):
        """Test hash_id as a bytes object"""
        self._test_iter(
            'H H * * *',
            datetime(2020, 1, 1, 14, 53),
            timedelta(days=1),
            hash_id=b'\x01\x02\x03\x04',
        )

    def test_hash_float(self):
        """Test result as a float object"""
        self._test_iter('H H * * *', 1577877000.0, (60 * 60 * 24), next_type=float)

    def test_invalid_definition(self):
        """Test an invalid defition raises CroniterNotAlphaError"""
        with self.assertRaises(CroniterNotAlphaError):
            croniter('X X * * *', self.epoch, hash_id=self.hash_id)

    def test_invalid_hash_id_type(self):
        """Test an invalid hash_id type raises TypeError"""
        with self.assertRaises(TypeError):
            croniter('H H * * *', self.epoch, hash_id={1: 2})

    def test_invalid_divisor(self):
        """Test an invalid divisor type raises CroniterBadCronError"""
        with self.assertRaises(CroniterBadCronError):
            croniter('* * H/0 * *', self.epoch, hash_id=self.hash_id)


class CroniterWordAliasTest(CroniterHashBase):
    def test_hash_word_midnight(self):
        """Test built-in @midnight

        @midnight is actually up to 3 hours after midnight, not exactly midnight
        """
        self._test_iter('@midnight', datetime(2020, 1, 1, 2, 10, 32), timedelta(days=1))

    def test_hash_word_hourly(self):
        """Test built-in @hourly"""
        self._test_iter('@hourly', datetime(2020, 1, 1, 0, 10, 32), timedelta(hours=1))

    def test_hash_word_daily(self):
        """Test built-in @daily"""
        self._test_iter('@daily', datetime(2020, 1, 1, 11, 10, 32), timedelta(days=1))

    def test_hash_word_weekly(self):
        """Test built-in @weekly"""
        # croniter 1.0.5 changes the defined weekly range from (0, 6)
        # to (0, 7), to match cron's behavior that Sunday is 0 or 7.
        # This changes the hash, so test for either.
        self._test_iter(
            '@weekly',
            (datetime(2020, 1, 3, 11, 10, 32), datetime(2020, 1, 5, 11, 10, 32)),
            timedelta(weeks=1),
        )

    def test_hash_word_monthly(self):
        """Test built-in @monthly"""
        self._test_iter(
            '@monthly', datetime(2020, 1, 1, 11, 10, 32), timedelta(days=31)
        )

    def test_hash_word_yearly(self):
        """Test built-in @yearly"""
        self._test_iter(
            '@yearly', datetime(2020, 9, 1, 11, 10, 32), timedelta(days=365)
        )

    def test_hash_word_annually(self):
        """Test built-in @annually

        @annually is the same as @yearly
        """
        obj_annually = croniter('@annually', self.epoch, hash_id=self.hash_id)
        obj_yearly = croniter('@yearly', self.epoch, hash_id=self.hash_id)
        self.assertEqual(obj_annually.get_next(datetime), obj_yearly.get_next(datetime))
        self.assertEqual(obj_annually.get_next(datetime), obj_yearly.get_next(datetime))
