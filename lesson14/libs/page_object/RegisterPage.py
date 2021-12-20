from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..Wait import Wait
from ..locators import CSS, XPATH
from ..page_object.BasePage import BasePage


class RegisterPage(BasePage):
    CONTENT = CSS().id('content').res
    AGREE = CSS().input.attr('name', 'agree').res
    CONTINUE = CSS().input.attr('value', 'Continue').res

    ALL_INPUTS = {
        key: (XPATH().label.for_(val).res, CSS().input.id(val).res)
        for key, val in (
            ('firstname', 'input-firstname'),
            ('lastname', 'input-lastname'),
            ('email', 'input-email'),
            ('telephone', 'input-telephone'),
            ('password', 'input-password'),
            ('confirm', 'input-confirm')
        )
    }

    @BasePage.cache
    def _content(self, **kwargs):
        return self._verify_visible_element(self.CONTENT)

    def _set_usual_input(self, key: str, val: str):
        label, input_ = self.ALL_INPUTS.get(key)
        parent = self._content()
        self._verify_visible_element(label, parent=parent)
        self._verify_visible_element(input_, parent=parent).send_keys(val)
        return self

    def set_firstname(self, val: str):
        return self._set_usual_input('firstname', val)

    def set_lastname(self, val: str):
        return self._set_usual_input('lastname', val)

    def set_email(self, val: str):
        return self._set_usual_input('email', val)

    def set_telephone(self, val: str):
        return self._set_usual_input('telephone', val)

    def set_password(self, val: str):
        return self._set_usual_input('password', val)

    def set_confirm(self, val: str):
        return self._set_usual_input('confirm', val)

    def agree(self):
        self._verify_visible_element(self.AGREE, parent=self._content()).click()
        return self

    def continue_(self):
        self._verify_visible_element(self.CONTINUE, parent=self._content()).click()
        Wait(self._driver).until(EC.title_is('Your Account Has Been Created!'))
        return self


if __name__ == '__main__':
    pass
