import pandas as pd

from src.validation import (
    get_gx_context,
    register_data_source,
    register_dataframe_asset
)

df = pd.read_csv("data/incoming/customers.csv")

context = get_gx_context()

data_source = register_data_source(context)

batch_definition = register_dataframe_asset(
    data_source,
    "customers_asset"
)

batch = batch_definition.get_batch(
    batch_parameters={"dataframe": df}
)

print("Data Source:", data_source.name)
print("Batch Definition:", batch_definition.name)
print("Batch created successfully:", batch is not None)