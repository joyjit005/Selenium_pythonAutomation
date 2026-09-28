# Capstone Project - Report: API Automation Framework

## Objective
Build a reusable API automation framework using Python's Requests
library and the Behave BDD framework, covering full CRUD operations
against a User Management API, with Allure reporting integrated.

## Tools Used
Python 3, Requests, Behave, Allure

## Approach

### Framework Design
- `config/config.py` centralizes the base URL, headers, and timeout so
  the entire suite can be pointed at a different environment by editing
  one file.
- `utils/api_client.py` wraps `requests.get/post/put/delete` inside an
  `APIClient` class, so no test talks to `requests` directly.
- `features/user_management.feature` describes six scenarios in Gherkin:
  get all users, get one user, create, update, delete, and a negative
  test (404 on a non-existent user).
- `features/steps/user_steps.py` implements each Gherkin line, calling
  `APIClient` and asserting on the response.
- `features/environment.py` provides suite-level hooks (`before_all`,
  `after_scenario`, `after_all`) for logging and structure, kept
  separate from the step logic itself.

### Execution
```bash
pip install -r requirements.txt
behave
```
Optional Allure reporting:
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

## Results
All six scenarios pass against the live JSONPlaceholder API:
- GET `/users` returns a non-empty list (200)
- GET `/users/1` returns full user details (200)
- POST `/users` returns a created user with an `id` (201)
- PUT `/users/1` reflects the updated name (200)
- DELETE `/users/1` succeeds (200)
- GET `/users/9999` correctly returns 404, confirming the framework
  validates error handling and not just the happy path

## Observations
- Centralizing the base URL and headers in one config file made it clear
  how little would need to change to point the framework at a real,
  authenticated API instead of a public mock.
- Writing the assertions in Gherkin's plain English made the test
  intent readable without needing to open the underlying Python.

## Conclusion
The framework demonstrates a maintainable, readable approach to API test
automation - Gherkin scenarios stay decoupled from the HTTP mechanics,
which live entirely inside the `APIClient` wrapper.
