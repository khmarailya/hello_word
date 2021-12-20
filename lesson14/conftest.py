"""
Примеры:
pytest lesson11/test_01.py::TestRunMainPage::test_all --browser="chrome"
"""
from typing import Tuple

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lesson14.libs.Wait import Wait

BROWSERS = {
    'chrome': (
        webdriver.Chrome,
        r'E:\MyApp\hello_world\chromedriver.exe'  # путь до хрома
    ),
    'firefox': (
        webdriver.Firefox,
        r'E:\MyApp\hello_world\geckodriver.exe'  # путь до лисы
    ),
    'opera': (
        webdriver.Opera,
        r'E:\MyApp\hello_world\operadriver.exe'  # путь до оперы
    )
}

ALL_BROWSERS = list(BROWSERS.keys())


def driver_factory(browser: str) -> WebDriver:
    if browser in BROWSERS:
        cls, path = BROWSERS[browser]
        return cls(executable_path=path)

    raise Exception("Driver not supported")


def get_page(driver: WebDriver, url: str, title: str) -> WebDriver:
    driver.get(url)
    Wait(driver).until(EC.title_is(title))
    return driver


def pytest_addoption(parser: Parser):
    parser.addoption(
        '--browser', action="store", choices=ALL_BROWSERS, default=ALL_BROWSERS[0], type=str, help='Browser choice',
    )
    parser.addoption(
        '--headless', action="store_true", help='Run headless',
    )
    parser.addoption(
        '--url', action="store", help='Run headless', default='https://demo.opencart.com/'
    )


@pytest.fixture(scope='session')
def browser(request: SubRequest) -> WebDriver:
    driver = driver_factory(request.config.getoption("--browser"))
    # driver.maximize_window()
    driver.implicitly_wait(5)
    request.addfinalizer(driver.quit)
    return driver


@pytest.fixture(scope='session')
def url_main(request: SubRequest) -> str:
    return request.config.getoption("--url")


@pytest.fixture(scope='session')
def main_page(browser, url_main) -> WebDriver:
    return get_page(browser, url_main, 'Your Store')


@pytest.fixture(scope='session')
def register_page(browser, url_main) -> WebDriver:
    return get_page(browser, url_main + '/index.php?route=account/register', 'Register Account')


@pytest.fixture(scope='session')
def admin_page(browser, url_main) -> WebDriver:
    return get_page(browser, url_main + '/admin', 'Administration')


@pytest.fixture(scope='function')
def admin_products_page(browser, url_main) -> WebDriver:
    return get_page(browser, url_main + '/admin/index.php?route=catalog/product', 'Administration')


@pytest.fixture(scope='session', params=[
    ('20', 'Desktops'),
    ('18', 'Laptops & Notebooks'),
    ('25_28', 'Monitors')
])
def catalogue_page(request, browser, url_main) -> WebDriver:
    id_, title = request.param
    return get_page(browser, f'{url_main}/index.php?route=product/category&path={id_}', title)


# dsr - описание, спецификации, ревью, есть ли эти вкладки
@pytest.fixture(scope='session', params=[
    ('43', 'MacBook', 'dsr'),
    ('40', 'iPhone', 'dr')
])
def card_page_params(request, browser, url_main) -> Tuple[WebDriver, str]:
    id_, title, dsr = request.param
    return get_page(browser, f'{url_main}/index.php?route=product/product&product_id={id_}', title), dsr
