from lesson18.libs.locators import CSS
from lesson18.libs.page_object.BasePage import BasePage, screen_step


class Top(BasePage):
    """ #top находится на каждой странице магазина """

    SELF = CSS().body.child.id('top').res
    CURRENCY_GROUP_BTN = CSS().id('form-currency').child.classes('btn-group').res
    CURRENCY_TITLE = CSS().button.classes('dropdown-toggle').child.strong.res
    CURRENCY_PANEL = CSS().classes('btn-group').child.ul.classes('dropdown-menu').res
    CURRENCY_BTN = CSS().button.classes('currency-select').res

    CURRENCY_INFO = {'EUR': ('€ Euro', '€'), 'GBP': ('£ Pound Sterling', '£'), 'USD': ('$ US Dollar', '$')}

    # xpath про запас
    # SELF = XPATH().body.child.id('top').res
    # CURRENCY_BTN = XPATH().id('form-currency').child.classes('btn-group').res
    # CURRENCY_PANEL = XPATH().child.ul.classes('dropdown-menu').res

    @BasePage.cache
    def _currency_group_btn(self, **kwargs):
        return self._verify_visible_element(self.CURRENCY_GROUP_BTN)

    @BasePage.cache
    def _currency_panel(self, **kwargs):
        return self._verify_visible_element(self.CURRENCY_PANEL, parent=self._currency_group_btn(**kwargs))

    @BasePage.cache
    def _currency_btns(self, **kwargs):
        return self._verify_visible_elements(self.CURRENCY_BTN, parent=self._currency_panel(**kwargs))

    @screen_step('Show currency')
    def show_currency(self):
        btn = self._currency_group_btn()
        self._click_element(btn)
        self._currency_panel()

        btns = self._currency_btns()
        name_text_list = set((btn.get_attribute('name'), btn.text) for btn in btns)
        assert len(name_text_list) == 3, ''

        asserts = [(name, info[0]) for name, info in self.CURRENCY_INFO.items()
                   if (name, info[0]) not in name_text_list]
        assert not asserts, f'Can\'t find currency {asserts}'
        return self

    @screen_step('Set currency {name}')
    def set_currency(self, name: str):
        btns = self._currency_btns()
        list(filter(lambda x: x.get_attribute('name') == name, btns))[0].click()
        self._reini()
        text = self._verify_visible_element(self.CURRENCY_TITLE, parent=self._currency_group_btn()).text
        assert text == self.CURRENCY_INFO[name][1], 'Incorrect currency title'
        return self
