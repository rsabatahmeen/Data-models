-- Create the olist_ecommerce database
CREATE DATABASE IF NOT EXISTS olist_ecommerce;
USE olist_ecommerce;

-- ===========================
--  INSERT Statements
-- ===========================

-- Insert a new customer into the customers table
INSERT INTO customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
VALUES ('c3', 'unique_003', 13579, 'Brasília', 'DF');

-- Insert a new order into the orders table
INSERT INTO orders (order_id, customer_id, order_status, order_purchase_timestamp)
VALUES ('o3', 'c3', 'processing', '2024-06-10 09:15:00');

-- ===========================
--  UPDATE Statements
-- ===========================

-- Update a customer's city in the customers table
UPDATE customers 
SET customer_city = 'Salvador' 
WHERE customer_id = 'c3';

-- Update an order status in the orders table
UPDATE orders 
SET order_status = 'shipped' 
WHERE order_id = 'o3';

-- ===========================
--  DELETE Statement
-- ===========================

-- Delete an order from the orders table
DELETE FROM orders 
WHERE order_id = 'o3';

-- ===========================
--  Simple SELECT Query
-- ===========================

-- Retrieve customer_id, customer_city, and customer_state for customers in São Paulo (SP)
SELECT customer_id, customer_city, customer_state 
FROM customers 
WHERE customer_state = 'SP';

-- ===========================
--  JOIN Queries
-- ===========================

-- Retrieve orders with customer details by joining orders and customers tables
SELECT orders.order_id, customers.customer_id, customers.customer_city, orders.order_status 
FROM orders 
JOIN customers ON orders.customer_id = customers.customer_id;

-- Retrieve products with seller information by joining products, order_items, and sellers tables
SELECT products.product_id, products.product_category_name, sellers.seller_id, sellers.seller_city 
FROM products 
JOIN order_items ON products.product_id = order_items.product_id 
JOIN sellers ON order_items.seller_id = sellers.seller_id;

-- ===========================
--  Summary Function Queries
-- ===========================

-- Count the total number of orders in the orders table
SELECT COUNT(order_id) AS total_orders FROM orders;

-- Calculate the average order price from the order_items table
SELECT AVG(price) AS average_order_price FROM order_items;

-- ===========================
--  Multi-Table Query
-- ===========================

-- Retrieve order details with customer and payment information
SELECT orders.order_id, customers.customer_city, orders.order_status, order_payments.payment_type, order_payments.payment_value
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
JOIN order_payments ON orders.order_id = order_payments.order_id;

-- ===========================
-- Custom Query
-- ===========================

-- Find the most frequently purchased products
SELECT products.product_id, products.product_category_name, COUNT(order_items.product_id) AS total_purchases
FROM products
JOIN order_items ON products.product_id = order_items.product_id
GROUP BY products.product_id, products.product_category_name
ORDER BY total_purchases DESC;
