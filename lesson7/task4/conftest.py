from _pytest.config import Config
from _pytest.python import Metafunc



def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default='https://ya.ru', type=str,
        help="",
    )
    parser.addoption(
        "--status_code", action="store", default='200', type=int,
        help="",
    )


def pytest_generate_tests(metafunc: Metafunc):
    conf: Config = metafunc.config
    if "url" in metafunc.fixturenames:
        metafunc.parametrize("url", [conf.getoption("--url")])

    if "status_code" in metafunc.fixturenames:
        metafunc.parametrize("status_code", [conf.getoption("--status_code")])

