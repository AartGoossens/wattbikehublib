from unittest import TestCase

from wattbikehublib.utils import username_parser


class TestUsernameParser(TestCase):
    def test_correct(self):
        username = username_parser('http://hub.wattbike.com/aart.goossens')
        self.assertEqual('aart.goossens', username)

    def test_invalid_url(self):
        username = username_parser('http://example.com/aart.goossens')
        self.assertEqual(None, username)

    def test_username_with_digit(self):
        username = username_parser('http://hub.wattbike.com/aart.goossens01')
        self.assertEqual('aart.goossens01', username)

    def test_username_without_period(self):
        username = username_parser('http://hub.wattbike.com/aartgoossens')
        self.assertEqual('aartgoossens', username)

    def test_username_with_underscore(self):
        username = username_parser('http://hub.wattbike.com/aart_goossens')
        self.assertEqual(None, username)
