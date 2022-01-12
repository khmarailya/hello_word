from ..locators import CSS
from ..page_object.BasePage import BasePage, screen_step


class Menu(BasePage):
    """ menu находится на каждой странице магазина """

    SELF = CSS().body.descendant.id('menu').res
    BUTTONS = CSS().classes('nav').child.li.res

    @screen_step('Check buttons')
    def check_buttons(self):
        btns = self._verify_visible_elements(self.BUTTONS)
        texts = set(btn.text for btn in btns)
        assert len(texts) == 8, 'Incorrect menu button count'

        asserts = [text for text in ('Desktops', 'Laptops & Notebooks', 'Components') if text not in texts]
        assert not asserts, f'Can\'t find menu buttons {asserts}'
        return self
