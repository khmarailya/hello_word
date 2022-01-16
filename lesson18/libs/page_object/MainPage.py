from ..locators import CSS, XPATH
from ..page_object.BasePage import BasePage, screen_step


class MainPage(BasePage):
    CONTENT = CSS().id('common-home').descendant.id('content').res
    SLIDESHOW = CSS().id('slideshow0').res
    FEATURE_TITLE = XPATH().h3.text('Featured').res
    FEATURES = CSS().div.classes('product-layout').res

    @BasePage.cache
    def _inner_element_content(self, renew=False):
        return self._verify_visible_element(self.CONTENT)

    @screen_step('Check content')
    def check_content(self):
        self._inner_element_content()
        return self

    @screen_step('Check slideshow')
    def check_slideshow(self):
        self._verify_visible_element(self.SLIDESHOW, parent=self._inner_element_content())
        return self

    @screen_step('Check feature')
    def check_feature(self):
        content = self._inner_element_content()
        self._verify_visible_element(self.FEATURE_TITLE, parent=content)
        features = self._verify_visible_elements(self.FEATURES, parent=content)
        assert len(features) == 4, 'Incorrect features length'
        return self


if __name__ == '__main__':
    pass
