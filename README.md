Sales Analysis and Dashboard

----------

**Summary** 

This project supports marketing teams providing data driven insights from transactional data. We build models capturing customer behavior, sales trends and customer lifetime value. Key output is a Power BI dashboard (screenshots in dashboard folder) that consolidates model insights and tracks additional sales KPI. 


**Key Insights**
- Over half of the customer base (54%) made no more than two purchases, with 35% transacting only once.  Prioritise a post-purchase re-engagement programme targeted at first and second-time buyers.
- Revenue largely driven by wholesale buyers (mean order value of $430) making up 2.85% of the customer base. 
- 'Promising' group identified by high frequency and low recency RFM scores with low average order values.  Ideal for up sales through product recommendations (using co-purchases derived from analysis). 
- Identified customers with greater than 80% probability of purchase in the next 30 days ideal for advertising. 
- Projected compound monthly growth of 0.14% from start of 2011 year. 


**Main Objectives**

1. Generate categories of each product based on item description. 
2. Process raw data to be stored using the STAR schema in an SQLite database. 
3. Forecast Sales using a time series model.
4. Segment customers based on recency, frequency and monetary value scores to identify customer behavior types. 
5.  Predict future customer lifetime value for customers in the database. 
6. Create product recommendations based on order co-purchases. 
7. Create a PowerBI dashboard for intuitive reporting of 3-6 above with additional key sales metrics. 


**Usage** 

To rerun analysis on updated data:
1. Edit `config.yml` to reconfigure directories and table keys.
2. Run `create_database.py` to create sqlite database stored in path 'db' in configuration file. SQL query used to create tables saved in logs folder as `sql_query.txt`. 
3. Run notebook `1_create_categories.ipynb` block by block. This requires inspecting the output saved to logs and modifying inputs yaml files in inputs folder. 
4. Run notebooks 2a-2d in any order, modify hyperparameters in time series model and Kmeans if necessary.  
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


