from typing import Union, List

from multipledispatch import dispatch
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyWait(WebDriverWait):

    def __init__(self, driver):
        super().__init__(driver, 3, 1)

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

    @classmethod
    @dispatch(object, WebDriverWait, str, object)
    def CSS(cls, wait: WebDriverWait, scc: str, cond) -> WebElement:
        return wait.until(cond((By.CSS_SELECTOR, scc)))

    @classmethod
    @dispatch(object, (WebDriver, WebElement), str, object)
    def CSS(cls, driver: Union[WebDriver, WebElement], scc: str, cond) -> WebElement:
        return cls.CSS(cls(driver), scc, cond)

    def css(self, scc: str, cond) -> WebElement:
        return self.CSS(self, scc, cond)

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


class CommonTests:

    @staticmethod
    def test_top(driver: WebDriver):
        """ #top находится на каждой странице """
        top = MyWait.CSS(driver, 'body > #top', EC.visibility_of_element_located)
        currency_btn = MyWait.CSS(top, '#form-currency > .btn-group', EC.visibility_of_element_located)
        currency_btn.click()

        currency_btn_wait = MyWait(currency_btn)
        for name, text in (('EUR', '€ Euro'), ('GBP', '£ Pound Sterling'), ('USD', '$ US Dollar')):
            btn = currency_btn_wait.css(f'button[name="{name}"]', EC.visibility_of_element_located)
            assert btn.text == text, ''

    @staticmethod
    def test_header(driver: WebDriver):
        """ header находится на каждой странице """
        header = MyWait.CSS(driver, 'body > header', EC.visibility_of_element_located)
        logo_btn = MyWait.CSS(header, '#logo', EC.visibility_of_element_located)
        assert logo_btn.text == 'Your Store', ''
        cart_btn = MyWait.CSS(header, '#cart', EC.visibility_of_element_located)
        assert cart_btn.text == '0 item(s) - $0.00', ''
        search = MyWait.CSS(header, '#search', EC.visibility_of_element_located)
        input_ = search.find_element(By.NAME, 'search')
        assert input_.get_attribute('placeholder') == 'Search', ''

    @staticmethod
    def test_menu(driver: WebDriver):
        """ menu находится на каждой странице """
        menu = MyWait.CSS(driver, 'body #menu', EC.visibility_of_element_located)
        btns: List[WebElement] = menu.find_elements(By.CSS_SELECTOR, '.nav > li')
        btn_texts = set(btn.text for btn in btns)
        for text in ('Desktops', 'Laptops & Notebooks', 'Components'):
            assert text in btn_texts, ''


class TestRunMainPage:

    def test_all(self, main_page):
        CommonTests.test_top(main_page)
        CommonTests.test_header(main_page)
        CommonTests.test_menu(main_page)
        content = MyWait.CSS(main_page, '#common-home #content', EC.visibility_of_element_located)
        slideshow0 = MyWait.CSS(content, '#slideshow0', EC.visibility_of_element_located)
        featured = MyWait.XPATH(content, '//h3[text()="Featured"]', EC.visibility_of_element_located)
        features = MyWait.CSS_ALL(content, 'div.product-layout')
        assert len(features) == 4, ''
        sponsors = MyWait.XPATH(content, '//h3[text()="Featured"]', EC.visibility_of_element_located)


class TestRunCatalogue:

    def test_all(self, catalogue_page):
        CommonTests.test_top(catalogue_page)
        CommonTests.test_header(catalogue_page)
        CommonTests.test_menu(catalogue_page)
        product_category = MyWait.CSS(catalogue_page, '#product-category', EC.visibility_of_element_located)
        category_path = MyWait.CSS(product_category, 'ul.breadcrumb', EC.visibility_of_element_located)
        column_left = MyWait.CSS(catalogue_page, '#column-left', EC.visibility_of_element_located)
        content = MyWait.CSS(catalogue_page, '#content', EC.visibility_of_element_located)
        content_title = MyWait.XPATH(content, f'//h2[text()="{catalogue_page.title}"]',
                                     EC.visibility_of_element_located)


class TestRunCard:

    def test_all(self, card_page_params):
        card_page, dsr = card_page_params
        CommonTests.test_top(card_page)
        CommonTests.test_header(card_page)
        CommonTests.test_menu(card_page)
        product_product = MyWait.CSS(card_page, '#product-product', EC.visibility_of_element_located)
        product_path = MyWait.CSS(product_product, 'ul.breadcrumb', EC.visibility_of_element_located)
        content = MyWait.CSS(card_page, '#content', EC.visibility_of_element_located)
        product_title = MyWait.XPATH(content, f'//h1[text()="{card_page.title}"]', EC.visibility_of_element_located)
        thumbnail = MyWait.XPATH(content, f'//a[@title="{card_page.title}"]', EC.visibility_of_element_located)
        tabs = MyWait.CSS(content, '.nav.nav-tabs', EC.visibility_of_element_located)
        for tab_title, content_id, has_dsr in (
                ('Description', '#tab-description', 'd'),
                ('Specification', '#tab-specification', 's'),
                ('Reviews', '#tab-review', 'r')
        ):
            if has_dsr not in dsr:
                continue

            tab = MyWait.XPATH(tabs, f'//a[starts-with(text(), "{tab_title}")]',
                               EC.visibility_of_element_located)
            tab.click()
            tab_content = MyWait.CSS(content, content_id, EC.visibility_of_element_located)


class TestRunRegister:

    def test_all(self, register_page):
        CommonTests.test_top(register_page)
        CommonTests.test_header(register_page)
        CommonTests.test_menu(register_page)
        content = MyWait.CSS(register_page, '#content', EC.visibility_of_element_located)
        title = MyWait.XPATH(content, f'//h1[text()="{register_page.title}"]', EC.visibility_of_element_located)
        for legend in ('Your Personal Details', 'Your Password', 'Newsletter'):
            fieldset = MyWait.XPATH(content, f'//fieldset//legend[text()="{legend}"]', EC.visibility_of_element_located)
        column_right = MyWait.CSS(register_page, '#column-right', EC.visibility_of_element_located)


class TestRunAdmin:

    def test_all(self, admin_page):
        header = MyWait.CSS(admin_page, '#header', EC.visibility_of_element_located)
        content = MyWait.CSS(admin_page, '#content', EC.visibility_of_element_located)
        form = MyWait.CSS(admin_page, 'form', EC.visibility_of_element_located)
        label = MyWait.XPATH(form, f'//label[@for="input-username"]', EC.visibility_of_element_located)
        input_ = MyWait.XPATH(form, f'//input[@name="username"]', EC.visibility_of_element_located)
        label = MyWait.XPATH(form, f'//label[@for="input-password"]', EC.visibility_of_element_located)
        input_ = MyWait.XPATH(form, f'//input[@name="password"]', EC.visibility_of_element_located)
        submit = MyWait.XPATH(form, f'//button[@type="submit"]', EC.visibility_of_element_located)


if __name__ == '__main__':
    pass
