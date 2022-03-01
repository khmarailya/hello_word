import inspect
import logging
from typing import Optional, List, Iterable

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from lesson18.conftest import CONFIG
from lesson18.libs.Wait import Wait


def screen_step(step_definition: str, exceptions: Iterable[type] = None):
    def decorator(action):
        args_names = inspect.signature(action).parameters.keys()

        def wrapper(self: 'BasePage', *args, **kwargs):
            err = None
            step_definition_ = step_definition
            for arg, val in tuple(zip(args_names, (self, ) + args)) + tuple(kwargs.items()):
                key = '{' + arg + '}'
                if key in step_definition:
                    step_definition_ = step_definition_.replace(key, str(val))

            with allure.step(step_definition_):
                try:
                    return action(self, *args, **kwargs)
                except Exception as e:
                    err = e
                    if exceptions and isinstance(e, tuple(exceptions)):
                        raise AssertionError(e)
                    else:
                        raise
                finally:
                    if err or CONFIG.ALWAYS_SCREEN:
                        driver = self._driver
                        allure.attach(
                            body=driver.get_screenshot_as_png(),
                            name="screenshot_image",
                            attachment_type=allure.attachment_type.PNG)

        return wrapper

    return decorator


# class wait_exception:
#
#     @classmethod
#     def Timeout(cls, msg: str):
#         def decorator(action):
#             args_names = inspect.signature(action).parameters.keys()
#
#             def wrapper(*args, **kwargs):
#                 try:
#                     return action(*args, **kwargs)
#                 except TimeoutException:
#                     msg_ = msg
#                     for arg, val in tuple(zip(args_names, args)) + tuple(kwargs.items()):
#                         key = '{' + arg + '}'
#                         if key in msg:
#                             msg_ = msg_.replace(key, str(val))
#
#                     raise AssertionError(msg_)
#
#             return wrapper
#
#         return decorator


class BasePage:
    SELF: tuple = None

    def __init__(self, driver: WebDriver, self_verify=True):
        with allure.step(f'Ini new page object "{self}"'):
            self._driver = driver
            self._self_verify = self_verify
            self.driver: Optional[WebDriver, WebElement] = None
            self._config_logger()
            self._reini()

    def _reini(self):
        self.driver = self._verify_visible_element(self.SELF, parent=self._driver) \
            if self._self_verify and self.SELF else self._driver
        self.__cache = {}

    def _config_logger(self):
        test_name = getattr(self._driver, CONFIG.KEY_TEST_NAME)
        log_level = getattr(self._driver, CONFIG.KEY_LOG_LEVEL)

        self.logger = logging.getLogger(str(self))
        self.logger.addHandler(logging.FileHandler(f"{test_name}.log"))
        self.logger.setLevel(level=log_level)

    def __str__(self):
        return type(self).__name__

    @screen_step('[{self}] Finding element by locator: {locator}', [TimeoutException])
    def _verify_visible_element(self, locator: tuple, parent=None) -> WebElement:
        self.logger.info(f'{self} => Verifying visible element: {locator}')
        return Wait(parent or self.driver).until(EC.visibility_of_element_located(locator))

    @screen_step('[{self}] Finding elements by locator: {locator}', [TimeoutException])
    def _verify_visible_elements(self, locator: tuple, parent=None) -> List[WebElement]:
        self.logger.info(f'{self} => Verifying visible elements: {locator}')
        return Wait(parent or self.driver).until(EC.visibility_of_all_elements_located(locator))

    @screen_step('[{self}] Clicking element')
    def _click_element(self, element):
        self.logger.info(f'{self} => Clicking element')
        ActionChains(self._driver).pause(0.3).move_to_element(element).click().perform()

    @screen_step('[{self}] Typing "{val}"')
    def _send_keys(self, element: WebElement, val: str):
        self.logger.info(f'{self} => Typing {val}')
        element.send_keys(val)

    @classmethod
    def cache(cls, action):
        key = action.__name__

        def wrapper(self: BasePage, *args, renew=False, **kwargs) -> WebElement:
            if renew or key not in self.__cache:
                self.__cache[key] = res = action(self, *args, renew=renew, **kwargs)
            else:
                res = self.__cache[key]
            return res

        return wrapper


if __name__ == '__main__':
    pass
