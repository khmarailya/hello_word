from selenium.webdriver.support.wait import WebDriverWait


class Wait(WebDriverWait):
    """ my WebDriverWait """

    def __init__(self, driver, timeout=2, frequency=1):
        super().__init__(driver, timeout, poll_frequency=frequency)


if __name__ == '__main__':
    pass
