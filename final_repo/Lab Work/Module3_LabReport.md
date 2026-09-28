# Module 3 - Lab Report: BDD with Behave

## Objective
Set up a Python BDD framework using Behave, wire it to Selenium for an
end-to-end scenario, extend it with data-driven scenarios, and combine it
with the Page Object Model from Module 2.

## Tools Used
Python 3, Behave, Selenium WebDriver, Requests

---

## Assignment 1: Selenium + Behave BDD Setup
**Task:** Set up a working Python BDD framework wired to Selenium for an
end-to-end login scenario.

**features/login.feature**
```gherkin
Feature: Selenium + Behave BDD Setup
  As a QA engineer
  I want a working Python BDD framework wired to Selenium
  So that I can run and debug an end-to-end browser scenario

  Scenario: Successful login on SauceDemo
    Given the browser is open on the SauceDemo login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page
```

**features/steps/login_steps.py**
```python
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@given('the browser is open on the SauceDemo login page')
def step_open_browser(context):
    options = Options()
    context.driver = webdriver.Chrome(options=options)
    context.driver.get("https://www.saucedemo.com/")


@when('I log in with username "{username}" and password "{password}"')
def step_login(context, username, password):
    context.driver.find_element(By.ID, "user-name").send_keys(username)
    context.driver.find_element(By.ID, "password").send_keys(password)
    context.driver.find_element(By.ID, "login-button").click()


@then('I should be redirected to the inventory page')
def step_check_redirect(context):
    assert "/inventory.html" in context.driver.current_url
    context.driver.quit()
```

**Result:** `behave` runs the scenario end-to-end: opens the browser, logs
in, and asserts the redirect.

---

## Assignment 2: Data-Driven Automation in Behave
**Task:** Use a Scenario Outline with an Examples table to run the same
scenario against multiple data sets (adapted here for API automation).

**features/api_ddt.feature**
```gherkin
Feature: Data-Driven API Automation with Behave
  As a QA engineer
  I want to run the same API scenario against multiple data sets
  So that I can validate several user IDs without duplicating scenarios

  Scenario Outline: Fetch a user by ID and validate the response
    Given the API is available
    When I request user with id <user_id>
    Then the response status code should be <expected_status>

    Examples: Valid and invalid user IDs
      | user_id | expected_status |
      | 1       | 200              |
      | 2       | 200              |
      | 9999    | 404              |
```

**features/steps/api_ddt_steps.py**
```python
from behave import given, when, then
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@given('the API is available')
def step_api_available(context):
    context.base_url = BASE_URL


@when('I request user with id {user_id}')
def step_get_user(context, user_id):
    context.response = requests.get(f"{context.base_url}/users/{user_id}", timeout=10)


@then('the response status code should be {status_code:d}')
def step_check_status(context, status_code):
    actual = context.response.status_code
    assert actual == status_code, f"Expected {status_code}, got {actual}"
```

**Result:** All three data rows executed as separate scenarios from one
Gherkin definition, returning the correct status code for each ID.

---

## Assignment 3: Selenium POM in the Behave Framework
**Task:** Combine the Page Object Model with Behave step definitions.

**pages/login_page.py**
```python
from selenium.webdriver.common.by import By


class LoginPage:
    URL = "https://www.saucedemo.com/"
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
```

**features/pom_login.feature**
```gherkin
Feature: Selenium Page Object Model inside the Behave Framework
  As a QA engineer
  I want the Behave steps to use Page Object classes instead of raw locators
  So that the automation stays maintainable using Gherkin + POM together

  Scenario: Login using the Page Object Model
    Given I am on the SauceDemo login page
    When I log in as "standard_user" with password "secret_sauce"
    Then I should land on the inventory page
```

**features/steps/pom_login_steps.py**
```python
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage


@given('I am on the SauceDemo login page')
def step_open_login_page(context):
    options = Options()
    context.driver = webdriver.Chrome(options=options)
    context.login_page = LoginPage(context.driver)
    context.login_page.open()


@when('I log in as "{username}" with password "{password}"')
def step_login_via_pom(context, username, password):
    context.login_page.login(username, password)


@then('I should land on the inventory page')
def step_verify_inventory(context):
    assert "/inventory.html" in context.driver.current_url
    context.driver.quit()
```

**Result:** Combined the readability of Gherkin with the maintainability
of POM - locators live in one place even though the test is described in
plain English.

## Observations
Gherkin's `Scenario Outline` + `Examples` is a clean way to express
data-driven tests without a manual loop. Reusing the same Page Object
class across both PyTest (Module 2) and Behave confirmed POM classes are
framework-agnostic.

## Conclusion
Module 3 layers BDD readability on top of the Selenium and POM work from
the earlier modules.
