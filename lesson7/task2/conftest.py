from typing import Tuple

import pytest

import requests

from lesson7.task2 import URL, Response, Utils


@pytest.fixture(scope="session")
def f_examples() -> requests.Response:
    return Response.examples()


@pytest.fixture(scope="session")
def f_cities(f_examples) -> dict:
    return Utils.mark_choice(f_examples.json(), 'city')


@pytest.fixture(scope="function")
def f_random_city(f_cities) -> str:
    return Utils.choice(f_cities)


@pytest.fixture(scope="session")
def f_dist(f_examples) -> dict:
    return Utils.mark_choice(f_examples.json(), 'longitude', 'latitude')


@pytest.fixture(scope="function")
def f_random_dist(f_dist) -> Tuple[str, str]:
    return Utils.choice(f_dist)


@pytest.fixture(scope="session")
def f_types_set() -> set:
    return {"micro", "nano", "regional", "brewpub", "large", "planning", "bar", "contract", "proprieter", "closed"}


@pytest.fixture(scope="session")
def f_types(f_types_set) -> dict:
    json = [{'name': t} for t in f_types_set]
    return Utils.mark_choice(json, 'name')


@pytest.fixture(scope="function")
def f_random_type(f_types) -> str:
    return Utils.choice(f_types)


# @pytest.fixture(scope="function")
# def f_random_city(f_cities) -> str:
#     return random.choice(f_cities)


@pytest.fixture(scope="session")
def f_by_city(request) -> requests.Response:
    return Response.by_city(request.param)
