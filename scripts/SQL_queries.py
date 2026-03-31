import pandas as pd
import sqlite3 as sql 
import yaml


# --- SQL Query --- #

T = "'2011-12-09'" # Set analysis date (format YYYY-MM-DD)

# Subqueries
Qsub_JoinOrderData = """
    SELECT 
        o.InvoiceNo,
        o.CustomerID,
        o.StockCode,
        date(t.InvoiceDate) AS order_date,
        p.CategoryLabel,
        p.Description,
        o.Quantity,
        o.UnitPrice,
        (o.Quantity * o.UnitPrice) AS Revenue,
        CASE WHEN o.InvoiceNo LIKE 'C%' THEN 1 ELSE 0 END AS is_cancellation
    FROM Orders o
    LEFT JOIN Products p 
        ON o.StockCode = p.StockCode
    LEFT JOIN time t
        ON o.InvoiceNo = t.InvoiceNo
    WHERE p.CategoryLabel IS NOT NULL
        AND o.CustomerID IS NOT NULL
"""

Qsub_CustomerAgg = f"""
    SELECT
        CustomerID,
        SUM(Revenue)  AS Revenue,
        COUNT(DISTINCT CASE WHEN is_cancellation = 0 THEN InvoiceNo END) AS Orders,
        MIN(CASE WHEN is_cancellation = 0 THEN order_date END) AS FirstOrderDate,
        MAX(CASE WHEN is_cancellation = 0 THEN order_date END) AS LastOrderDate
    FROM ({Qsub_JoinOrderData})
    GROUP BY CustomerID
    HAVING SUM(Revenue) > 0
    """

# Queries
Q_Sales = f"""
    SELECT 
        s.InvoiceNo,
        s.is_cancellation,
        s.order_date,
        s.CustomerID,
        s.StockCode,
        s.CategoryLabel AS category,
        s.Description AS description,
        s.Revenue AS revenue
    FROM ({Qsub_JoinOrderData}) s
"""

Q_rfm = f"""
    SELECT 
        a.CustomerID,
        julianday({T}) - julianday(a.LastOrderDate) AS recency,
        a.Orders AS frequency,
        a.Revenue AS monetary_value,
        julianday({T}) - julianday(a.FirstOrderDate) AS tenure
    FROM ({Qsub_CustomerAgg}) a
    GROUP BY a.CustomerID
    """
    
Q_clv = f"""
    SELECT
        a.CustomerID,
        (julianday(a.LastOrderDate) - julianday(a.FirstOrderDate)) AS recency,
        a.Orders - 1 AS frequency,
        julianday({T}) - julianday(a.FirstOrderDate) AS tenure,
        CASE
            WHEN a.Orders > 0
            THEN a.Revenue / a.Orders 
            ELSE NULL
        END AS monetary_value       
    FROM ({Qsub_CustomerAgg}) a
    GROUP BY a.CustomerID
"""


Q_pr = f"""
    SELECT
        o.InvoiceNo,
        o.CustomerID,
        o.StockCode
    FROM ({Qsub_JoinOrderData}) o
    WHERE o.is_cancellation = 0
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
    