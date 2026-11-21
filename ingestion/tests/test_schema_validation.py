import pandas as pd
from pathlib import Path

from src.dataset_validator import validate_schema


# Create a DataFrame with a missing customer_id column
df = pd.DataFrame({
    "first_name": ["Rahul"],
    "last_name": ["Sharma"],
    "email": ["rahul@example.com"],
    "city": ["Bangalore"]
})

file_path = Path("customers.csv")

result = validate_schema(file_path, df)

print("Schema validation result:", result)