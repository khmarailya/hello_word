from typing import Union, List

from multipledispatch import dispatch
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class EC:
    """ my expected_conditions """


class Wait(WebDriverWait):
    """ my WebDriverWait """

    def __init__(self, driver, timeout=2, frequency=1):
        super().__init__(driver, timeout, poll_frequency=frequency)

    @classmethod
    @dispatch(object, WebDriverWait, str)
    def CSS_ALL(cls, wait: WebDriverWait, scc: str) -> List[WebElement]:
        return wait.until(cls._scc_all(scc))

    @classmethod
    @dispatch(object, (WebDriver, WebElement), str)
    def CSS_ALL(cls, driver: Union[WebDriver, WebElement], scc: str) -> List[WebElement]:
        return cls.CSS_ALL(cls(driver), scc)

    def css_all(self, scc: str) -> List[WebElement]:
        return self.CSS_ALL(self, scc)

    @staticmethod
    def _scc_all(css: str):
        def wrapper(driver: Union[WebDriver, WebElement]) -> List[WebElement]:
            elements = driver.find_elements(By.CSS_SELECTOR, css)
            return elements

        return wrapper

    # @classmethod
    # @dispatch(object, WebDriverWait, str, object)
    # def CSS(cls, wait: WebDriverWait, scc: str, cond) -> WebElement:
    #     return wait.until(cond((By.CSS_SELECTOR, scc)))
    #
    # @classmethod
    # @dispatch(object, (WebDriver, WebElement), str, object)
    # def CSS(cls, driver: Union[WebDriver, WebElement], scc: str, cond) -> WebElement:
    #     return cls.CSS(cls(driver), scc, cond)

    def css(self, scc: str, cond) -> WebElement:
        return self.until(cond((By.CSS_SELECTOR, scc)))
        # return self.CSS(self, scc, cond)

    @classmethod
    @dispatch(object, WebDriverWait, str, object)
    def XPATH(cls, wait: WebDriverWait, xpath: str, cond) -> WebElement:
        return wait.until(cond((By.XPATH, xpath)))

    @classmethod
    @dispatch(object, (WebDriver, WebElement), str, object)
    def XPATH(cls, driver: Union[WebDriver, WebElement], xpath: str, cond) -> WebElement:
        return cls.XPATH(cls(driver), xpath, cond)

    def xpath(self, xpath: str, cond) -> WebElement:
        return self.XPATH(self, xpath, cond)


if __name__ == '__main__':
    pass
