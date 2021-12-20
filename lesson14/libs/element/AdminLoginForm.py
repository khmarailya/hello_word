from ..locators import XPATH, CSS
from ..page_object.BasePage import BasePage


class AdminLoginForm(BasePage):

    SELF = CSS().body.descendant.id('content').res
    USER_LABEL = XPATH().label.for_('input-username').res
    USER_INPUT = XPATH().input.name('username').res
    PASSWORD_LABEL = XPATH().label.for_('input-password').res
    PASSWORD_INPUT = XPATH().input.name('password').res
    SUBMIT = XPATH().button.type('submit').res

    def login(self, user, password):
        self._verify_visible_element(self.USER_LABEL)
        input_ = self._verify_visible_element(self.USER_INPUT)
        input_.clear()
        input_.send_keys(user)
        self._verify_visible_element(self.PASSWORD_LABEL)
        input_ = self._verify_visible_element(self.PASSWORD_INPUT)
        input_.clear()
        input_.send_keys(user)
        self._verify_visible_element(self.SUBMIT).click()

