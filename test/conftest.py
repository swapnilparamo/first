import datetime
import os

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager



driver = None

# Set up the reports and screenshots directories
REPORTS_DIR = 'reports'
SCREENSHOTS_DIR = 'screenshots'

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)


# Command line option for browser selection
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests on")


@pytest.fixture()
def browser(request):
    global driver
    # selected_browser = request.config.getoption("browser")
    selected_browser = "firefox"

    if selected_browser == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https:\\www.cricbuzz.com")
        driver.maximize_window()
        driver.implicitly_wait(5)
        request.cls.driver = driver
        yield driver
        driver.quit()
    elif selected_browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
        driver.get("https:\\www.cricbuzz.com")
        driver.maximize_window()
        driver.implicitly_wait(5)
        request.cls.driver = driver
        yield driver
        driver.quit()
    else:
        raise ValueError(f"Browser {selected_browser} is not supported.")


# Function to capture screenshot
def take_screenshot(driver, method_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{method_name}_{timestamp}.png"
    screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
    driver.save_screenshot(screenshot_path)
    return screenshot_path


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        # Capture the screenshot when a test fails
        if hasattr(item, "funcargs"):
            driver = item.funcargs['browser']
            screenshot_path = take_screenshot(driver, item.name)
            report.extra = getattr(report, 'extra', [])
            report.extra.append(pytest_html.extras.image(screenshot_path))


# Function to create report with timestamp
def pytest_configure(config):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"report_{timestamp}.html"
    config.option.htmlpath = os.path.join(REPORTS_DIR, report_name)
