import csv
import imghdr
import random
from typing import Tuple, List

import requests


class URL:
    main = 'https://jsonplaceholder.typicode.com'
    posts = f'{main}/posts'

    @classmethod
    def by_post_id(cls, id_) -> str:
        return f'{cls.posts}/{id_}'


class Response:

    headers = {
        'Content-type': 'application/json; charset=UTF-8',
    }

    @classmethod
    def posts(cls) -> requests.Response:
        return requests.request('get', URL.posts)

    @classmethod
    def by_post_id(cls, id_) -> requests.Response:
        return requests.request('get', URL.by_post_id(id_))

    @classmethod
    def post(cls, post: dict) -> requests.Response:
        return requests.request('post', URL.posts, headers=cls.headers, params=post)

    @classmethod
    def put(cls, id_, post: dict) -> requests.Response:
        return requests.request('put', URL.by_post_id(id_), headers=cls.headers, params=post)

    @classmethod
    def patch(cls, id_, rec: dict) -> requests.Response:
        return requests.request('patch', URL.by_post_id(id_), headers=cls.headers, params=rec)

    @classmethod
    def delete(cls, id_) -> requests.Response:
        return requests.request('delete', URL.by_post_id(id_))


class Utils:

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
    def get_post_by_id(cls, id_, posts):
        f_posts = list(filter(lambda x: x.get('id') == id_, posts))
        assert f_posts and len(f_posts) == 1, 'Wrong id'
        return f_posts[0]

    @classmethod
    def common_post_check(cls, r: requests.Response, id_, title, body, user_id):
        assert r.status_code == 200, 'Wrong status code'

        post = r.json()
        assert isinstance(post, dict), 'Post is not dict'

        id__ = post.get('id')
        assert id__ == id_ and type(id__) == int, 'Wrong id'

        title_ = post.get('title')
        assert title_ == title and type(title_) == str, 'Wrong title'

        body_ = post.get('body')
        assert body_ == body and type(body_) == str, 'Wrong body'

        user_id_ = post.get('userId')
        assert user_id_ == user_id and type(user_id_) == int, 'Wrong userId'
