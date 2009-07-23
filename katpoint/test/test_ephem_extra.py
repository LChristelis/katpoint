"""Tests for the ephem_extra module."""
# pylint: disable-msg=C0103,W0212

import unittest

import ephem

from katpoint.ephem_extra import Timestamp

class TestTimestamp(unittest.TestCase):
    """Test timestamp creation and conversion."""
    def setUp(self):
        self.valid_timestamps = [(1248186982.3980861, '2009-07-21 14:36:22.398'),
                                 (ephem.Date('2009/07/21 02:52:12.34'), '2009-07-21 02:52:12.340'),
                                 (0, '1970-01-01 00:00:00'),
                                 (-10, '1969-12-31 23:59:50'),
                                 ('2009-07-21 02:52:12.034', '2009-07-21 02:52:12.034'),
                                 ('2009-07-21 02:52:12.000', '2009-07-21 02:52:12'),
                                 ('2009-07-21 02:52:12', '2009-07-21 02:52:12'),
                                 ('2009-07-21 02:52', '2009-07-21 02:52:00'),
                                 ('2009-07-21 02', '2009-07-21 02:00:00'),
                                 ('2009-07-21', '2009-07-21 00:00:00'),
                                 ('2009-07', '2009-07-01 00:00:00'),
                                 ('2009', '2009-01-01 00:00:00'),
                                 ('2009/07/21 02:52:12.034', '2009-07-21 02:52:12.034'),
                                 ('2009/07/21 02:52:12.000', '2009-07-21 02:52:12'),
                                 ('2009/07/21 02:52:12', '2009-07-21 02:52:12'),
                                 ('2009/07/21 02:52', '2009-07-21 02:52:00'),
                                 ('2009/07/21 02', '2009-07-21 02:00:00'),
                                 ('2009/07/21', '2009-07-21 00:00:00'),
                                 ('2009/07', '2009-07-01 00:00:00'),
                                 ('2009', '2009-01-01 00:00:00'),
                                 ('2019-07-21 02:52:12', '2019-07-21 02:52:12')]
        self.invalid_timestamps = ['gielie', '03 Mar 2003']
        self.overflow_timestamps = ['2049-07-21 02:52:12']
    
    def test_construct_timestamp(self):
        """Test construction of timestamps."""
        for v, s in self.valid_timestamps:
            t = Timestamp(v)
            self.assertEqual(str(t), s, "Timestamp string ('%s') differs from expected one ('%s')" % (str(t), s))
        for v in self.invalid_timestamps:
            self.assertRaises(ValueError, Timestamp, v)
#        for v in self.overflow_timestamps:
#            self.assertRaises(OverflowError, Timestamp, v)
    
    def test_numerical_timestamp(self):
        """Test numerical properties of timestamps."""
        t = Timestamp(self.valid_timestamps[0][0])
        self.assertEqual(t, t + 0.0)
        self.assertNotEqual(t, t + 1.0)
        self.assertTrue(t > t - 1.0)
        self.assertTrue(t < t + 1.0)
        self.assertEqual(t, eval(repr(t)))
        self.assertEqual(float(t), self.valid_timestamps[0][0])
        t = Timestamp(self.valid_timestamps[1][0])
        self.assertAlmostEqual(t.to_ephem_date(), self.valid_timestamps[1][0], places=9)
        