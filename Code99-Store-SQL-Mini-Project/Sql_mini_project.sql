/* ============================================================
   DAY 45 : MINI PROJECT ASSIGNMENT
   ============================================================
   Do this AFTER going through Day45_SQL_Mini_Project_Notes.sql

   You are the data analyst for Code99 Store. Complete the
   business questions below, organized into the same three
   sections as today's notes. As in real work, there is no hint
   about which SQL tool to use for each question -- work out your
   own thought process first (what tables? joins? grouping?
   filtering? sorting?), then write the query. Use the
   code99_store database throughout.

   A final written task is included at the end -- this is the
   most important part of a real project, so don't skip it.
   ============================================================ */


/* ------------------------------------------------------------
   SECTION A: SALES & REVENUE OVERVIEW
   ------------------------------------------------------------ */

-- TASK 1:
-- How many orders currently have each order status (Delivered,
-- Pending, etc.)?
-- Your query:

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status;


-- TASK 2:
-- How much actual revenue is tied up in each order status? (For
-- example, this tells us how much money is still "Pending" and
-- not yet confirmed as delivered.)
-- Your query

SELECT
    o.order_status,
    SUM(oi.quantity * oi.price_each) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.order_status;


/* ------------------------------------------------------------
   SECTION B: PRODUCT PERFORMANCE
   ------------------------------------------------------------ */

-- TASK 3:
-- Which category currently holds the most total stock units
-- overall (not the most revenue -- just the raw unit count sitting
-- in our warehouse)?
-- Your query:
SHOW TABLES

 DESC products;
 
SELECT
    category,
    SUM(stock_quantity) AS total_stock
FROM products
GROUP BY category
ORDER BY total_stock DESC
LIMIT 1;


-- TASK 4:
-- Find every product that is BOTH priced above its own category's
-- average price AND still currently has stock available.
-- Your query:
SELECT
    p.product_name,
    p.price,
    p.category
FROM products p
WHERE p.price >
(
    SELECT AVG(p2.price)
    FROM products p2
    WHERE p2.category = p.category
)
AND p.stock_quantity > 0;


/* ------------------------------------------------------------
   SECTION C: CUSTOMER INSIGHTS
   ------------------------------------------------------------ */

-- TASK 5:
-- Which customer(s) have purchased from the widest variety of
-- different product categories? Make sure your answer wouldn't
-- accidentally hide a tie.
-- Your query:

WITH customer_categories AS
(
    SELECT
        c.customer_id,
        c.customer_name,
        COUNT(DISTINCT p.category) AS category_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT *
FROM customer_categories
WHERE category_count =
(
    SELECT MAX(category_count)
    FROM customer_categories
);
-- TASK 6:
-- Among customers who have actually placed at least one order,
-- rank them by their AVERAGE order value (not their total spend)
-- -- highest average first.
-- Your query:

WITH order_totals AS
(
    SELECT
        o.order_id,
        o.customer_id,
        SUM(oi.quantity * oi.price_each) AS order_value
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.customer_id
)
SELECT
    c.customer_name,
    ROUND(AVG(ot.order_value),2) AS avg_order_value
FROM customers c
JOIN order_totals ot
    ON c.customer_id = ot.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY avg_order_value DESC;


/* ------------------------------------------------------------
   FINAL TASK: EXECUTIVE SUMMARY
   ------------------------------------------------------------ */

-- TASK 7:
-- Using your results from Tasks 1-6 (and anything from today's
-- notes you'd like to reference), write a short executive summary
-- -- 4 to 6 sentences, in plain business language, no SQL -- as
-- if you were handing this directly to the founder of Code99
-- Store. Cover at least one finding from each section (Sales,
-- Products, Customers), and end with one clear recommendation.
-- Your query:

-- Sales analysis shows the current order status distribution and the revenue associated with each status.
-- Product analysis identifies the category with the highest total
-- stock and products priced above their category average while still having stock available.
-- Customer analysis identifies the customers who purchased from the
-- widest variety of product categories and ranks customers by their average order value.
-- Based on these findings, Code99 Store should focus on improving
-- sales performance, managing inventory efficiently, and targeting high-value customers with suitable offers.


/* ============================================================
   End of the Day 45 mini project.
   This is the final SQL day of the course -- congratulations on
   completing the full SQL portion of the syllabus (Days 34-45)!
   ============================================================ */
