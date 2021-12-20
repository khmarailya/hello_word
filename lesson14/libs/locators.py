from selenium.webdriver.common.by import By


class Locator:

    def __init__(self):
        self._res = ''

    @classmethod
    def _css(cls, s: str):
        def _get(self: 'CSS') -> 'CSS':
            self._res += s
            return self

        return property(_get)

    @classmethod
    def _xpath_tag(cls, s: str):
        def _get(self: 'XPATH') -> 'XPATH':
            return self._set_tag(s)

        return property(_get)

    @classmethod
    def _xpath_node(cls, s: str):
        def _get(self: 'XPATH') -> 'XPATH':
            return self._close_open_node(s)

        return property(_get)


class CSS(Locator):

    @property
    def res(self):
        return By.CSS_SELECTOR, self._res

    child: 'CSS' = Locator._css(' > ')
    header: 'CSS' = Locator._css('header')
    descendant: 'CSS' = Locator._css(' ')
    a: 'CSS' = Locator._css('a')
    ul: 'CSS' = Locator._css('ul')
    input: 'CSS' = Locator._css('input')
    li: 'CSS' = Locator._css('li')
    button: 'CSS' = Locator._css('button')
    body: 'CSS' = Locator._css('body')
    div: 'CSS' = Locator._css('div')
    tbody: 'CSS' = Locator._css('tbody')
    strong: 'CSS' = Locator._css('strong')

    def id(self, s: str):
        self._res += '#' + s
        return self

    def classes(self, *args):
        for c in args:
            self._res += '.' + c
        return self

    def attr(self, a: str, val: str):
        self._res += '[' + a + '="' + val + '"]'
        return self


class XPATH(Locator):
    TAG_ANY = '*'

    def __init__(self):
        super().__init__()
        self._node_is_open = False
        self._tag_conditions = []
        self._cur_tag = None

    def _close_node(self):
        if self._tag_conditions:
            tag = self._cur_tag or self.TAG_ANY
            self._res += tag + '[' + ' and '.join(self._tag_conditions) + ']'
            self._tag_conditions = []
        elif self._cur_tag is not None:
            self._res += self._cur_tag

        self._cur_tag = None
        self._node_is_open = False

    def _open_node(self, node=''):
        self._res += '//' + node
        self._node_is_open = True
        return self

    def _close_open_node(self, node: str, tag: str = None):
        self._close_node()
        self._open_node(node)
        self._cur_tag = tag
        return self

    def _set_tag(self, tag: str):
        if self._cur_tag is not None:
            self._close_node()

        if not self._node_is_open:
            self._open_node()

        self._cur_tag = tag
        return self

    def _add_tag_conditions(self, *args):
        if not self._node_is_open:
            self._open_node()

        self._tag_conditions += list(args)
        return self

    @staticmethod
    def _contain_exact(tag: str, val: str):
        return 'contains(concat(" ", normalize-space(@' + tag + '), " "), " ' + val + ' ")'

    @property
    def res(self) -> tuple:
        self._close_node()
        return By.XPATH, self._res

    child: 'XPATH' = Locator._xpath_node('child::')
    descendant: 'XPATH' = Locator._xpath_node('')

    any: 'XPATH' = Locator._xpath_tag(TAG_ANY)
    ul: 'XPATH' = Locator._xpath_tag('ul')
    li: 'XPATH' = Locator._xpath_tag('li')
    body: 'XPATH' = Locator._xpath_tag('body')
    label: 'XPATH' = Locator._xpath_tag('label')
    input: 'XPATH' = Locator._xpath_tag('input')
    button: 'XPATH' = Locator._xpath_tag('button')
    h2: 'XPATH' = Locator._xpath_tag('h2')
    h3: 'XPATH' = Locator._xpath_tag('h3')
    tbody: 'XPATH' = Locator._xpath_tag('tbody')

    def id(self, val: str):
        return self._add_tag_conditions(f'@id="{val}"')

    def text(self, val: str):
        return self._add_tag_conditions(f'text()="{val}"')

    def content(self, val: str):
        return self._add_tag_conditions(f'.="{val}"')

    def for_(self, val: str):
        return self._add_tag_conditions(f'@for="{val}"')

    def name(self, val: str):
        return self._add_tag_conditions(f'@name="{val}"')

    def type(self, val: str):
        return self._add_tag_conditions(f'@type="{val}"')

    def classes(self, *args):
        args = tuple(self._contain_exact('class', arg) for arg in args)
        return self._add_tag_conditions(*args)
