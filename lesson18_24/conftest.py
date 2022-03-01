"""
Примеры:
python -m pytest lesson18/test_01.py::TestRunAll::test_main_page --browser=chrome --executor=http://q.w.ru --bversion=86.0
E:/ПО/allure-2.14.0/bin/allure.bat generate allure-results -c
"""
import json
import logging
import time
from datetime import datetime

import allure
import pytest
import requests
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from lesson18.libs.Wait import Wait


class CONFIG:
    KEY_TEST_NAME = '__KEY_TEST_NAME__'
    KEY_LOG_LEVEL = '__KEY_LOG_LEVEL__'
    ALWAYS_SCREEN = False

    ALLURE_RESULTS = 'allure-results'
    ALLURE_REPORT = 'allure-report'

    BROWSERS = {
        'chrome': r'E:\MyApp\hello_world\chromedriver.exe',  # путь до хрома
        'firefox': r'E:\MyApp\hello_world\geckodriver.exe',  # путь до лисы
        'opera': r'E:\MyApp\hello_world\operadriver.exe',  # путь до оперы
    }

    @classmethod
    def driver_factory(cls, browser: str) -> WebDriver:
        if browser in cls.BROWSERS:
            path = cls.BROWSERS[browser]
            func = getattr(cls, browser)
            return func(path)

        raise Exception("Driver not supported")

    @staticmethod
    @allure.step("Get page {url}")
    def get_page(driver: WebDriver, url: str, title: str) -> WebDriver:
        driver.get(url)
        Wait(driver).until(EC.title_is(title))

        return driver


def pytest_addoption(parser: Parser):
    parser.addoption('--browser', action='store', choices=list(CONFIG.BROWSERS.keys()), default='chrome', type=str,
                     help='Browser choice', )
    parser.addoption('--headless', action='store_true', help='Run headless')
    parser.addoption('--url', action='store', help='Main page', default='https://demo.opencart.com/')
    parser.addoption('--browser_console_log', action="store_true", help='Console logs to files')
    parser.addoption('--log_level', action='store', choices=['DEBUG'], default='DEBUG', type=str, help='Log level')
    parser.addoption('--executor', action='store', default='')  # http://qasuag.corp.tander.ru
    parser.addoption('--bversion', action='store', default='')  # 86.0
    parser.addoption('--vnc', action='store_true', default=True)
    parser.addoption('--logs', action='store_true', default=True)
    parser.addoption('--video', action='store_true', default=False)


# https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


@allure.step("Waiting for resource availability {url}")
def wait_url_data(url, timeout=10) -> requests.Response:
    while timeout:
        response = requests.get(url)
        if not response.ok:
            time.sleep(1)
            timeout -= 1
        else:
            return response


@pytest.fixture(scope='session')
def browser(request: SubRequest) -> WebDriver:
    test_name = request.node.name
    log_level = request.config.getoption("--log_level")
    console_log = request.config.getoption('--browser_console_log')

    logger = logging.getLogger('driver')
    logger.addHandler(logging.FileHandler(f'{test_name}.log'))
    logger.setLevel(level=log_level)
    logger.info(f'Test {test_name} started: {datetime.now()}')

    browser = request.config.getoption('--browser')
    executor = request.config.getoption('--executor')
    version = request.config.getoption('--bversion')
    video = request.config.getoption('--video')
    logs = request.config.getoption('--logs')

    if browser == 'firefox':
        caps = DesiredCapabilities.FIREFOX
        options = webdriver.FirefoxOptions()
        driver_class = webdriver.Firefox
    elif browser == 'chrome':
        caps = DesiredCapabilities.CHROME
        options = webdriver.ChromeOptions()
        driver_class = webdriver.Chrome
        options.add_experimental_option('w3c', False)
    elif browser == 'opera':
        from selenium.webdriver.opera.options import Options as OperaOptions
        options = OperaOptions()
        caps = DesiredCapabilities.OPERA
        driver_class = webdriver.Opera
    else:
        raise Exception('Incorrect browser')

    if console_log:
        caps['loggingPrefs'] = {'performance': 'ALL', 'browser': 'ALL', 'driver': 'ALL'}

    if executor:
        driver_class = webdriver.Remote
        caps.update({
            "version": version,
            "enableVNC": request.config.getoption('--vnc'),
            "enableVideo": video,
            "enableLog": logs,
            "sessionTimeout": "5m",
            "timeZone": "Europe/Moscow",
            "acceptInsecureCerts": True
        })
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        kwargs = dict(command_executor=f'{executor}:4444/wd/hub')
    else:
        kwargs = dict(executable_path=CONFIG.BROWSERS[browser])

    driver = driver_class(desired_capabilities=caps,
                          options=options,
                          **kwargs)

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities),
        attachment_type=allure.attachment_type.JSON)

    if executor:
        logger.info(f'{executor}:8080/#/sessions/' + driver.session_id)

    logger.info(f'Browser {browser}: {driver.desired_capabilities}')

    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(5)

    def fin():
        if console_log:
            # Логирование
            for key in (
                    'performance',  # производительности страницы
                    'browser',  # WARNINGS, ERRORS
                    'driver'  # Локальное - драйвер
            ):
                with open(f'{key}.log', 'w+') as f:
                    for line in driver.get_log(key):
                        f.write(f'{line}\n')

        if executor:
            failed = request.node.status != 'passed'

            def fin_url(url: str, content_key: str, name_pref: str, attachment_type):
                url_data = wait_url_data(url)
                if not url_data:
                    return

                content = getattr(url_data, content_key)
                if failed and content:
                    allure.attach(name=name_pref + driver.session_id, body=content, attachment_type=attachment_type)
                if content:
                    requests.delete(url=url)

            if video:
                fin_url(f'http://{executor}:8080/video/{driver.session_id}.mp4', 'content', 'video_',
                        allure.attachment_type.MP4)

            if logs:
                fin_url(f'{executor}/logs/{driver.session_id}.log', 'text', 'log_', allure.attachment_type.TEXT)

        driver.quit()
        logger.info(f'Test {test_name} finished: {datetime.now()}')
        logger.info(f'Report: (after generate) allure open {CONFIG.ALLURE_REPORT}')

        # Add environment info to allure-report
        with open(f'{CONFIG.ALLURE_RESULTS}/environment.xml', 'w+') as file:
            s = '<environment>'

            def add_param(key, value):
                return f"""
                    <parameter>
                        <key>{key}</key>
                        <value>{value}</value>
                    </parameter>
                """

            s += add_param('Browser', browser)
            s += add_param('Browser.Version', version) if version else ''
            s += add_param('Executor', executor) if executor else ''
            s += '</environment>'
            file.write(s)

    request.addfinalizer(fin)

    setattr(driver, CONFIG.KEY_TEST_NAME, test_name)
    setattr(driver, CONFIG.KEY_LOG_LEVEL, log_level)
    return driver


@pytest.fixture(scope='session')
def url_main(request: SubRequest) -> str:
    return request.config.getoption("--url")


@pytest.fixture(scope='session')
def main_page(browser, url_main) -> WebDriver:
    return CONFIG.get_page(browser, url_main, 'Your Store')


@pytest.fixture(scope='session')
def register_page(browser, url_main) -> WebDriver:
    return CONFIG.get_page(browser, url_main + '/index.php?route=account/register', 'Register Account')


@pytest.fixture(scope='session')
def admin_page(browser, url_main) -> WebDriver:
    return CONFIG.get_page(browser, url_main + '/admin', 'Administration')


@pytest.fixture(scope='function')
def admin_products_page(browser, url_main) -> WebDriver:
    return CONFIG.get_page(browser, url_main + '/admin/index.php?route=catalog/product', 'Administration')


@pytest.fixture(scope='session', params=[
    ('20', 'Desktops'),
    ('18', 'Laptops & Notebooks'),
    ('25_28', 'Monitors')
])
def catalogue_page(request, browser, url_main) -> WebDriver:
    id_, title = request.param
    return CONFIG.get_page(browser, f'{url_main}/index.php?route=product/category&path={id_}', title)
