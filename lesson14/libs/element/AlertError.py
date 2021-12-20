from ..locators import XPATH, CSS
from ..page_object.BasePage import BasePage


class AlertError(BasePage):
    SELF = CSS().classes('alert-danger').res

    def check_text(self, text: str):
        assert text in self.driver.text, 'Incorrect alert text'
        return self

    def check_have_no_permission(self):
        self.check_text('Warning: You do not have permission to modify products!')
        return self
