from selenium.webdriver.support.wait import WebDriverWait


class Wait(WebDriverWait):
    """ my WebDriverWait """

    def __init__(self, driver, timeout=2, frequency=1):
        super().__init__(driver, timeout, poll_frequency=frequency)


class url_get(object):
    """An expectation for checking the current url.
    url is the expected url, which must be an exact match
    returns True if the url matches, false otherwise."""
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        driver.get(self.url)
        return self.url == driver.current_url


if __name__ == '__main__':
    pass
