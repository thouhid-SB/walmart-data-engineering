
import pandas as pd

from src.validation import (
    get_gx_context,
    register_data_source,
    validate_dataframe
)

from gx.expectations.order_item_expectations import (
    create_order_item_suite
)


# Load order items data
df = pd.read_csv("data/incoming/order_items.csv")

# Create GX context and data source
context = get_gx_context()
data_source = register_data_source(context)

# Create order items expectation suite
order_item_suite = create_order_item_suite()

# Execute validation
validation_success = validate_dataframe(
    context=context,
    data_source=data_source,
    df=df,
    asset_name="order_items_asset",
    suite=order_item_suite
)

print("\nFinal Result:", validation_success)
