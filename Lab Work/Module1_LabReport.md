# Module 1 - Lab Report: Selenium Core & Advanced Interactions

## Objective
Build and validate six independent Selenium scripts covering element
location strategies, explicit waits, dynamic UI controls, JavaScript
dialogs, table data extraction, and window/tab/iframe handling.

## Tools Used
Python 3, Selenium WebDriver, ChromeDriver

---

## Experiment 1: The Multi-Locator Challenge
**Task:** Log into SauceDemo using `By.ID` for username, `By.NAME` for
password, and `By.XPATH` for the login button. Validate the resulting
URL contains `/inventory.html`.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_multi_locator_login():
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.saucedemo.com/")

        username_field = driver.find_element(By.ID, "user-name")
        username_field.send_keys("standard_user")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("secret_sauce")

        login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
        login_button.click()

        assert "/inventory.html" in driver.current_url, (
            f"Expected /inventory.html in URL, got: {driver.current_url}"
        )
        print("PASSED: Logged in successfully, URL contains /inventory.html")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_multi_locator_login()
```

**Result:** Login succeeded; assertion on `/inventory.html` passed.

---

## Experiment 2: Synchronization & Explicit Waits
**Task:** Navigate to a page with dynamic content and wait until it
appears, without using `time.sleep()`.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def test_explicit_wait_dynamic_loading():
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

        start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
        start_button.click()

        wait = WebDriverWait(driver, 10)
        finish_text = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))
        )

        assert finish_text.text == "Hello World!", (
            f"Expected 'Hello World!', got: {finish_text.text}"
        )
        print(f"PASSED: Dynamic text appeared and matched -> '{finish_text.text}'")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_explicit_wait_dynamic_loading()
```

**Result:** Text "Hello World!" correctly captured after the explicit wait.

---

## Experiment 3: Dynamic Dropdowns & Checkboxes
**Task:** Select checkboxes and verify their state; type into an
autocomplete field and select a matching suggestion.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def test_checkboxes_and_autocomplete():
    options = Options()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://rahulshettyacademy.com/AutomationPractice/")

        checkbox1 = driver.find_element(By.ID, "checkBoxOption1")
        checkbox2 = driver.find_element(By.ID, "checkBoxOption2")

        checkbox1.click()
        assert checkbox1.is_selected(), "checkBoxOption1 should be selected"
        print("PASSED: checkBoxOption1 is selected")

        checkbox2.click()
        assert checkbox2.is_selected(), "checkBoxOption2 should be selected"
        print("PASSED: checkBoxOption2 is selected")

        autocomplete_input = driver.find_element(By.ID, "autocomplete")
        autocomplete_input.send_keys("Ind")

        suggestions = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ui-menu-item div"))
        )

        target_found = False
        for suggestion in suggestions:
            if suggestion.text.strip().lower() == "india":
                suggestion.click()
                target_found = True
                break

        assert target_found, "Expected to find and select 'India' from suggestions"
        print("PASSED: 'India' selected from autocomplete suggestions")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_checkboxes_and_autocomplete()
```

**Result:** Both checkboxes verified selected; "India" correctly chosen
from the autocomplete list.

---

## Experiment 4: JavaScript Alerts and Confirms
**Task:** Trigger and handle a JS Alert, Confirm box, and Prompt box.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def test_js_alerts_confirm_prompt():
    options = Options()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/javascript_alerts")

        driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
        alert = wait.until(EC.alert_is_present())
        assert alert.text == "I am a JS Alert"
        alert.accept()
        result = driver.find_element(By.ID, "result").text
        assert result == "You successfully clicked an alert"
        print("PASSED: JS Alert accepted ->", result)

        driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
        confirm_alert = wait.until(EC.alert_is_present())
        assert confirm_alert.text == "I am a JS Confirm"
        confirm_alert.dismiss()
        result = driver.find_element(By.ID, "result").text
        assert result == "You clicked: Cancel"
        print("PASSED: JS Confirm dismissed ->", result)

        driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
        prompt_alert = wait.until(EC.alert_is_present())
        prompt_alert.send_keys("Hello from Selenium")
        prompt_alert.accept()
        result = driver.find_element(By.ID, "result").text
        assert "Hello from Selenium" in result
        print("PASSED: JS Prompt submitted with text ->", result)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_js_alerts_confirm_prompt()
```

**Result:** Each dialog's resulting message matched the expected
accept/dismiss/text-entry outcome.

---

## Experiment 5: The HTML Web Table Extractor
**Task:** Iterate a data table and extract a value by matching a row.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_extract_table_value():
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://the-internet.herokuapp.com/tables")

        table = driver.find_element(By.ID, "table1")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        target_last_name = "Bach"
        due_value = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            last_name = cells[0].text.strip()
            if last_name == target_last_name:
                due_value = cells[3].text.strip()
                break

        assert due_value is not None, f"Row with last name '{target_last_name}' not found"
        print(f"PASSED: Due amount for '{target_last_name}' is {due_value}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_extract_table_value()
```

**Result:** Correct due amount extracted for the target row.

---

## Experiment 6: Windows, Tabs, and Iframes
**Task:** Interact inside an iframe, then open, switch to, read from,
close, and switch back from a new browser tab.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def test_iframe_and_new_tab():
    options = Options()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://the-internet.herokuapp.com/iframe")
        driver.switch_to.frame("mce_0_ifr")

        editor_body = driver.find_element(By.ID, "tinymce")
        editor_body.clear()
        editor_body.send_keys("Selenium can type inside an iframe!")

        assert "Selenium can type inside an iframe!" in editor_body.text
        print("PASSED: Typed inside the iframe editor")

        driver.switch_to.default_content()

        driver.get("https://the-internet.herokuapp.com/windows")
        main_window = driver.current_window_handle

        driver.find_element(By.LINK_TEXT, "Click Here").click()

        wait.until(EC.number_of_windows_to_be(2))
        all_windows = driver.window_handles
        new_window = [w for w in all_windows if w != main_window][0]

        driver.switch_to.window(new_window)
        new_tab_title = driver.title
        assert new_tab_title == "New Window", f"Unexpected title: {new_tab_title}"
        print(f"PASSED: New tab opened with title '{new_tab_title}'")

        driver.close()
        driver.switch_to.window(main_window)
        assert driver.title == "The Internet"
        print("PASSED: Switched back to main window successfully")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_iframe_and_new_tab()
```

**Result:** Text entered inside the iframe; new tab title read correctly;
tab lifecycle handled cleanly.

## Observations
Explicit waits proved noticeably more reliable than fixed sleeps.
Switching context (iframe vs. default content, window handles) requires
explicit `switch_to` calls at every boundary.

## Conclusion
All six Module 1 scripts run independently and validate their expected
outcome with assertions.
