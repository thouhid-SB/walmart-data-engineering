import great_expectations as gx

from great_expectations.expectations.core.expect_column_values_to_not_be_null import (
    ExpectColumnValuesToNotBeNull,
)
from great_expectations.expectations.core.expect_column_values_to_be_unique import (
    ExpectColumnValuesToBeUnique,
)
from great_expectations.expectations.core.expect_column_values_to_be_in_set import (
    ExpectColumnValuesToBeInSet,
)
from great_expectations.expectations.core.expect_column_values_to_be_between import (
    ExpectColumnValuesToBeBetween,
)
from great_expectations.expectations.core.expect_column_values_to_match_regex import (
    ExpectColumnValuesToMatchRegex,
)


def create_employee_suite():
    suite = gx.ExpectationSuite(name="employees_suite")

    required_columns = [
        "employee_id", "store_id", "first_name", "last_name", "email",
        "job_title", "salary", "created_timestamp", "updated_timestamp",
        "is_active",
    ]
    for column in required_columns:
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column=column))

    suite.add_expectation(ExpectColumnValuesToBeUnique(column="employee_id"))
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(column="salary", min_value=0)
    )
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(column="is_active", value_set=["Y", "N"])
    )
    suite.add_expectation(
        ExpectColumnValuesToMatchRegex(
            column="email",
            regex=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        )
    )

    return suite
