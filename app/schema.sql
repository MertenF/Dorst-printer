DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS items;

CREATE TABLE IF NOT EXISTS orders
(
    table_name         TEXT,
    payment_status     TEXT,
    order_num          INT,
    payment_method     TEXT,
    customer           TEXT,
    prepare_location   TEXT,
    total_price_cents  INT,
    total_items_amount INT,
    order_datetime     TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items
(
    amount       INT,
    product_name TEXT,
    price_cents  INT,
    subitem      TEXT
);