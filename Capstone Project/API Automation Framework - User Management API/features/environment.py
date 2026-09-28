"""
Behave hooks - run automatically before/after the test suite and each scenario.
Keeps cross-cutting concerns (logging, cleanup) out of the step files.
"""


def before_all(context):
    print("\n===== Starting API Automation Test Suite =====\n")


def after_scenario(context, scenario):
    if scenario.status == "failed":
        print(f"[FAILED] {scenario.name}")
    else:
        print(f"[PASSED] {scenario.name}")


def after_all(context):
    print("\n===== API Automation Test Suite Complete =====\n")
