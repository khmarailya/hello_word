from selenium.webdriver.support import expected_conditions as EC

from ..Wait import Wait
from ..element.AlertError import AlertError
from ..locators import CSS, XPATH
from ..page_object.BasePage import BasePage


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

    def check_loaded(self):
        Wait(self.driver).until(EC.title_is('Products'))
        return self

    @BasePage.cache
    def _form_product(self, **kwargs):
        return self._verify_visible_element(self.FORM_PRODUCT)

    @BasePage.cache
    def _tab_general_content(self, **kwargs):
        return self._verify_visible_element(self.GENERAL_TAB_CONTENT, parent=self._form_product(**kwargs))

    @BasePage.cache
    def _tab_data_content(self, **kwargs):
        return self._verify_visible_element(self.DATA_TAB_CONTENT, parent=self._form_product(**kwargs))

    def add_new(self):
        self._verify_visible_element(self.ADD_BTN).click()
        self._form_product()
        return self

    def delete(self):
        self._verify_visible_element(self.DELETE_BTN).click()
        alert = self._driver.switch_to.alert
        assert alert.text == 'Are you sure?', 'Incorrect alert text'
        alert.accept()
        AlertError(self.driver) \
            .check_have_no_permission()
        return self

    def save(self):
        self._verify_visible_element(self.SAVE_BTN).click()
        AlertError(self.driver) \
            .check_have_no_permission()
        return self

    def open_general(self):
        _form_product = self._form_product()
        self._verify_visible_element(self.GENERAL_TAB, parent=_form_product).click()
        self._tab_general_content()
        return self

    def open_data(self):
        _form_product = self._form_product()
        self._verify_visible_element(self.DATA_TAB, parent=_form_product).click()
        self._tab_data_content()
        return self

    def _set_usual_input(self, key: str, val: str, parent=None):
        label, input_ = self.USUAL_PRODUCT_INPUTS.get(key)
        self._verify_visible_element(label, parent=parent)
        self._verify_visible_element(input_, parent=parent).send_keys(val)
        return self

    def set_product_name(self, val: str):
        return self._set_usual_input('name', val, parent=self._tab_general_content())

    def set_meta_tag(self, val: str):
        return self._set_usual_input('meta_tag', val, parent=self._tab_general_content())

    def set_model(self, val: str):
        return self._set_usual_input('model', val, parent=self._tab_data_content())

    def select(self, *indexes):
        _form_product = self._form_product()
        checkboxes = self._verify_visible_elements(self.PRODUCT_LIST_CHECKBOXES, parent=_form_product)
        for i in indexes:
            checkboxes[i].click()
        return self


if __name__ == '__main__':
    pass
