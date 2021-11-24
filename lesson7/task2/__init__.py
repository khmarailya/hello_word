import random
from typing import List

import requests


class URL:
    main = 'https://api.openbrewerydb.org'
    examples = f'{main}/breweries'

    @classmethod
    def by_city(cls, city: str) -> str:
        return f'{cls.examples}?by_city={city}'

    @classmethod
    def by_dist(cls, longitude: str, latitude: str) -> str:
        return f'{cls.examples}?by_dist={longitude},{latitude}'

    @classmethod
    def by_type(cls, type_: str) -> str:
        return f'{cls.examples}?by_type={type_}'


class Response:

    @classmethod
    def examples(cls) -> requests.Response:
        return requests.request('get', URL.examples)

    @classmethod
    def by_city(cls, city: str) -> requests.Response:
        return requests.request('get', URL.by_city(city))

    @classmethod
    def by_dist(cls, longitude: str, latitude: str) -> requests.Response:
        return requests.request('get', URL.by_dist(longitude, latitude))

    @classmethod
    def by_type(cls, type_: str) -> requests.Response:
        return requests.request('get', URL.by_type(type_))


class Utils:

    @classmethod
    def normalize(cls, s: str):
        return s.replace(' ', '_')

    @classmethod
    def mark_choice(cls, json: List[dict], *keys) -> dict:
        if len(keys) > 1:
            def map_(x):
                return tuple(x.get(key) for key in keys)
        else:
            key = keys[0]

            def map_(x):
                return x.get(key)

        choices = set(map(map_, json))
        return dict(zip(choices, [False] * len(choices)))

    @classmethod
    def choice(cls, choices: dict, with_re_choice=True):
        not_choices = list(filter(lambda x: not choices.get(x), choices))
        res = None
        if not_choices:
            res = random.choice(not_choices)
            choices[res] = True

        if not res and with_re_choice:
            for key in choices:
                choices[key] = False
            res = cls.choice(choices, with_re_choice=False)

        return res

    @classmethod
    def calc_dist(cls, longitude, latitude, longitude2, latitude2):
        longitude, latitude = float(longitude), float(latitude)
        longitude2, latitude2 = float(longitude2), float(latitude2)
        res = ((longitude - longitude2) ** 2 + (latitude - latitude2) ** 2) ** .5
        return res
