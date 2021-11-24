import random
from typing import Tuple

import pytest

import requests

from lesson7.task1 import URL, Utils


@pytest.fixture(scope="session")
def url_all_response() -> requests.Response:
    return requests.request('get', URL.all)


@pytest.fixture(scope="session")
def all_breed_sub_breeds(url_all_response) -> dict:
    rec = url_all_response.json()
    return rec.get('message')


@pytest.fixture(scope="session")
def all_breads(all_breed_sub_breeds) -> tuple:
    return tuple(all_breed_sub_breeds.keys())


@pytest.fixture(scope="function", params=range(10))
def random_breed_response(all_breads) -> requests.Response:
    breed = random.choice(all_breads)
    return requests.request('get', URL.by_breed(breed))


@pytest.fixture(scope="function", params=[
    ('1', 'error', 'Breed not found (master breed does not exist)', 404),
    ('', 'error', 'No route found for "GET /api/breed//images" with code: 0', 404)
])
def fixture_wrong_breed(request, all_breads) -> Tuple:
    url = URL.by_breed(request.param[0])
    return requests.request('get', url), *request.param[1:]


@pytest.fixture(scope="function", params=range(10))
def random_breed_response_single(request, all_breads) -> requests.Response:
    breed = random.choice(all_breads)
    return requests.request('get', URL.by_breed_random(breed))


@pytest.fixture(scope="function")
def url_random_response() -> requests.Response:
    return requests.request('get', URL.random)


@pytest.fixture(scope="function")
def url_random_count_response():
    return lambda cnt: requests.request('get', URL.random_count(cnt))


@pytest.fixture(scope="function", **Utils.parametrize_random_count())
def p_f_random_count(request, url_random_count_response):
    cnt = request.param[0]
    return url_random_count_response(cnt), *request.param


@pytest.fixture(scope="function")
def url_random_count_by_breed_response():
    return lambda breed, cnt: requests.request('get', URL.by_breed_random_cnt(breed, cnt))


@pytest.fixture(scope="function", **Utils.parametrize_random_count_by_breed())
def p_f_random_count_by_breed(request, all_breads, url_random_count_by_breed_response):
    breed = random.choice(all_breads)
    cnt = request.param[0]
    return url_random_count_by_breed_response(breed, cnt), breed, *request.param
