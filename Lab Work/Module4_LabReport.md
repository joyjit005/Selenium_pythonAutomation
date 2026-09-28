# Module 4 - Lab Report: Robot Framework

## Objective
Get hands-on with Robot Framework's core syntax, variables, custom
keywords, assertions, setup/teardown hooks, tagging, and reporting.

## Tools Used
Python 3, Robot Framework, SeleniumLibrary, RequestsLibrary

---

## 1. Basic Syntax and Keywords
**Task:** Open a browser and navigate to a URL, fill a field using
`Input Text`, and verify an element's presence using
`Page Should Contain Element`.

**basic_syntax.robot**
```robotframework
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Open Browser And Navigate To URL
    Open Browser    https://www.saucedemo.com/    chrome
    Maximize Browser Window
    [Teardown]    Close Browser

Fill Form Field Using Input Text
    Open Browser    https://www.saucedemo.com/    chrome
    Input Text    id=user-name    standard_user
    [Teardown]    Close Browser

Verify Element Presence On Page
    Open Browser    https://www.saucedemo.com/    chrome
    Page Should Contain Element    id=login-button
    [Teardown]    Close Browser
```

**Result:** Browser opens and navigates correctly; text entered into the
username field; login button confirmed present on the page.

---

## 2. Variables and Data-Driven Automation
**Task:** Use variables to store credentials, and run a data-driven test
that reads test data from an external file.

**login_data.py** (external variable file)
```python
LOGIN_CASES = [
    {"username": "standard_user", "password": "secret_sauce", "expected": "success"},
    {"username": "locked_out_user", "password": "secret_sauce", "expected": "locked_out"},
    {"username": "standard_user", "password": "wrong_password", "expected": "invalid_credentials"},
]
```

**variables_ddt.robot**
```robotframework
*** Settings ***
Library      SeleniumLibrary
Variables    login_data.py

*** Variables ***
${USERNAME}    standard_user
${PASSWORD}    secret_sauce
${URL}         https://www.saucedemo.com/

*** Test Cases ***
Login Using Variables
    Open Browser    ${URL}    chrome
    Input Text    id=user-name    ${USERNAME}
    Input Text    id=password    ${PASSWORD}
    Click Button    id=login-button
    Location Should Contain    inventory.html
    [Teardown]    Close Browser

Data Driven Login From External File
    FOR    ${case}    IN    @{LOGIN_CASES}
        Open Browser    ${URL}    chrome
        Input Text    id=user-name    ${case}[username]
        Input Text    id=password    ${case}[password]
        Click Button    id=login-button
        Run Keyword If    '${case}[expected]' == 'success'
        ...    Location Should Contain    inventory.html
        ...    ELSE
        ...    Page Should Contain Element    css:[data-test='error']
        Close Browser
    END
```

**Result:** Login using stored variables succeeds; the external-file-driven
loop correctly handles both the success case and the two failure cases.

---

## 3. Custom Keywords and Libraries
**Task:** Build a custom Robot Framework keyword using Python, and use
the BuiltIn/String libraries for string and math operations.

**MathKeywords.py** (custom Python keyword library)
```python
def add_numbers(a, b):
    """Custom Robot Framework keyword: sums two numbers."""
    return float(a) + float(b)
```

**custom_keywords.robot**
```robotframework
*** Settings ***
Library    MathKeywords.py
Library    BuiltIn
Library    String

*** Test Cases ***
Use Custom Python Keyword To Add Numbers
    ${result}=    Add Numbers    5    7
    Should Be Equal As Numbers    ${result}    12

Use Library Keywords For String And Math Operations
    ${upper}=    Convert To Upper Case    hello robot
    Should Be Equal    ${upper}    HELLO ROBOT
    ${sum}=    Evaluate    10 + 25
    Should Be Equal As Integers    ${sum}    35
```

**Result:** Custom `Add Numbers` keyword correctly sums two values;
built-in string/math operations produce the expected results.

---

## 4. Assertions and Verification
**Task:** Perform an action and assert the outcome; verify an API
response using `Should Be Equal As Strings`.

**assertions.robot**
```robotframework
*** Settings ***
Library    SeleniumLibrary
Library    RequestsLibrary

*** Test Cases ***
Action Then Assert Outcome
    Open Browser    https://www.saucedemo.com/    chrome
    Input Text    id=user-name    standard_user
    Input Text    id=password    secret_sauce
    Click Button    id=login-button
    ${title}=    Get Text    css:.title
    Should Be Equal As Strings    ${title}    Products
    [Teardown]    Close Browser

Verify API Response With Should Be Equal As Strings
    Create Session    jsonplaceholder    https://jsonplaceholder.typicode.com
    ${response}=    GET On Session    jsonplaceholder    /users/1
    ${name}=    Set Variable    ${response.json()}[name]
    Should Be Equal As Strings    ${name}    Leanne Graham
```

**Result:** UI assertion confirms the "Products" title after login; API
assertion confirms the expected user name from the response JSON.

---

## 5. Test Setup and Teardown
**Task:** Set up a common test setup that logs in before tests, and a
teardown that logs out and cleans up.

**setup_teardown.robot**
```robotframework
*** Settings ***
Library           SeleniumLibrary
Suite Setup       Open Browser And Login
Suite Teardown    Logout And Close Browser

*** Test Cases ***
Verify Inventory Page After Suite Login
    Page Should Contain Element    id=inventory_container

*** Keywords ***
Open Browser And Login
    Open Browser    https://www.saucedemo.com/    chrome
    Input Text    id=user-name    standard_user
    Input Text    id=password    secret_sauce
    Click Button    id=login-button

Logout And Close Browser
    Click Element    id=react-burger-menu-btn
    Click Element    id=logout_sidebar_link
    Close Browser
```

**Result:** Suite setup logs in once before the test cases run; suite
teardown logs out and closes the browser cleanly afterward.

---

## 6. Tags and Test Execution
**Task:** Assign tags to test cases and run a subset using
`--include`/`--exclude`; run tests in parallel.

**tags_execution.robot**
```robotframework
*** Settings ***
Library       SeleniumLibrary
Force Tags    regression

*** Test Cases ***
Smoke Test Login
    [Tags]    smoke
    Open Browser    https://www.saucedemo.com/    chrome
    Input Text    id=user-name    standard_user
    Input Text    id=password    secret_sauce
    Click Button    id=login-button
    Location Should Contain    inventory.html
    [Teardown]    Close Browser

Full Regression Checkout Flow
    [Tags]    regression
    Log    Placeholder for a longer checkout regression flow
```

**Execution commands:**
```
robot --include smoke tags_execution.robot
robot --exclude regression tags_execution.robot
pabot --processes 2 tags_execution.robot
```
(Note: parallel execution with `--processes` requires the separate
`pabot` runner - vanilla `robot` does not support it directly.)

**Result:** `--include smoke` runs only the login test; `--exclude
regression` skips both since the suite carries a `regression` Force Tag;
`pabot` runs the suite's tests across 2 parallel processes.

---

## 7. Reports and Logs
**Task:** Generate an HTML report with test outcomes, and use the `Log`
keyword for custom debug messages.

**reports_logs.robot**
```robotframework
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Test With Custom Log Messages
    Log    Starting the reports and logging demonstration test
    Open Browser    https://www.saucedemo.com/    chrome
    Log    Browser opened, now attempting login
    Input Text    id=user-name    standard_user
    Input Text    id=password    secret_sauce
    Click Button    id=login-button
    Log    Login submitted, verifying redirect
    Location Should Contain    inventory.html
    Log    Test completed successfully    console=True
    [Teardown]    Close Browser
```

**Execution command:** `robot reports_logs.robot`

**Result:** Robot Framework automatically produces `report.html` and
`log.html` after every run; the custom `Log` messages appear in
`log.html` for debugging, and the `console=True` message also prints to
the terminal live.

## Observations
Robot Framework's keyword-driven syntax reads closer to plain English
than pytest/unittest, at the cost of needing exact keyword names and
argument ordering. Suite-level setup/teardown avoided repeating the login
steps in every test case.

## Conclusion
Module 4 covers the full breadth of Robot Framework fundamentals - from
basic keyword syntax to custom Python keywords, tagging, and native HTML
reporting - completing the automation stack alongside Selenium, PyTest,
and Behave from the earlier modules.
