-- =========================================================
-- WALMART DATA ENGINEERING PROJECT
-- BRONZE: S3 -> Auto Loader
-- SILVER: Bronze -> AUTO CDC (SCD TYPE 1)
-- =========================================================
-- =========================================================
-- PART 1: BRONZE STREAMING TABLES
-- =========================================================
-- CUSTOMERS
CREATE OR REFRESH STREAMING TABLE walmart.bronze.customers
AS SELECT *
FROM STREAM read_files(
    's3://ecom-data-lake-thouhid/raw/customers/',
    format => 'csv'
);


-- EMPLOYEES
CREATE OR REFRESH STREAMING TABLE walmart.bronze.employees
AS SELECT *
FROM STREAM read_files(
    's3://ecom-data-lake-thouhid/raw/employees/',
    format => 'csv'
);


-- ORDERS
CREATE OR REFRESH STREAMING TABLE walmart.bronze.orders
AS SELECT *
FROM STREAM read_files(
    's3://ecom-data-lake-thouhid/raw/orders/',
    format => 'csv'
);


-- ORDER ITEMS
CREATE OR REFRESH STREAMING TABLE walmart.bronze.order_items
AS SELECT *
FROM STREAM read_files(
    's3://ecom-data-lake-thouhid/raw/order_items/',
    format => 'csv'
);


-- PRODUCTS
CREATE OR REFRESH STREAMING TABLE walmart.bronze.products
AS SELECT *
FROM STREAM read_files(
    's3://ecom-data-lake-thouhid/raw/products/',
    format => 'csv'
);


-- STORES
CREATE OR REFRESH STREAMING TABLE walmart.bronze.stores
AS SELECT *
FROM STREAM read_files(
    's3://ecom-data-lake-thouhid/raw/stores/',
    format => 'csv'
);


-- =========================================================
-- PART 2: SILVER STREAMING TABLES
-- =========================================================
CREATE OR REFRESH STREAMING TABLE walmart.silver.customers;

CREATE OR REFRESH STREAMING TABLE walmart.silver.employees;

CREATE OR REFRESH STREAMING TABLE walmart.silver.orders;

CREATE OR REFRESH STREAMING TABLE walmart.silver.order_items;

CREATE OR REFRESH STREAMING TABLE walmart.silver.products;

CREATE OR REFRESH STREAMING TABLE walmart.silver.stores;


-- =========================================================
-- PART 3: AUTO CDC FLOWS (SCD TYPE 1)
-- =========================================================
-- CUSTOMERS CDC
CREATE FLOW customers_cdc
AS AUTO CDC INTO walmart.silver.customers
FROM STREAM(walmart.bronze.customers)
KEYS (customer_id)
SEQUENCE BY updated_timestamp
STORED AS SCD TYPE 1;


-- EMPLOYEES CDC
CREATE FLOW employees_cdc
AS AUTO CDC INTO walmart.silver.employees
FROM STREAM(walmart.bronze.employees)
KEYS (employee_id)
SEQUENCE BY updated_timestamp
STORED AS SCD TYPE 1;


-- ORDERS CDC
CREATE FLOW orders_cdc
AS AUTO CDC INTO walmart.silver.orders
FROM STREAM(walmart.bronze.orders)
KEYS (order_id)
SEQUENCE BY updated_timestamp
STORED AS SCD TYPE 1;


-- ORDER ITEMS CDC
CREATE FLOW order_items_cdc
AS AUTO CDC INTO walmart.silver.order_items
FROM STREAM(walmart.bronze.order_items)
KEYS (order_item_id)
SEQUENCE BY updated_timestamp
STORED AS SCD TYPE 1;


-- PRODUCTS CDC
CREATE FLOW products_cdc
AS AUTO CDC INTO walmart.silver.products
FROM STREAM(walmart.bronze.products)
KEYS (product_id)
SEQUENCE BY updated_timestamp
STORED AS SCD TYPE 1;


-- STORES CDC
CREATE FLOW stores_cdc
AS AUTO CDC INTO walmart.silver.stores
FROM STREAM(walmart.bronze.stores)
KEYS (store_id)
SEQUENCE BY updated_timestamp
STORED AS SCD TYPE 1;
