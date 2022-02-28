from lesson18.libs.locators import CSS, XPATH
from lesson18.libs.page_object.BasePage import BasePage, screen_step


class CataloguePage(BasePage):
    PRODUCT_CATEGORY = CSS().id('product-category').res
    CATEGORY_PATH = CSS().ul.classes('breadcrumb').res
    COLUMN_LEFT = CSS().id('column-left').res
    CONTENT = CSS().id('content').res
    CONTENT_TITLE = XPATH().h2.text('{}').res

    @screen_step('Check category')
    def check_category(self):
        product_category = self._verify_visible_element(self.PRODUCT_CATEGORY)
        self._verify_visible_element(self.CATEGORY_PATH, parent=product_category)
        return self

    @screen_step('Check column left')
    def check_column_left(self):
        self._verify_visible_element(self.COLUMN_LEFT)
        return self

    @screen_step('Check content')
    def check_content(self):
        content = self._verify_visible_element(self.CONTENT)
        locator = list(self.CONTENT_TITLE)
        locator[1] = locator[1].format(self._driver.title)
        self._verify_visible_element(tuple(locator), parent=content)
        return self


if __name__ == '__main__':
    pass
