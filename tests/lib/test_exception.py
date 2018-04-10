# file: test_exception.py
# author: mbiokyle29
import unittest

from place.lib.exception import PlaceException


class TestPlaceException(unittest.TestCase):

    def test_raise(self):
        with self.assertRaises(PlaceException):
            raise PlaceException("BAD")
