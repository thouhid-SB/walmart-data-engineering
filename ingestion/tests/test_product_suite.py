
import pandas as pd

from src.validation import (
    get_gx_context,
    register_data_source,
    validate_dataframe
)

from gx.expectations.product_expectations import (
    create_product_suite
)


# Load product data
df = pd.read_csv("data/incoming/products.csv")

# Create GX context and data source
context = get_gx_context()
data_source = register_data_source(context)

# Create product expectation suite
product_suite = create_product_suite()

# Execute validation
validation_success = validate_dataframe(
    context=context,
    data_source=data_source,
    df=df,
    asset_name="products_asset",
    suite=product_suite
)

print("\nFinal Result:", validation_success)
