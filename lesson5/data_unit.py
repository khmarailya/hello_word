from typing import List


class DataUnit:

    def __init__(self, data: dict = None):
        self._data = data or {}

    @property
    def data(self) -> dict:
        return self._data

    def __str__(self):
        return '; '.join(f'{key}: "{val}"' for key, val in self._data.items() if val)

    @staticmethod
    def _d_property(key, default=None):

        def getter(self: DataUnit):
            if key in self._data:
                res = self._data[key]
            else:
                res = default() if callable(default) else default
                self._data[key] = res

            return res

        def setter(self: DataUnit, val):
            self._data[key] = val

        return property(fget=getter, fset=setter)


class CSVBook(DataUnit):
    d_author: str = DataUnit._d_property('Author', '')
    d_title: str = DataUnit._d_property('Title', '')
    d_genre: str = DataUnit._d_property('Genre', '')
    d_pages: str = DataUnit._d_property('Pages', '')
    d_publisher: str = DataUnit._d_property('Publisher', '')


class RezJSONBook(DataUnit):
    d_title: str = DataUnit._d_property('title', '')
    d_author: str = DataUnit._d_property('author', '')
    d_pages: int = DataUnit._d_property('pages', 0)
    d_genre: str = DataUnit._d_property('genre', '')

    def from_book(self, book: CSVBook):
        self.d_author = book.d_author
        self.d_pages = int(book.d_pages)
        self.d_title = book.d_title
        self.d_genre = book.d_genre
        return self


class JSONUser(DataUnit):
    d_id: str = DataUnit._d_property('_id', '')
    d_index: int = DataUnit._d_property('index')
    d_guid: str = DataUnit._d_property('guid', '')
    d_is_active: bool = DataUnit._d_property('isActive', False)
    d_balance: str = DataUnit._d_property('balance', '')
    d_picture: str = DataUnit._d_property('picture', '')
    d_age: int = DataUnit._d_property('age', 0)
    d_eye_color: str = DataUnit._d_property('eyeColor', '')
    d_name: str = DataUnit._d_property('name', '')
    d_gender: str = DataUnit._d_property('gender', '')
    d_company: str = DataUnit._d_property('company', '')
    d_email: str = DataUnit._d_property('email', '')
    d_phone: str = DataUnit._d_property('phone', '')
    d_address: str = DataUnit._d_property('address', '')
    d_about: str = DataUnit._d_property('about', '')
    d_registered: str = DataUnit._d_property('registered', '')
    d_latitude: float = DataUnit._d_property('latitude', 0)
    d_longitude: float = DataUnit._d_property('longitude', 0)
    d_tags: List[str] = DataUnit._d_property('tags', list)
    d_friends: List[dict] = DataUnit._d_property('friends', list)


class RezJSONUser(DataUnit):
    d_name: str = DataUnit._d_property('name', '')
    d_gender: str = DataUnit._d_property('gender', '')
    d_address: str = DataUnit._d_property('address', '')
    d_age: int = DataUnit._d_property('age', 0)
    d_books: List[dict] = DataUnit._d_property('books', list)

    def from_user(self, user: JSONUser):
        self.d_name = user.d_name
        self.d_age = user.d_age
        self.d_address = user.d_address
        self.d_gender = user.d_gender
        self.d_name = user.d_name
        return self

    def __iadd__(self, book: RezJSONBook):
        self.d_books.append(book.data)
        return self

