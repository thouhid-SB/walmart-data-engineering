
import pandas as pd

from src.validation import (
    get_gx_context,
    register_data_source,
    validate_dataframe
)

from gx.expectations.customer_expectations import create_customer_suite


# Load customer data
df = pd.read_csv("data/incoming/customers.csv")

# Create GX context and data source
context = get_gx_context()
data_source = register_data_source(context)

# Create customer expectation suite
customer_suite = create_customer_suite()

# Execute validation
validation_success = validate_dataframe(
    context=context,
    data_source=data_source,
    df=df,
    asset_name="customers_asset",
    suite=customer_suite
)

print("\nFinal Result:", validation_success)
