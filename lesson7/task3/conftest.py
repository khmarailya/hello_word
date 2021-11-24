import random
from typing import Tuple, List, Iterable

import pytest
import csv

import requests

from lesson7.task3 import URL, Response, Utils


@pytest.fixture(scope="session")
def f_posts() -> List[dict]:
    return Response.posts().json()


@pytest.fixture(scope="session")
def f_post_ids(f_posts) -> dict:
    return Utils.mark_choice(f_posts, 'id')


@pytest.fixture(scope="function")
def f_random_post_id(f_post_ids) -> str:
    return Utils.choice(f_post_ids)

