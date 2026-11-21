
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


def create_order_suite():
    suite = gx.ExpectationSuite(name="orders_suite")

    required_columns = [
        "order_id",
        "customer_id",
        "store_id",
        "order_timestamp",
        "payment_method",
        "order_status",
        "total_amount",
        "created_timestamp",
        "updated_timestamp",
        "is_active",
    ]

    for column in required_columns:
        suite.add_expectation(
            ExpectColumnValuesToNotBeNull(column=column)
        )

    suite.add_expectation(
        ExpectColumnValuesToBeUnique(column="order_id")
    )

    suite.add_expectation(
        ExpectColumnValuesToBeInSet(
            column="payment_method",
            value_set=[
                "Credit Card",
                "Debit Card",
                "Cash",
                "Gift Card",
                "Online",
                "UPI",
            ],
        )
    )

    suite.add_expectation(
        ExpectColumnValuesToBeInSet(
            column="order_status",
            value_set=[
                "Pending",
                "Cancelled",
                "Returned",
                "Completed",
                "Shipped",
                "Delivered",
            ],
        )
    )

    suite.add_expectation(
        ExpectColumnValuesToBeInSet(
            column="is_active",
            value_set=["Y", "N"],
        )
    )

    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="total_amount",
            min_value=0,
        )
    )

    return suite
