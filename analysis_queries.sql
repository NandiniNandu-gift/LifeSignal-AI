-- ==========================================
-- LIFESIGNAL AI - DATABASE SETUP & ANALYSIS
-- ==========================================

-- STEP 1: Create Database
CREATE DATABASE IF NOT EXISTS lifesignal_ai;

-- STEP 2: Select Database
USE lifesignal_ai;

-- STEP 3: Create Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    description VARCHAR(255),
    category VARCHAR(100),
    transaction_type VARCHAR(30),
    amount_inr DECIMAL(12,2) NOT NULL,
    payment_method VARCHAR(100),
    account_name VARCHAR(100)
);

-- STEP 4: Check Tables
SHOW TABLES;

DESCRIBE transactions;

-- STEP 5: Verify Uploaded Data
SELECT COUNT(*) AS total_transactions
FROM transactions;

SELECT *
FROM transactions
LIMIT 10;

-- STEP 6: Overall Financial Summary
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_amount,
    ROUND(AVG(amount_inr), 2) AS average_amount,
    MIN(amount_inr) AS minimum_amount,
    MAX(amount_inr) AS maximum_amount
FROM transactions;

-- STEP 7: Income vs Expenses
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount
FROM transactions
GROUP BY transaction_type;

-- STEP 8: Category-wise Expenses
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_expenses
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY category
ORDER BY total_expenses DESC;

-- STEP 9: Monthly Expenses
SELECT
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    SUM(amount_inr) AS monthly_expenses
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY month
ORDER BY month;

-- STEP 10: Monthly Income, Expenses and Savings
SELECT
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    SUM(CASE
        WHEN LOWER(transaction_type) = 'income'
        THEN amount_inr ELSE 0
    END) AS income,
    SUM(CASE
        WHEN LOWER(transaction_type) = 'expense'
        THEN amount_inr ELSE 0
    END) AS expenses,
    SUM(CASE
        WHEN LOWER(transaction_type) = 'income'
        THEN amount_inr
        WHEN LOWER(transaction_type) = 'expense'
        THEN -amount_inr
        ELSE 0
    END) AS net_savings
FROM transactions
GROUP BY month
ORDER BY month;

-- STEP 11: Payment Method Analysis
SELECT
    payment_method,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount
FROM transactions
GROUP BY payment_method
ORDER BY total_amount DESC;

-- STEP 12: Account-wise Analysis
SELECT
    account_name,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount
FROM transactions
GROUP BY account_name
ORDER BY total_amount DESC;

-- STEP 13: Top 10 Highest Expenses
SELECT
    transaction_date,
    description,
    category,
    amount_inr,
    payment_method
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
ORDER BY amount_inr DESC
LIMIT 10;

-- STEP 14: Data Quality Check
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT transaction_id) AS unique_ids,
    SUM(amount_inr IS NULL) AS missing_amounts,
    SUM(transaction_date IS NULL) AS missing_dates
FROM transactions;

-- STEP 15: High-value Transactions
SELECT *
FROM transactions
WHERE amount_inr >= (
    SELECT AVG(amount_inr) * 2
    FROM transactions
)
ORDER BY amount_inr DESC;

SELECT COUNT(*) AS total_transactions
FROM transactions;
-- STEP 16: Category-wise Monthly Expenses

SELECT
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    category,
    SUM(amount_inr) AS total_expenses
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY month, category
ORDER BY month, total_expenses DESC;

-- STEP 17: HIGHEST EXPENSE CATEGORY
-- PURPOSE: Identify the category with highest spending

SELECT
    category,
    SUM(amount_inr) AS total_expenses
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY category
ORDER BY total_expenses DESC
LIMIT 1

-- STEP 18: AVERAGE EXPENSE BY CATEGORY

SELECT
    category,
    ROUND(AVG(amount_inr), 2) AS average_expense,
    COUNT(*) AS transaction_count
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY category
ORDER BY average_expense DESC;
 
-- STEP 19: DAILY EXPENSE ANALYSIS
-- PURPOSE: Calculate daily total expenses

SELECT
    transaction_date,
    SUM(amount_inr) AS daily_expenses
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY transaction_date
ORDER BY transaction_date;

-- STEP 20: WEEKDAY-WISE EXPENSE ANALYSIS
-- PURPOSE: Identify spending patterns by weekday

SELECT
    DAYNAME(transaction_date) AS weekday,
    ROUND(AVG(amount_inr), 2) AS average_expense,
    SUM(amount_inr) AS total_expenses
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY DAYOFWEEK(transaction_date), DAYNAME(transaction_date)
ORDER BY DAYOFWEEK(transaction_date);

-- STEP 20: WEEKDAY-WISE EXPENSE ANALYSIS
-- PURPOSE: Identify spending patterns by weekday

SELECT
    DAYNAME(transaction_date) AS weekday,
    ROUND(AVG(amount_inr), 2) AS average_expense,
    SUM(amount_inr) AS total_expenses
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY DAYOFWEEK(transaction_date), DAYNAME(transaction_date)
ORDER BY DAYOFWEEK(transaction_date);

-- STEP 21: TOP 20 TRANSACTIONS
-- PURPOSE: Find the 20 highest transaction amounts
SELECT
    transaction_id,
    transaction_date,
    description,
    category,
    transaction_type,
    amount_inr
FROM transactions
ORDER BY amount_inr DESC
LIMIT 20;

-- STEP 22: MONTHLY TRANSACTION COUNT
-- PURPOSE: Count transactions for each month

SELECT
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY month
ORDER BY month;

-- STEP 23: INCOME BY CATEGORY
-- PURPOSE: Calculate income generated by each category

SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_income
FROM transactions
WHERE LOWER(transaction_type) = 'income'
GROUP BY category
ORDER BY total_income DESC;

-- STEP 24: EXPENSE PERCENTAGE BY CATEGORY
-- PURPOSE: Calculate each category's share of total expenses

SELECT
    category,
    SUM(amount_inr) AS category_expense,
    ROUND(
        SUM(amount_inr) * 100 /
        NULLIF(
            (SELECT SUM(amount_inr)
             FROM transactions
             WHERE LOWER(transaction_type) = 'expense'),
            0
        ),
        2
    ) AS expense_percentage
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY category
ORDER BY expense_percentage DESC;

-- STEP 25: HIGH-VALUE EXPENSE DETECTION
-- PURPOSE: Identify expenses greater than twice the average expense

SELECT
    transaction_id,
    transaction_date,
    description,
    category,
    amount_inr
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
AND amount_inr > (
    SELECT AVG(amount_inr) * 2
    FROM transactions
    WHERE LOWER(transaction_type) = 'expense'
)
ORDER BY amount_inr DESC;

-- STEP 26: RUNNING TOTAL OF EXPENSES
-- PURPOSE: Calculate cumulative expenses over time

SELECT
    transaction_date,
    transaction_id,
    amount_inr,
    SUM(amount_inr) OVER (
        ORDER BY transaction_date, transaction_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_expenses
FROM transactions
WHERE LOWER(transaction_type) = 'expense';
-- ==========================================
-- STEP 27: RANK EXPENSE CATEGORIES
-- PURPOSE: Rank categories based on total expenses

SELECT
    category,
    SUM(amount_inr) AS total_expenses,
    DENSE_RANK() OVER (
        ORDER BY SUM(amount_inr) DESC
    ) AS expense_rank
FROM transactions
WHERE LOWER(transaction_type) = 'expense'
GROUP BY category
ORDER BY expense_rank;
-- ==========================================
-- STEP 28: PREVIOUS MONTH EXPENSE COMPARISON
-- PURPOSE: Compare current month expenses with previous month

WITH monthly_data AS (
    SELECT
        DATE_FORMAT(transaction_date, '%Y-%m') AS month,
        SUM(amount_inr) AS monthly_expenses
    FROM transactions
    WHERE LOWER(transaction_type) = 'expense'
    GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
)
SELECT
    month,
    monthly_expenses,
    LAG(monthly_expenses) OVER (
        ORDER BY month
    ) AS previous_month_expenses
FROM monthly_data
ORDER BY month;
-- ==========================================
-- STEP 29: MONTHLY EXPENSE CHANGE PERCENTAGE
-- PURPOSE: Calculate month-to-month expense growth or reduction

WITH monthly_data AS (
    SELECT
        DATE_FORMAT(transaction_date, '%Y-%m') AS month,
        SUM(amount_inr) AS monthly_expenses
    FROM transactions
    WHERE LOWER(transaction_type) = 'expense'
    GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
),
comparison AS (
    SELECT
        month,
        monthly_expenses,
        LAG(monthly_expenses) OVER (
            ORDER BY month
        ) AS previous_month_expenses
    FROM monthly_data
)
SELECT
    month,
    monthly_expenses,
    previous_month_expenses,
    ROUND(
        (monthly_expenses - previous_month_expenses) * 100 /
        NULLIF(previous_month_expenses, 0),
        2
    ) AS expense_change_percentage
FROM comparison
ORDER BY month;
-- ==========================================
-- STEP 30: FINAL FINANCIAL SUMMARY
-- PURPOSE: Calculate overall income, expenses and net savings

SELECT
    SUM(CASE
        WHEN LOWER(transaction_type) = 'income'
        THEN amount_inr ELSE 0
    END) AS total_income,

    SUM(CASE
        WHEN LOWER(transaction_type) = 'expense'
        THEN amount_inr ELSE 0
    END) AS total_expenses,

    SUM(CASE
        WHEN LOWER(transaction_type) = 'income'
        THEN amount_inr
        WHEN LOWER(transaction_type) = 'expense'
        THEN -amount_inr
        ELSE 0
    END) AS net_savings,

    COUNT(*) AS total_transactions

FROM transactions
-- ==========================================
-- STEP 31: FINAL DATABASE VALIDATION
-- PURPOSE: Verify transaction count and data quality

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT transaction_id) AS unique_transactions,
    SUM(transaction_id IS NULL) AS missing_ids,
    SUM(transaction_date IS NULL) AS missing_dates,
    SUM(amount_inr IS NULL) AS missing_amounts
FROM transactions;