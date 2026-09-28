# API Automation Framework - User Management API

Python API automation framework built with **Requests + Behave (BDD)**,
targeting the User Management endpoints of `https://jsonplaceholder.typicode.com`.

## Tech Stack
- **Requests** - HTTP client for API calls
- **Behave** - BDD framework (Gherkin feature files -> step definitions)
- **Allure** - test execution reporting

## Project Structure
```
Capstone Project/
├── config/
│   └── config.py          # Base URL, headers, timeout - single source of truth
├── utils/
│   └── api_client.py      # Reusable wrapper around requests (GET/POST/PUT/DELETE)
├── features/
│   ├── user_management.feature   # Gherkin scenarios (CRUD on /users)
│   ├── environment.py            # Behave hooks (before_all/after_scenario/after_all)
│   └── steps/
│       └── user_steps.py         # Step definitions implementing the Gherkin steps
├── requirements.txt
├── behave.ini
├── README.md
├── Report.md
└── Video_Demo.md
```

## Setup
```bash
pip install -r requirements.txt
```

## Run the tests
```bash
behave
```

## Run with Allure reporting
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```
(Requires the Allure commandline tool installed separately - `npm install -g allure-commandline`.)

## What this covers
| Objective | Where |
|---|---|
| Python Requests Library | `utils/api_client.py` |
| REST API Testing (GET/POST/PUT/DELETE) | `features/steps/user_steps.py` |
| Authentication | `config/config.py` (Authorization header attached to every request) |
| Behave BDD Framework | `features/*.feature` + `features/steps/*.py` |
| Allure Reporting | Run command above |
| Reusable Framework Design | `APIClient` class + centralized `config.py` |

## Scenarios covered
1. Get all users (200 + list validation)
2. Get single user by ID (200 + payload validation)
3. Create a new user (201 + id returned)
4. Update an existing user (200 + field updated)
5. Delete a user (200)
6. Get a non-existent user (404 - negative test case)
