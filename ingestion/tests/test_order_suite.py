
import pandas as pd

from src.validation import (
    get_gx_context,
    register_data_source,
    validate_dataframe
)

from gx.expectations.order_expectations import create_order_suite


# Load order data
df = pd.read_csv("data/incoming/orders.csv")

# Create GX context and data source
context = get_gx_context()
data_source = register_data_source(context)

# Create order expectation suite
order_suite = create_order_suite()

# Execute validation
validation_success = validate_dataframe(
    context=context,
    data_source=data_source,
    df=df,
    asset_name="orders_asset",
    suite=order_suite
)

print("\nFinal Result:", validation_success)
