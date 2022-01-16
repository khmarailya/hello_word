from ..locators import XPATH, CSS
from ..page_object.BasePage import BasePage, screen_step


class AlertError(BasePage):
    SELF = CSS().classes('alert-danger').res

    @screen_step('Check alert text "{text}"')
    def check_text(self, text: str):
        assert text in self.driver.text, 'Incorrect alert text'
        return self

    @screen_step('Check there is no permission')
    def check_have_no_permission(self):
        self.check_text('Warning: You do not have permission to modify products!')
        return self
