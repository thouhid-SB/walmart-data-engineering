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


def create_product_suite():
    suite = gx.ExpectationSuite(name="products_suite")

    required_columns = [
        "product_id", "product_name", "category", "brand", "price",
        "created_timestamp", "updated_timestamp", "is_active",
    ]
    for column in required_columns:
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column=column))

    suite.add_expectation(ExpectColumnValuesToBeUnique(column="product_id"))
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(
            column="category",
            value_set=["Electronics", "Clothing", "Grocery", "Sports", "Toys", "Home"],
        )
    )
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(column="price", min_value=0)
    )
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(column="is_active", value_set=["Y", "N"])
    )

    return suite
