import csv
import json
from typing import Iterable

from lesson5.data_unit import RezJSONUser


class RW:

    def __init__(self, path: str, encoding: str = 'utf8'):
        self.path = path
        self.encoding = encoding
        self.data = None

    def read(self):
        with open(self.path, 'r', encoding=self.encoding) as f:
            self.data = self._read_inner(f)
        return self

    def write(self):
        with open(self.path, 'w', encoding=self.encoding) as f:
            self._write_inner(f, self.data)
        return self

    def _read_inner(self, file) -> Iterable:
        pass

    def _write_inner(self, file, data: Iterable):
        pass

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


class CSVBooks(RW):

    def __init__(self):
        super().__init__('books.csv')

    def _read_inner(self, file):
        return tuple(csv.DictReader(file, delimiter=','))


class JSONUsers(RW):

    def __init__(self):
        super().__init__('users.json')

    def _read_inner(self, file) -> Iterable:
        return json.load(file)


class RezJSONUsers(RW):

    def __init__(self):
        super().__init__('result.json')
        self.data = []

    def _write_inner(self, file, data: Iterable):
        json.dump(data, file, indent=4)

    def __iadd__(self, user: RezJSONUser):
        self.data.append(user.data)
        return self

