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


def create_customer_suite():
    suite = gx.ExpectationSuite(name="customers_suite")

    required_columns = [
        "customer_id", "first_name", "last_name", "email", "phone",
        "city", "province", "country", "created_timestamp",
        "updated_timestamp", "is_active",
    ]
    for column in required_columns:
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column=column))

    suite.add_expectation(ExpectColumnValuesToBeUnique(column="customer_id"))
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(column="country", value_set=["India"])
    )
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(column="is_active", value_set=["Y", "N"])
    )
    # The current pandas reader infers +91 phone values as integers.
    # This range represents +91 followed by a valid 10-digit Indian mobile number.
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="phone",
            min_value=916000000000,
            max_value=919999999999,
        )
    )
    suite.add_expectation(
        ExpectColumnValuesToMatchRegex(
            column="email",
            regex=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        )
    )

    return suite
