import runpy
import unittest
from unittest import mock

import mintotp

SECRET1 = 'ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS'
SECRET2 = 'PW4YAYYZVDE5RK2AOLKUATNZIKAFQLZO'


class Test(unittest.TestCase):
    def test_hotp(self):
        self.assertEqual(mintotp.hotp(SECRET1, 0), '549419')
        self.assertEqual(mintotp.hotp(SECRET2, 0), '009551')
        self.assertEqual(mintotp.hotp(SECRET1, 42), '626854')
        self.assertEqual(mintotp.hotp(SECRET2, 42), '093610')

    def test_totp(self):
        with mock.patch('time.time', return_value=0):
            self.assertEqual(mintotp.totp(SECRET1), '549419')
            self.assertEqual(mintotp.totp(SECRET2), '009551')
        with mock.patch('time.time', return_value=10):
            self.assertEqual(mintotp.totp(SECRET1), '549419')
            self.assertEqual(mintotp.totp(SECRET2), '009551')
        with mock.patch('time.time', return_value=1260):
            self.assertEqual(mintotp.totp(SECRET1), '626854')
            self.assertEqual(mintotp.totp(SECRET2), '093610')
        with mock.patch('time.time', return_value=1270):
            self.assertEqual(mintotp.totp(SECRET1), '626854')
            self.assertEqual(mintotp.totp(SECRET2), '093610')

    def test_main(self):
        with mock.patch('sys.stdin', [SECRET1]):
            with mock.patch('time.time', return_value=0):
                with mock.patch('builtins.print') as mock_print:
                    mintotp.main()
                    mock_print.assert_called_once_with('549419')
        with mock.patch('sys.stdin', [SECRET1, SECRET2]):
            with mock.patch('time.time', return_value=0):
                with mock.patch('builtins.print') as mock_print:
                    mintotp.main()
                    self.assertEqual(mock_print.mock_calls,
                                     [mock.call('549419'),
                                      mock.call('009551')])

    def test_name(self):
        with mock.patch('sys.stdin', [SECRET1]):
            with mock.patch('time.time', return_value=0):
                with mock.patch('builtins.print') as mock_print:
                    runpy.run_module('mintotp', run_name='mintotp')
                    mock_print.assert_not_called()
                    runpy.run_module('mintotp', run_name='__main__')
                    mock_print.assert_called_once_with('549419')
