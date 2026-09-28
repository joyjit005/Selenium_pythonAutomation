from behave import given, when, then
from utils.api_client import APIClient


@given('the API is available')
def step_api_available(context):
    context.client = APIClient()


@when('I request all users')
def step_get_all_users(context):
    context.response = context.client.get("/users")


@when('I request user with id {user_id}')
def step_get_user(context, user_id):
    context.response = context.client.get(f"/users/{user_id}")


@when('I create a new user with name "{name}" and email "{email}"')
def step_create_user(context, name, email):
    payload = {"name": name, "email": email}
    context.response = context.client.post("/users", data=payload)


@when('I update user with id {user_id} with name "{name}"')
def step_update_user(context, user_id, name):
    payload = {"name": name}
    context.response = context.client.put(f"/users/{user_id}", data=payload)


@when('I delete user with id {user_id}')
def step_delete_user(context, user_id):
    context.response = context.client.delete(f"/users/{user_id}")


@then('the response status code should be {status_code:d}')
def step_check_status(context, status_code):
    actual = context.response.status_code
    assert actual == status_code, f"Expected {status_code}, got {actual}"


@then('the response should contain a list of users')
def step_check_list(context):
    data = context.response.json()
    assert isinstance(data, list) and len(data) > 0


@then('the response should contain user details')
def step_check_user_details(context):
    data = context.response.json()
    assert "id" in data and "name" in data


@then('the response should contain the created user id')
def step_check_created_id(context):
    data = context.response.json()
    assert "id" in data


@then('the response should reflect the updated name')
def step_check_updated_name(context):
    data = context.response.json()
    assert data.get("name") == "Jane Doe"
