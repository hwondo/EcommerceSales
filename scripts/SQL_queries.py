import pandas as pd
import sqlite3 as sql 
import yaml


# --- SQL Query --- #

T = "'2011-12-09'" # Set analysis date (format YYYY-MM-DD)

# Subqueries
Qsub_Order_Data = """
    SELECT 
        o.InvoiceNo,
        o.CustomerID,
        o.StockCode,
        date(t.InvoiceDate) AS order_date,
        p.CategoryLabel,
        p.Description,
        o.Revenue
    FROM Orders o
    LEFT JOIN Products p 
        ON o.StockCode = p.StockCode
    LEFT JOIN time t
        ON o.InvoiceNo = t.InvoiceNo
    WHERE o.Revenue > 0 
        AND o.InvoiceNo NOT LIKE 'C%'
        AND p.CategoryLabel IS NOT NULL
"""

Qsub_Customer_Agg = f"""
    SELECT 
        s.CustomerID,
        julianday({T}) - julianday(MAX(s.order_date)) AS recency_days,
        julianday({T}) - julianday(MIN(s.order_date)) AS observation_days,
        julianday(MAX(s.order_date)) - julianday(MIN(s.order_date)) AS active_days,
        COUNT(DISTINCT s.InvoiceNo) AS total_orders,
        SUM(s.Revenue) AS total_purchase      
    FROM ({Qsub_Order_Data}) s
    GROUP BY s.CustomerID
"""

# Queries
Q_Sales = f"""
    SELECT 
        s.InvoiceNo,
        s.order_date,
        s.CustomerID,
        s.StockCode,
        s.CategoryLabel AS category, 
        s.Description AS description,
        s.Revenue AS revenue
    FROM ({Qsub_Order_Data}) s
"""

Q_rfm = f"""
    SELECT 
        c.CustomerID,
        c.recency_days AS recency,
        c.total_orders AS frequency,
        CASE
            WHEN c.total_orders > 0
            THEN c.total_purchase / c.total_orders
            ELSE NULL
        END AS  monetary_value,
        c.observation_days AS tenure
    FROM ({Qsub_Customer_Agg}) c
    """
    
Q_clv = f"""
    SELECT
        c.CustomerID,
        c.active_days as recency,
        c.total_orders - 1 AS frequency,
        c.observation_days AS tenure,
        c.total_purchase / c.total_orders AS monetary_value
    FROM ({Qsub_Customer_Agg}) c
    """

Q_pr = f"""
    SELECT
        o.InvoiceNo,
        o.CustomerID,
        o.StockCode
    FROM ({Qsub_Order_Data}) o
"""

# --- Main Function --- #   

def main(sales = False, rfm = False, clv = False, pr = False):

    # Get directories from YAML file
    with open('../config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        DB_DIR = config['dir']['db']

    # Query from database
    conn = sql.connect("../"+DB_DIR)

    if (sales == True):
        output_df = pd.read_sql_query(Q_Sales, conn)
    if (rfm == True):
        output_df = pd.read_sql_query(Q_rfm, conn)
    if (clv == True):
        output_df = pd.read_sql_query(Q_clv, conn)
    if (pr == True):
        output_df = pd.read_sql_query(Q_pr,conn)
        
    # Debugging 
    #order_df = pd.read_sql_query(Q_Order_Data, conn)
    #customer_agg_df = pd.read_sql_query(Q_Customer_Agg, conn)

    conn.close()
    
    return output_df


if __name__ == "__main__":
    main()
    