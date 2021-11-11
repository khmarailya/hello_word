import csv
import json
from typing import Iterable
import urllib.request

from lesson5.data_unit import RezJSONUser


class RW:

    def __init__(self, path: str, encoding: str = 'utf8', url: str = None):
        self.path = path
        self.encoding = encoding
        self.data = None
        self.url = url

    def read(self):
        if self.url:
            with urllib.request.urlopen(self.url) as f:
                self.data = self._read_inner(f)
        else:
            with open(self.path, 'r', encoding=self.encoding) as f:
                self.data = self._read_inner(f)

        return self

    def write(self):
        with open(self.path, 'w', encoding=self.encoding) as f:
            self._write_inner(f, self.data)
        return self

    def _read_inner(self, data) -> Iterable:
        pass

    def _write_inner(self, file, data: Iterable):
        pass

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


class CSVBooks(RW):

    def __init__(self):
        super().__init__(
            'books.csv',
            url='https://raw.githubusercontent.com/konflic/front_example/master/data/books.csv'
        )

    def _read_inner(self, data):
        if self.url:
            r: bytes = data.read()
            data = r.decode(self.encoding).strip().split('\n')

        return tuple(csv.DictReader(data, delimiter=','))


class JSONUsers(RW):

    def __init__(self):
        super().__init__(
            'users.json',
            url='https://raw.githubusercontent.com/konflic/front_example/master/data/users.json'
        )

    def _read_inner(self, data) -> Iterable:
        if self.url:
            return json.loads(data.read())
        else:
            return json.load(data)


class RezJSONUsers(RW):

    def __init__(self):
        super().__init__('result.json')
        self.data = []

    def _write_inner(self, file, data: Iterable):
        json.dump(data, file, indent=4)

    def __iadd__(self, user: RezJSONUser):
        self.data.append(user.data)
        return self

