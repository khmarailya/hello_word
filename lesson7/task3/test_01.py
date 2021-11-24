from typing import Tuple

import requests
import pytest

from lesson7.task3 import Utils, Response


class TestRunGet:

    @pytest.mark.parametrize('ind', range(5))
    def test_common(self, f_random_post_id, f_posts, ind):
        f_post = Utils.get_post_by_id(f_random_post_id, f_posts)
        Utils.common_post_check(
            Response.by_post_id(f_random_post_id), f_post['id'], f_post['title'], f_post['body'], f_post['userId'])


class TestRunPost:

    @pytest.mark.parametrize('title, body, user_id, expected_id', (
            ('foo', 'bar', 1, 101),
            ('bar', 'foo', 2, 101),
    ))
    def test_common(self, f_posts, title, body, user_id, expected_id):
        r = Response.post({
            'title': title,
            'body': body,
            'userId': user_id,
        })
        assert r.status_code == 201, 'Wrong status code'

        post = r.json()
        assert isinstance(post, dict), 'Post is not dict'

        id_ = post.get('id')
        assert expected_id == id_ and type(id_) == int, 'Wrong id'

        r = Response.by_post_id(id_)
        assert r.status_code == 404, 'Wrong status code'


class TestRunPut:

    @pytest.mark.parametrize('title, body, user_id', (
            ('foo', 'bar', 1),
            ('bar', 'foo', 2),
    ))
    def test_common(self, f_random_post_id, f_posts, title, body, user_id):
        r = Response.put(f_random_post_id, {
            'id': f_random_post_id,
            'title': title,
            'body': body,
            'userId': user_id,
        })
        assert r.status_code == 200, 'Wrong status code'

        post = r.json()
        assert isinstance(post, dict), 'Post is not dict'

        id_ = post.get('id')
        assert f_random_post_id == id_ and type(id_) == int, 'Wrong id'

        f_post = Utils.get_post_by_id(id_, f_posts)
        Utils.common_post_check(
            Response.by_post_id(id_), f_post['id'], f_post['title'], f_post['body'], f_post['userId'])


class TestRunPatch:

    @pytest.mark.parametrize('title, body, user_id', (
            ('foo', None, None),
            (None, 'foo', None),
            (None, None, 2),
    ))
    def test_common(self, f_random_post_id, f_posts, title, body, user_id):
        rec = {}
        if title is not None:
            rec['title'] = title
        if body is not None:
            rec['body'] = body
        if user_id is not None:
            rec['userId'] = user_id

        f_post = Utils.get_post_by_id(f_random_post_id, f_posts)
        Utils.common_post_check(
            Response.patch(f_random_post_id, rec), f_post['id'], f_post['title'], f_post['body'], f_post['userId'])


class TestRunDelete:

    @pytest.mark.parametrize('ind', range(5))
    def test_common(self, f_random_post_id, f_posts, ind):
        r = Response.delete(f_random_post_id)
        assert r.status_code == 200, 'Wrong status code'

        rec = r.json()
        assert isinstance(rec, dict), 'Rec is not dict'
        assert not rec, 'Rec is not empty'

        f_post = Utils.get_post_by_id(f_random_post_id, f_posts)
        Utils.common_post_check(
            Response.by_post_id(f_random_post_id), f_post['id'], f_post['title'], f_post['body'], f_post['userId'])

if __name__ == '__main__':
    pass