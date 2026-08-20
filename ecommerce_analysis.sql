CREATE TABLE ecommerce_sales (
    order_id INT,
    order_date DATE,
    customer_id INT,
    product_category VARCHAR(100),
    region VARCHAR(100),
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(10,4),
    payment_method VARCHAR(50),
    delivery_days INT,
    customer_rating DECIMAL(3,2),
    revenue DECIMAL(12,2),
    gross_sales DECIMAL(12,2),
    discount_amount DECIMAL(12,2),
    calculated_revenue DECIMAL(12,2),
    year INT,
    month VARCHAR(20),
    month_number INT,
    quarter VARCHAR(10),
    day_of_week VARCHAR(20),
    revenue_difference DECIMAL(12,2)
);

desc ecommerce_sales

#Total Revenue

SELECT SUM(revenue) AS total_revenue
FROM ecommerce_sales;

#Total Orders

SELECT COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_sales;

#Total Customers

SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM ecommerce_sales;

#Total Quantity

SELECT SUM(quantity) AS total_quantity
FROM ecommerce_sales;

#Average Order values

SELECT SUM(revenue) / COUNT(DISTINCT order_id) AS average_order_value
FROM ecommerce_sales;

#Revenue by Category

SELECT product_category, SUM(revenue) AS total_revenue
FROM ecommerce_sales
GROUP BY product_category
ORDER BY total_revenue DESC;

# Monthly Revenue

SELECT year, month_number, month,SUM(revenue) AS total_revenue
FROM ecommerce_sales
GROUP BY year, month_number, month
ORDER BY year, month_number;

# Quarterly Revenue

SELECT year, quarter, SUM(revenue) AS total_revenue
FROM ecommerce_sales
GROUP BY year, quarter
ORDER BY year, quarter;

#Top 10 Cuctomers

SELECT customer_id, SUM(revenue) AS total_revenue
FROM ecommerce_sales
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;

#Revenue by Payment Method

SELECT payment_method, SUM(revenue) AS total_revenue
FROM ecommerce_sales
GROUP BY payment_method
ORDER BY total_revenue DESC;

#Orders by Payment Method

SELECT payment_method, COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_sales
GROUP BY payment_method
ORDER BY total_orders DESC;

# Highest Discount Categories

SELECT product_category, AVG(discount) * 100 AS average_discount_percentage
FROM ecommerce_sales
GROUP BY product_category
ORDER BY average_discount_percentage DESC;

# Discount Impact

SELECT product_category, SUM(gross_sales) AS gross_sales, SUM(discount_amount) AS total_discount, SUM(revenue) AS net_revenue
FROM ecommerce_sales
GROUP BY product_category
ORDER BY net_revenue DESC;

# Delivery Performance

SELECT region, ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM ecommerce_sales
GROUP BY region
ORDER BY average_delivery_days;

# Customer Rating by Delivery Time

SELECT delivery_days, ROUND(AVG(customer_rating), 2) AS average_rating
FROM ecommerce_sales
GROUP BY delivery_days
ORDER BY delivery_days;

# High-Rating Categories

SELECT product_category, ROUND(AVG(customer_rating), 2) AS average_rating
FROM ecommerce_sales
GROUP BY product_category
HAVING AVG(customer_rating) >= 3
ORDER BY average_rating DESC;

# Revenue Contribution by Category

SELECT product_category,
    SUM(revenue) AS total_revenue,
    ROUND( SUM(revenue) * 100 / (SELECT SUM(revenue) FROM ecommerce_sales), 2 ) AS revenue_percentage
FROM ecommerce_sales
GROUP BY product_category
ORDER BY total_revenue DESC;

# Repeat Customers

SELECT customer_id, COUNT(DISTINCT order_id) AS total_orders
FROM ecommerce_sales
GROUP BY customer_id
HAVING COUNT(DISTINCT order_id) > 1
ORDER BY total_orders DESC;
