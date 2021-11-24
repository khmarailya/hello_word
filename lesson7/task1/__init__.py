import csv
import imghdr
import random
from typing import Tuple

import requests


class URL:
    main = 'https://dog.ceo'
    base = f'{main}/api'
    base_image = 'https://images.dog.ceo/breeds'
    all = f'{base}/breeds/list/all'
    random = f'{base}/breeds/image/random'

    @classmethod
    def random_count(cls, cnt: int) -> str:
        return f'{cls.random}/{cnt}'

    @classmethod
    def by_breed(cls, breed: str) -> str:
        return f'{cls.base}/breed/{breed}/images'

    @classmethod
    def by_breed_random(cls, breed: str) -> str:
        return f'{cls.by_breed(breed)}/random'

    @classmethod
    def by_breed_random_cnt(cls, breed: str, cnt: int) -> str:
        return f'{cls.by_breed_random(breed)}/{cnt}'


class Response:

    @classmethod
    def by_breed(cls, breed: str) -> requests.Response:
        return requests.request('get', URL.by_breed(breed))


class Utils:

    @classmethod
    def extract_names_jpg(cls, url: str, base_url: str) -> Tuple[str, str, str]:
        name, jpg = tuple(url[len(base_url) + 1:].split('/'))  # type: str
        names = tuple(name.split('-'))
        name = names[0]
        sub_name = names[1] if len(names) > 1 else ''
        return name, sub_name, jpg

    @classmethod
    def common_response_check(cls, r: requests.Response) -> dict:
        assert r.status_code == 200, 'Wrong status code'

        rec = r.json()
        assert isinstance(rec, dict), 'Response is not dict'

        for key in ('message', 'status'):
            assert key in rec, f'Wrong response structure - {key} is not found'

        assert rec.get('status') == 'success', 'Wrong status'
        return rec

    @classmethod
    def common_wrong_response_check(cls, r: requests.Response, status: str, msg: str, code: int) -> dict:
        assert r.status_code == code, 'Wrong status code'

        rec = r.json()
        assert isinstance(rec, dict), 'Response is not dict'

        for key, val in {'message': msg, 'status': status, 'code': code}.items():
            assert key in rec, f'Wrong response structure - {key} is not found'
            assert rec.get(key) == val, 'Wrong {key} value'

        return rec

    @classmethod
    def common_count_check(cls, links: list, cnt: int, mode='=='):
        assert isinstance(links, list), 'Object is not list'
        ln = len(links)
        assert ln, 'Objects is empty'
        if mode == '==':
            assert ln == cnt, 'Message has wrong link count'
        elif mode == '<=':
            assert ln <= cnt, 'Message has wrong link count'
        elif mode == '>=':
            assert ln >= cnt, 'Message has wrong link count'

    @classmethod
    def common_count_less_check(cls, links: list, cnt: int):
        assert isinstance(links, list), 'Message is not list'
        assert len(links) == cnt, 'Message has wrong link count'

    @classmethod
    def common_links_check(cls, all_breed_sub_breeds, links: list, breed_=None, sub_breed_=None):
        links = random.sample(links, 5) if len(links) > 5 else links
        for link in links:
            Utils.check_img_link(link, all_breed_sub_breeds, breed_=breed_, sub_breed_=sub_breed_)
            Utils.check_img_by_link(link)

    @classmethod
    def check_img_link(cls, link: str, all_breed_sub_breeds: dict, breed_=None, sub_breed_=None):
        assert link.startswith(URL.base_image), f'Wrong link - {link}'

        breed, sub_breed, jpg = cls.extract_names_jpg(link, URL.base_image)
        assert breed in all_breed_sub_breeds, "Breed doesn't exists"
        if breed_ is not None:
            assert breed == breed_, 'Wrong breed'
        if sub_breed:
            assert sub_breed in all_breed_sub_breeds.get(breed), "Sub_breed doesn't exists"
        if sub_breed_ is not None:
            assert sub_breed == sub_breed_, 'Wrong sub_breed'

    @classmethod
    def check_img_by_link(cls, link: str):
        r = requests.request('get', link)
        assert r.ok, 'Cannot load image'
        assert imghdr.what(None, h=r.content) in ('jpeg', 'png'), 'Content is not an image'

    @classmethod
    def parametrize_breed_not_found(cls, *args):
        for s in args:
            for url in (URL.by_breed(s), URL.by_breed_random(s)):
                yield url, 'error', 'Breed not found (master breed does not exist)', 404

    @classmethod
    def parametrize_route_not_found(cls, *args):
        for s in ('', ):
            for url in (URL.by_breed(s), URL.by_breed_random(s)):
                yield url, 'error', f'No route found for "GET {url[len(URL.main):]}" with code: 0', 404

    @classmethod
    def parametrize_random_count(cls) -> dict:
        all_params = (
            ('x', 1, 'letter'),
            (-1, 1, 'lborder-1'),
            (0, 1, 'lborder'),
            (1, 1, 'lborder+1'),
            (random.randint(2, 48),) * 2 + ('random in range', ),
            (49, 49, 'rborder-1'),
            (50, 50, 'rborder'),
            (51, 50, 'rborder+1'),
        )
        return {
            'params': (x[:2] for x in all_params),
            'ids': (x[2] for x in all_params)
        }

    @classmethod
    def parametrize_random_count_by_breed(cls) -> dict:
        all_params = (
            ('x', 1, '==', 'letter'),
            (-2, 10, '<=', 'negative'),
            (-1, 10, '<=', 'lborder-1'),
            (0, 1, '==', 'lborder'),
            (1, 1, '==', 'lborder+1'),
            (random.randint(2, 50),) * 2 + ('<=', 'random in range'),
            (51, 1000, '<=', 'random in long range'),
        )
        return {
            'params': (x[:3] for x in all_params),
            'ids': (x[3] for x in all_params)
        }


# def get_auth_endpoints():
#     with open("lesson7/data/auth_endpoints.csv", "r") as f:
#         reader = csv.reader(f)
#         next(reader)
#         for i, el in enumerate(reader):
#             if i > 2:
#                 break
#             yield el
#
#
# auth_endpoints = get_auth_endpoints()