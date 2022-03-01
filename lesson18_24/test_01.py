import allure

from lesson18.libs.element.AdminLoginForm import AdminLoginForm
from lesson18.libs.element.Header import Header
from lesson18.libs.element.Menu import Menu
from lesson18.libs.element.Top import Top
from lesson18.libs.helpers import random_email, random_phone
from lesson18.libs.page_object.AdminProductPage import AdminProductPage
from lesson18.libs.page_object.Catalogue import CataloguePage
from lesson18.libs.page_object.MainPage import MainPage
from lesson18.libs.page_object.RegisterPage import RegisterPage


class TestRunAll:

    @allure.feature('Main Page')
    @allure.story('Check elements')
    @allure.title('Check all elements')
    def test_main_page(self, main_page):
        Top(main_page) \
            .show_currency() \
            .set_currency('GBP')
        Header(main_page) \
            .check_logo() \
            .check_cart(Top.CURRENCY_INFO['GBP'][1]) \
            .check_search()
        Menu(main_page) \
            .check_buttons()
        MainPage(main_page) \
            .check_content() \
            .check_slideshow() \
            .check_feature()

    @allure.feature('Catalogue Page')
    @allure.story('Check elements')
    @allure.title('Check all elements')
    def test_catalogue(self, catalogue_page):
        Top(catalogue_page) \
            .show_currency() \
            .set_currency('USD')
        Header(catalogue_page) \
            .check_logo() \
            .check_cart(Top.CURRENCY_INFO['USD'][1]) \
            .check_search()
        Menu(catalogue_page) \
            .check_buttons()
        CataloguePage(catalogue_page) \
            .check_category() \
            .check_column_left() \
            .check_content()

    @allure.feature('Register Page')
    @allure.story('Register new user')
    @allure.title('Register random user')
    def test_register(self, register_page):
        Top(register_page) \
            .show_currency() \
            .set_currency('EUR')
        Header(register_page) \
            .check_logo() \
            .check_cart(Top.CURRENCY_INFO['EUR'][1]) \
            .check_search()
        Menu(register_page) \
            .check_buttons()
        RegisterPage(register_page) \
            .set_firstname('firstname') \
            .set_lastname('lastname') \
            .set_email(random_email()) \
            .set_telephone(random_phone()) \
            .set_password('12345678') \
            .set_confirm('12345678') \
            .agree() \
            .continue_()

    @allure.feature('Product Page')
    @allure.story('Add products')
    @allure.title('Add new product')
    def test_add_new_product(self, admin_products_page):
        AdminLoginForm(admin_products_page) \
            .login('demo', 'demo')
        AdminProductPage(admin_products_page) \
            .check_loaded() \
            .add_new() \
            .open_general() \
            .set_product_name('new product') \
            .set_meta_tag('new meta') \
            .open_data() \
            .set_model('new model') \
            .save()

    @allure.feature('Product Page')
    @allure.story('Delete products')
    @allure.title('Delete many products')
    def test_delete_product(self, admin_products_page):
        AdminLoginForm(admin_products_page) \
            .login('demo', 'demo')
        AdminProductPage(admin_products_page) \
            .check_loaded() \
            .select(0, 1, 2) \
            .delete()


if __name__ == '__main__':
    pass
