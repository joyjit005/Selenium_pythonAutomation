Feature: User Management API
  As a QA engineer
  I want to automate testing of the User Management API
  So that CRUD operations are verified without manual checking

  Scenario: Get all users
    Given the API is available
    When I request all users
    Then the response status code should be 200
    And the response should contain a list of users

  Scenario: Get a single user by ID
    Given the API is available
    When I request user with id 1
    Then the response status code should be 200
    And the response should contain user details

  Scenario: Create a new user
    Given the API is available
    When I create a new user with name "John Doe" and email "john.doe@example.com"
    Then the response status code should be 201
    And the response should contain the created user id

  Scenario: Update an existing user
    Given the API is available
    When I update user with id 1 with name "Jane Doe"
    Then the response status code should be 200
    And the response should reflect the updated name

  Scenario: Delete a user
    Given the API is available
    When I delete user with id 1
    Then the response status code should be 200

  Scenario: Get a non-existent user returns not found
    Given the API is available
    When I request user with id 9999
    Then the response status code should be 404
