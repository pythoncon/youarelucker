#!/usr/bin/python
import unittest
import logging
import os
import sys
_src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, _src_path)
from app import lucky
from app import static

UPLOAD_PATH = os.path.join(_src_path, '..', 'www', 'upload')

class AppTest(unittest.TestCase):
    def setUp(self):
        super(AppTest, self).setUp()
        self._clear_uploaded()
        self._mock_session()

    def _clear_uploaded(self):
        for file_name in os.listdir(UPLOAD_PATH):
            if not file_name.startswith('.'):
                os.remove(os.path.join(UPLOAD_PATH, file_name))

    def _mock_session(self):
        from bottle import request
        request.environ['beaker.session'] = {}

    def test_lucky_return_None_if_no_file(self):
        self.assertEqual(lucky(), None)

    def test_lucky_return_file_path_if_one_file(self):
        self._add_file('a.jpg')
        self.assertEqual(lucky(), 'upload/a.jpg')

    def test_lucky_return_different_result_on_different_request(self):
        self._add_file('a.jpg')
        self._add_file('b.jpg')
        _1st = lucky()
        _2nd = lucky()
        self.assertNotEqual(_1st, None)
        self.assertNotEqual(_2nd, None)
        self.assertNotEqual(_1st, _2nd)

    def test_lucky_return_None_if_no_more_file(self):
        self._add_file('a.jpg')
        self._add_file('b.jpg')
        lucky()
        lucky()
        self.assertEqual(lucky(), None)

    def test_static_interface_should_work(self):
        self._add_file('a.txt')
        response = static('upload/a.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_length, 0)

    def _add_file(self, file_name):
        with open(os.path.join(UPLOAD_PATH, file_name), 'w+b') as fp:
            fp.write('')


if __name__ == '__main__':
    FORMAT = "%(asctime)s %(levelname)6s %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%m%d%H%M%S', stream=sys.stdout)
    unittest.main()
