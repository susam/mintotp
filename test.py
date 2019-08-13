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

    @mock.patch('time.time', mock.Mock(return_value=0))
    @mock.patch('sys.argv', ['prog'])
    @mock.patch('sys.stdin', [SECRET1])
    @mock.patch('builtins.print')
    def test_main_one_secret(self, mock_print):
        mintotp.main()
        mock_print.assert_called_once_with('549419')

    @mock.patch('time.time', mock.Mock(return_value=0))
    @mock.patch('sys.argv', ['prog'])
    @mock.patch('sys.stdin', [SECRET1, SECRET2])
    @mock.patch('builtins.print')
    def test_main_two_secrets(self, mock_print):
        mintotp.main()
        self.assertEqual(mock_print.mock_calls, [mock.call('549419'),
                                                 mock.call('009551')])

    @mock.patch('time.time', mock.Mock(return_value=2520))
    @mock.patch('sys.argv', ['prog', '60'])
    @mock.patch('sys.stdin', [SECRET1])
    @mock.patch('builtins.print')
    def test_main_step(self, mock_print):
        mintotp.main()
        mock_print.assert_called_once_with('626854')

    @mock.patch('time.time', mock.Mock(return_value=0))
    @mock.patch('sys.argv', ['prog', '30', '8'])
    @mock.patch('sys.stdin', [SECRET1])
    @mock.patch('builtins.print')
    def test_main_digits(self, mock_print):
        mintotp.main()
        mock_print.assert_called_once_with('49549419')

    @mock.patch('time.time', mock.Mock(return_value=0))
    @mock.patch('sys.argv', ['prog', '30', '6', 'sha256'])
    @mock.patch('sys.stdin', [SECRET1])
    @mock.patch('builtins.print')
    def test_main_digest(self, mock_print):
        mintotp.main()
        mock_print.assert_called_once_with('473535')

    @mock.patch('time.time', mock.Mock(return_value=0))
    @mock.patch('sys.argv', ['prog'])
    @mock.patch('sys.stdin', [SECRET1])
    @mock.patch('builtins.print')
    def test_module(self, mock_print):
        runpy.run_module('mintotp', run_name='mintotp')
        mock_print.assert_not_called()
        runpy.run_module('mintotp', run_name='__main__')
        mock_print.assert_called_once_with('549419')
