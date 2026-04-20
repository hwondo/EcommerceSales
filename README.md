# Sales Analysis and Dashboard

---

## Summary

This project supports marketing teams by providing data-driven insights from 
transactional data. We build models capturing customer behaviour, sales trends, 
and customer lifetime value. The key output is a Power BI dashboard (screenshots 
in the dashboard folder) that consolidates model insights and tracks additional 
sales KPIs. We also apply a driver analysis to identify factors contributing to 
increases and anomalies in revenue.

---

## Key Insights

An upward trend in revenue is observed throughout the year. Wholesaler purchases 
are the primary driver, contributing approximately $1,052 per week (around 20% 
of the total weekly revenue increase). This poses a concentration risk to revenue, 
since wholesalers represent a small group (2.85% of the customer base, with a 
mean order value of $430 and average monetary value of approximately $16,000) 
that disproportionately affects total revenue.

Over half of the customer base (54%) made no more than two purchases, with 35% 
transacting only once. A high number of single-purchase customers transacted in 
the week ending 25 September 2011, contributing to a spike in revenue for that 
week, possibly due to a clearance sale attracting new customers. If a clearance 
sale is confirmed, a post-purchase re-engagement programme targeted at first- and 
second-time buyers should be prioritised for future promotional activity.

In relation to the two points above, marketing should utilise the customer 
analytics dashboard to target the following:

- **Promising** customers — identified by high frequency and low recency RFM 
  scores with low average order values. Ideal candidates for upselling through 
  product recommendations derived from co-purchase analysis.
- Customers with greater than 80% probability of purchase in the next 30 days 
  (from the CLV model) — ideal for advertising to increase conversion.
- Loyal customers — monitor health metrics in the customer profile dashboard, 
  identify shortfalls within groups, and target accordingly.

A forecasted compound monthly growth rate of 0.14% from the start of 2011 
should be used as a baseline against which to measure the future performance 
of marketing campaigns and targeting activity.

---

## Deliverables

1. Generate categories for each product based on item description.
2. Process raw data and store using the star schema in an SQLite database.
3. Forecast sales using a time series model.
4. Segment customers based on recency, frequency, and monetary value scores 
   to identify customer behaviour types.
5. Predict future customer lifetime value for customers in the database.
6. Generate product recommendations based on order co-purchases.
7. Build a Power BI dashboard for intuitive reporting of deliverables 3–6 
   above, with additional key sales metrics.

---

## Usage

To rerun the analysis on updated data:

1. Edit `config.yml` to reconfigure directories and table keys.
2. Run `create_database.py` to create the SQLite database stored in the path 
   specified by `db` in the configuration file. The SQL query used to create 
   tables is saved in the logs folder as `sql_query.txt`.
3. Run notebook `1_create_categories.ipynb` block by block. This requires 
   inspecting the output saved to logs and modifying the input YAML files in 
   the inputs folder.
4. Run notebooks `2a`–`2d` in any order. Modify hyperparameters in the time 
   series model and K-means clustering if necessary.
5. Refresh data in Power BI.

---

## Data Sources

The raw data was obtained from the UC Irvine Machine Learning Repository. It 
is a transactional dataset containing all transactions occurring between 
01/12/2010 and 09/12/2011 for a UK-based registered non-store online retailer.

For more information on the data, see `./data/raw/about.md`.

---

## Star Schema in SQLite Database

Data is stored in the following tables in the SQLite database. The SQL queries 
used to create the tables are recorded in the logs directory.

- **Orders** (fact table) — indexed by `InvoiceNo`. Contains time of order, 
  customer ID, and stock purchased.
- **Customers** (dimension table) — contains customer information.
- **Time** (dimension table) — contains data on the timing of orders.

---

## Notebook Data Input and Outputs


- Within each notebook, data is imported via queries specified in 
`./scripts/SQL_queries.py`.
- Analysis outputs from notebooks are stored as Parquet files in 
  `./data/analysis`.
- A table called `orders.parquet` (a joined fact and dimension table) is 
  created to circumvent known issues with connecting an SQLite database 
  directly to Power BI.
- Both `orders.parquet` and analysis outputs are imported into Power BI.