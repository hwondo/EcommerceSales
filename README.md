Sales Analysis and Dashboard

----------

**Overview** 

This project aims to analyse ecommerce sales data with insights delivered through a PowerBI dashboard.  

**Main Objectives**

1. Generate categories of each product based on item description. 
2. Process raw data to be stored using the STAR schema in an SQLite database. 
3. Forecast Sales using a time series model.
4. Segment customers based on recency, frequency and monetary value scores to identify customer behavior types. 
5.  Predict future customer lifetime value for customers in the database. 
6. Create product recommendations based on order copurchases. 
7. Create a PowerBI dashboard for intuitive reporting of 3-6 above with additional key sales metrics. 


**Usage** 

To rerun analysis on updated data:
1. Edit `config.yml` to reconfigure directories and table keys.
2. Run `create_database.py` to create sqlite database stored in path 'db' in configuration file. SQL query used to create tables saved in logs folder as `sql_query.txt`. 
3. Run notebook `1_create_categories.ipynb` block by block. This requires inspecting the output saved to logs and modifying inputs yaml files in inputs folder. 
4. Run notebooks 2a-2d in any order, modify hyperparameters in ARIMA and Kmeans if necessary.  
5. Refresh data in PowerBI. 

----------

**Data Sources**

The raw data was obtained from UC Irvine MAchine Learning Repository. 

This is a transactional data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.

The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers.

For more information on the data, see `./data/raw/about.md`. 


**Star schema in SQLite database**

Data is stored in the following tables in the sqlite database. The SQL queries used to create the tables are recorded in the logs directory. 
- Fact table called 'Orders' indexed by InvoiceNo. Contains time of order, customer id who purchased the order, stock that was bought. 
- Dimension table called 'Customers' containing customer information. 
- Dimension table called 'Time' containing data on time of orders. 

**SQLite Database to Analysis**

Within each notebook data is imported via queries specified in `./scripts/SQL_queries.py`. 

**Notebook Outputs**

- Analysis output from notebooks stored as parquet files in folder `.data/analysis`. 
- Data table called orders.parquet (joined fact table with dimension tables) is created to circumvent issues with connecting sqlite database to PowerBI. 
- Both Orders.parquet 'raw data' and analysis output are imported into PowerBI. 


