"""
Примеры:
pytest lesson7/task4/test_01.py::TestRunAddoption::test_common --url="https://ya.ru" --status_code=200
pytest lesson7/task4/test_01.py::TestRunAddoption::test_common --url="https://ya.ru/sfh" --status_code=404
"""

import requests


class TestRunAddoption:

    def test_common(self, url, status_code):
        r = requests.request('get', url)
        assert r.status_code == status_code, 'Wrong status code'


if __name__ == '__main__':
    pass
