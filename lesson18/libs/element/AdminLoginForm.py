import allure

from ..locators import XPATH, CSS
from ..page_object.BasePage import BasePage, screen_step


class AdminLoginForm(BasePage):

    SELF = CSS().body.descendant.id('content').res
    USER_LABEL = XPATH().label.for_('input-username').res
    USER_INPUT = XPATH().input.name('username').res
    PASSWORD_LABEL = XPATH().label.for_('input-password').res
    PASSWORD_INPUT = XPATH().input.name('password').res
    SUBMIT = XPATH().button.type('submit').res

    @screen_step('Login as "{user}" by "{password}"')
    def login(self, user, password):
        with allure.step(f'Find user input and type "{user}"'):
            self._verify_visible_element(self.USER_LABEL)
            input_ = self._verify_visible_element(self.USER_INPUT)
            input_.clear()
            self._send_keys(input_, user)
        with allure.step(f'Find password input and type "{password}"'):
            self._verify_visible_element(self.PASSWORD_LABEL)
            input_ = self._verify_visible_element(self.PASSWORD_INPUT)
            input_.clear()
            self._send_keys(input_, password)

        with allure.step('Submit'):
            self._verify_visible_element(self.SUBMIT).click()

