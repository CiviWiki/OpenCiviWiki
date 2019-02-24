import os
from contextlib import contextmanager

from aloe import around, world
from selenium import webdriver

'''
this method sets a global variable of type WebDriver. This is the browser.
@around.all is a global hook. It will be ran once before all scenarios
After the last scenario is completed (pass or fail) the WebDriver will be closed
'''


@around.all
@contextmanager
def with_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument("--no-sandbox")
    driver_path = os.path.dirname(os.path.realpath(__file__)) + "/utilities/chromedriver.exe"
    world.browser = webdriver.Chrome(executable_path=driver_path, options=options)
    yield
    world.browser.quit()
    delattr(world, 'browser')
