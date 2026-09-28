# Module 2 - Lab Report: Test Design & Reporting

## Objective
Restructure Selenium scripts into a maintainable framework using the Page
Object Model, add data-driven testing from an external file, and
integrate PyTest with automated HTML reporting.

## Tools Used
Python 3, Selenium WebDriver, PyTest, pytest-html

---

## Experiment 1: Page Object Model (POM) Restructure
**Task:** Restructure the Module 1 login script into POM - page classes
hold only locators and UI actions, test files hold the assertions.

**pages/login_page.py**
```python
from selenium.webdriver.common.by import By


class LoginPage:
    URL = "https://www.saucedemo.com/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_text(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text
```

**pages/dashboard_page.py**
```python
from selenium.webdriver.common.by import By


class DashboardPage:
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    PAGE_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self):
        return len(self.driver.find_elements(*self.INVENTORY_CONTAINER)) > 0

    def get_page_title(self):
        return self.driver.find_element(*self.PAGE_TITLE).text
```

**tests/test_login_pom.py**
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_valid_login_lands_on_dashboard():
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        login_page = LoginPage(driver).open()
        login_page.login("standard_user", "secret_sauce")

        dashboard_page = DashboardPage(driver)
        assert dashboard_page.is_loaded(), "Inventory page did not load"
        assert dashboard_page.get_page_title() == "Products"
        print("PASSED: Valid login lands on the Products dashboard")

    finally:
        driver.quit()


def test_invalid_login_shows_error():
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        login_page = LoginPage(driver).open()
        login_page.login("standard_user", "wrong_password")

        error_text = login_page.get_error_text()
        assert "Username and password do not match" in error_text
        print("PASSED: Invalid login correctly shows an error ->", error_text)

    finally:
        driver.quit()
```

**Result:** Same login behaviour as Module 1's script, now reusable
across multiple test files without duplicating locators.

---

## Experiment 2: Data-Driven Automation (DDT)
**Task:** Read multiple login test cases from an external CSV file and
loop through valid/invalid combinations.

**data/login_data.csv**
```
username,password,expected_result
standard_user,secret_sauce,success
locked_out_user,secret_sauce,locked_out
standard_user,wrong_password,invalid_credentials
,secret_sauce,missing_username
standard_user,,missing_password
```

**test_ddt_login.py**
```python
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "login_data.csv")


def load_test_data():
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run_login_attempt(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def test_data_driven_login():
    test_cases = load_test_data()
    options = Options()

    for case in test_cases:
        driver = webdriver.Chrome(options=options)
        try:
            run_login_attempt(driver, case["username"], case["password"])

            expected = case["expected_result"]

            if expected == "success":
                assert "/inventory.html" in driver.current_url, case
                print(f"PASSED [{case}] -> reached inventory page")
            else:
                error_el = driver.find_elements(By.CSS_SELECTOR, "[data-test='error']")
                assert len(error_el) > 0, f"Expected an error for case: {case}"
                print(f"PASSED [{case}] -> error shown: {error_el[0].text}")

        finally:
            driver.quit()
```

**Result:** All five data rows produced the expected outcome without
hardcoding credentials into the test logic.

---

## Experiment 3: PyTest Integration with HTML Reporting
**Task:** Convert scripts to PyTest with fixtures for setup/teardown,
auto-generating an HTML report with screenshots on failure.

**conftest.py**
```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            try:
                screenshot = driver_fixture.get_screenshot_as_base64()
                extra = getattr(report, "extra", [])
                try:
                    import pytest_html
                    extra.append(pytest_html.extras.image(screenshot))
                    report.extra = extra
                except ImportError:
                    pass
            except Exception:
                pass
```

**test_pytest_html.py**
```python
from selenium.webdriver.common.by import By


def test_login_success(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    assert "/inventory.html" in driver.current_url


def test_login_failure_shows_error(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "Username and password do not match" in error.text
```

**Run command:** `pytest --html=report.html --self-contained-html`

**Result:** A single self-contained HTML report generated after each run,
showing pass/fail status per test with failure screenshots embedded.

## Observations
Moving locators into Page Object classes made the DDT and PyTest tests
shorter to write. Fixtures removed a whole category of "forgot to quit
the driver" bugs.

## Conclusion
Module 2 turns individual Module 1 scripts into a structured, reusable
framework with proper reporting.
