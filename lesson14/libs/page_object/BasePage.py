import inspect
from typing import Optional, List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from lesson14.libs.Wait import Wait


class wait_exception:

    @classmethod
    def Timeout(cls, msg: str):
        def decorator(action):
            args_names = inspect.signature(action).parameters.keys()

            def wrapper(*args, **kwargs):
                try:
                    return action(*args, **kwargs)
                except TimeoutException:
                    msg_ = msg
                    for arg, val in tuple(zip(args_names, args)) + tuple(kwargs.items()):
                        key = '{' + arg + '}'
                        if key in msg:
                            msg_ = msg_.replace(key, str(val))

                    raise AssertionError(msg_)

            return wrapper

        return decorator


class BasePage:
    SELF: tuple = None

    def __init__(self, driver: WebDriver, self_verify=True):
        self._driver = driver
        self._self_verify = self_verify
        self.driver: Optional[WebDriver, WebElement] = None
        self._reini()

    def _reini(self):
        self.driver = self._verify_visible_element(self.SELF, parent=self._driver) \
            if self._self_verify and self.SELF else self._driver
        self.__cache = {}

    @wait_exception.Timeout('Can\'t find visible element by locator: {locator}')
    def _verify_visible_element(self, locator: tuple, parent=None) -> WebElement:
        return Wait(parent or self.driver).until(EC.visibility_of_element_located(locator))

    @wait_exception.Timeout('Can\'t find visible elements by locator: {locator}')
    def _verify_visible_elements(self, locator: tuple, parent=None) -> List[WebElement]:
        return Wait(parent or self.driver).until(EC.visibility_of_all_elements_located(locator))

    def _click_element(self, element):
        ActionChains(self._driver).pause(0.3).move_to_element(element).click().perform()

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
