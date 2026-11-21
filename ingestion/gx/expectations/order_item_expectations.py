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


def create_order_item_suite():
    suite = gx.ExpectationSuite(name="order_items_suite")

    required_columns = [
        "order_item_id", "order_id", "product_id", "quantity",
        "unit_price", "line_amount", "created_timestamp",
        "updated_timestamp", "is_active",
    ]
    for column in required_columns:
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column=column))

    suite.add_expectation(ExpectColumnValuesToBeUnique(column="order_item_id"))
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(column="quantity", min_value=1)
    )
    for column in ["unit_price", "line_amount"]:
        suite.add_expectation(
            ExpectColumnValuesToBeBetween(column=column, min_value=0)
        )
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(column="is_active", value_set=["Y", "N"])
    )

    return suite
