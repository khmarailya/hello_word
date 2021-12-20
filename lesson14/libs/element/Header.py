from selenium.webdriver.common.by import By

from ..locators import CSS
from ..page_object.BasePage import BasePage


class Header(BasePage):
    """ #header находится на каждой странице магазина """

    SELF = CSS().body.child.header.res
    LOGO = CSS().id('logo').res
    CART = CSS().id('cart').res
    SEARCH = CSS().id('search').res

    def check_logo(self):
        logo = self._verify_visible_element(self.LOGO)
        assert logo.text == 'Your Store', 'Incorrect logo text'
        return self

    def check_cart(self, currency: str):
        cart = self._verify_visible_element(self.CART)
        assert currency in cart.text, 'Incorrect cart text'
        return self

    def check_search(self):
        search = self._verify_visible_element(self.SEARCH)
        input_ = search.find_element(By.NAME, 'search')
        assert input_.get_attribute('placeholder') == 'Search', 'Incorrect placeholder'
        return self
