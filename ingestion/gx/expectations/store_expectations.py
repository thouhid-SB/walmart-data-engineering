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


def create_store_suite():
    suite = gx.ExpectationSuite(name="stores_suite")

    required_columns = [
        "store_id", "store_name", "city", "province", "country",
        "created_timestamp", "updated_timestamp", "is_active",
    ]
    for column in required_columns:
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column=column))

    suite.add_expectation(ExpectColumnValuesToBeUnique(column="store_id"))
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(column="country", value_set=["India"])
    )
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(column="is_active", value_set=["Y", "N"])
    )

    return suite
