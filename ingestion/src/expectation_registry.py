from gx.expectations.customer_expectations import create_customer_suite
from gx.expectations.employee_expectations import create_employee_suite
from gx.expectations.order_expectations import create_order_suite
from gx.expectations.order_item_expectations import create_order_item_suite
from gx.expectations.product_expectations import create_product_suite
from gx.expectations.store_expectations import create_store_suite


EXPECTED_COLUMNS = {
    "customers.csv": [
        "customer_id", "first_name", "last_name", "email", "phone",
        "city", "province", "country", "created_timestamp",
        "updated_timestamp", "is_active"
    ],
    "employees.csv": [
        "employee_id", "store_id", "first_name", "last_name", "email",
        "job_title", "salary", "created_timestamp", "updated_timestamp",
        "is_active"
    ],
    "orders.csv": [
        "order_id", "customer_id", "store_id", "order_timestamp",
        "payment_method", "order_status", "total_amount",
        "created_timestamp", "updated_timestamp", "is_active"
    ],
    "order_items.csv": [
        "order_item_id", "order_id", "product_id", "quantity",
        "unit_price", "line_amount", "created_timestamp",
        "updated_timestamp", "is_active"
    ],
    "products.csv": [
        "product_id", "product_name", "category", "brand", "price",
        "created_timestamp", "updated_timestamp", "is_active"
    ],
    "stores.csv": [
        "store_id", "store_name", "city", "province", "country",
        "created_timestamp", "updated_timestamp", "is_active"
    ],
}


EXPECTATION_REGISTRY = {
    "customers.csv": create_customer_suite,
    "employees.csv": create_employee_suite,
    "orders.csv": create_order_suite,
    "order_items.csv": create_order_item_suite,
    "products.csv": create_product_suite,
    "stores.csv": create_store_suite,
}
