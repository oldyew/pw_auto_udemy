import os
import logging
import pytest
from settings import *
from pytest import fixture
from playwright.sync_api import sync_playwright
from page_objects.application import App


@fixture(autouse=True, scope='session')
def precondition():
    logging.info('preconditions started')
    yield
    logging.info('postconditions started')


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


# @fixture(scope='session', params=['chromium', 'firefox', 'webkit'], ids=['chromium', 'firefox', 'webkit'])
@fixture(scope='session', params=['chromium'])
def get_browser(get_playwright, request):
    browser = request.param
    # browser = request.config.getoption('--browser')
    os.environ['PWBROWSER'] = browser
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

    if browser == 'chromium':
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'unsupported browser type'

    yield bro
    bro.close()
    del os.environ['PWBROWSER']


@fixture(scope='session')
def desktop_app(get_browser):
    app = App(get_browser, base_url='http://127.0.0.1:8000', **BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app):
    app = desktop_app
    app.goto('/login')
    app.login('alice', 'Qamania123')
    yield app


@fixture(scope='session', params=['iPhone 11', 'Pixel 2'])
def mobile_app(get_playwright, get_browser, request):
    if os.environ.get('PWBROWSER') == 'firefox':
        pytest.skip()
    device = request.param
    # device = request.config.getoption('--device')
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
        device_config.update(BROWSER_OPTIONS)
    else:
        device_config = BROWSER_OPTIONS
    app = App(get_browser, base_url='http://127.0.0.1:8000', **device_config)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def mobile_app_auth(mobile_app):
    app = mobile_app
    app.goto('/login')
    app.login('alice', 'Qamania123')
    yield app


def pytest_addoption(parser):
    parser.addoption('--device', action='store', default='')
    parser.addoption('--browser', action='store', default='chromium')
    parser.addini('headless', help='run browser in headless mode', default='True')
