import allure
from selenium.webdriver.support import expected_conditions as EC

from ..Wait import Wait
from ..element.AlertError import AlertError
from ..locators import CSS, XPATH
from ..page_object.BasePage import BasePage, screen_step


class AdminProductPage(BasePage):
    ADD_BTN = CSS().a.attr('data-original-title', 'Add New').res
    SAVE_BTN = CSS().button.attr('data-original-title', 'Save').res
    DELETE_BTN = CSS().button.attr('data-original-title', 'Delete').res
    FORM_PRODUCT = CSS().id('form-product').res
    PRODUCT_LIST_CHECKBOXES = CSS().id('form-product').descendant.tbody.descendant.input.attr('type', 'checkbox').res

    GENERAL_TAB = XPATH().li.content('General').res
    GENERAL_TAB_CONTENT = CSS().id('tab-general').res

    DATA_TAB = XPATH().li.content('Data').res
    DATA_TAB_CONTENT = CSS().id('tab-data').res

    PRODUCT_NAME_LABEL = XPATH().label.for_('input-name1').res
    PRODUCT_NAME_INPUT = CSS().input.id('input-name1').res

    PRODUCT_META_TAG_LABEL = XPATH().label.for_('input-meta-title1').res
    PRODUCT_META_TAG_INPUT = CSS().input.id('input-meta-title1').res

    USUAL_PRODUCT_INPUTS = {
        key: (XPATH().label.for_(val).res, CSS().input.id(val).res)
        for key, val in (
            ('name', 'input-name1'),
            ('meta_tag', 'input-meta-title1'),
            ('model', 'input-model'),
        )
    }

    @screen_step('Check page with title "Products" is loaded')
    def check_loaded(self):
        Wait(self.driver).until(EC.title_is('Products'))
        return self

    @BasePage.cache
    @screen_step('Find form with product')
    def _form_product(self, **kwargs):
        return self._verify_visible_element(self.FORM_PRODUCT)

    @BasePage.cache
    @screen_step('Find general tab')
    def _tab_general_content(self, **kwargs):
        return self._verify_visible_element(self.GENERAL_TAB_CONTENT, parent=self._form_product(**kwargs))

    @BasePage.cache
    @screen_step('Find content tab')
    def _tab_data_content(self, **kwargs):
        return self._verify_visible_element(self.DATA_TAB_CONTENT, parent=self._form_product(**kwargs))

    @screen_step('Find and click add button')
    def _find_and_click_add_button(self):
        self._verify_visible_element(self.ADD_BTN).click()

    @screen_step('Find and click save button')
    def _find_and_click_save_button(self):
        self._verify_visible_element(self.SAVE_BTN).click()

    @screen_step('Find and click delete button')
    def _find_and_click_delete_button(self):
        self._verify_visible_element(self.DELETE_BTN).click()

    @screen_step('Check alert "{text}" and accept')
    def _check_alert_and_accept(self, text: str):
        alert = self._driver.switch_to.alert
        assert alert.text == text, 'Incorrect alert text'
        alert.accept()

    @screen_step('Add new article')
    def add_new(self):
        self._find_and_click_add_button()
        self._form_product()
        return self

    @screen_step('Delete article')
    def delete(self):
        self._find_and_click_delete_button()
        self._check_alert_and_accept('Are you sure?')
        AlertError(self.driver) \
            .check_have_no_permission()
        return self

    @screen_step('Save article')
    def save(self):
        self._find_and_click_save_button()
        AlertError(self.driver) \
            .check_have_no_permission()
        return self

    @screen_step('Open general')
    def open_general(self):
        _form_product = self._form_product()
        with allure.step('Find and click general tab'):
            self._verify_visible_element(self.GENERAL_TAB, parent=_form_product).click()
        self._tab_general_content()
        return self

    @screen_step('Open data')
    def open_data(self):
        _form_product = self._form_product()
        with allure.step('Find and click data tab'):
            self._verify_visible_element(self.DATA_TAB, parent=_form_product).click()
        self._tab_data_content()
        return self

    @screen_step('Find input "{key}" and type "{val}"')
    def _set_usual_input(self, key: str, val: str, parent=None):
        label, input_ = self.USUAL_PRODUCT_INPUTS.get(key)
        self._verify_visible_element(label, parent=parent)
        self._send_keys(self._verify_visible_element(input_, parent=parent), val)
        return self

    @screen_step('Set product name "{val}"')
    def set_product_name(self, val: str):
        return self._set_usual_input('name', val, parent=self._tab_general_content())

    @screen_step('Set meta tag "{val}"')
    def set_meta_tag(self, val: str):
        return self._set_usual_input('meta_tag', val, parent=self._tab_general_content())

    @screen_step('Set model "{val}"')
    def set_model(self, val: str):
        return self._set_usual_input('model', val, parent=self._tab_data_content())

    @screen_step('Select many products')
    def select(self, *indexes):
        _form_product = self._form_product()
        checkboxes = self._verify_visible_elements(self.PRODUCT_LIST_CHECKBOXES, parent=_form_product)
        for i in indexes:
            checkboxes[i].click()
        return self


if __name__ == '__main__':
    pass
