import yaml

import pandas as pd
import sqlite3 as sql

def load_excel(raw_data_dir: str):
    # Read Excel files
    return  pd.read_excel(raw_data_dir)

def create_df(raw_data:pd.DataFrame, cols:list = None):
    # Create dataframe consisting of subsets cols with unique rows
    if cols == None:
        cols = raw_data.columns
        
    return (
        raw_data[cols]
        .drop_duplicates()
        .reset_index(drop=True)
        )

def create_time_df(raw_df:pd.DataFrame, time_cols:list):
    # Separate time column into Year, Month and Day columns
    time = raw_df[time_cols].copy()
    
    time['Year'] = pd.to_datetime(time['InvoiceDate']).dt.year
    time['Month'] = pd.to_datetime(time['InvoiceDate']).dt.month
    time['Day'] = pd.to_datetime(time['InvoiceDate']).dt.day
    
    return create_df(time)

def calc_revenue(raw_df:pd.DataFrame, order_cols:list):
    # Calculate revenue from orders dataframe
    orders = raw_df[order_cols].copy()
    orders['Revenue'] = orders['Quantity'] * orders['UnitPrice']

    return (
        orders[['InvoiceNo', 'CustomerID', 'StockCode', 'Quantity', 'Revenue']]
        .reset_index(drop=True)
    )
   

def create_table_sql(table_name:str, df: pd.DataFrame, pk_columns=[], fk_dict={}):
    """Generate SQL script for creating a table from dataframe with primary and foreign keys"""
    
    col_defs = []
    
    for col, dtype in zip(df.columns, df.dtypes):
        if 'int' in str(dtype):
            sql_type = 'INTEGER'
        elif 'float' in str(dtype):
            sql_type = 'REAL'
        else:
            sql_type = 'TEXT'
        col_defs.append(f"{col} {sql_type}")
    
    # Add primary key
    if pk_columns:
        col_defs.append(f"PRIMARY KEY ({', '.join(pk_columns)})")
    
    # Add foreign keys
    for child_col, parent_ref in fk_dict.items():
        parent_table, parent_col = parent_ref.split('.')
        col_defs.append(f"FOREIGN KEY ({child_col}) REFERENCES {parent_table}({parent_col})")
    
    sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    " + ",\n    ".join(col_defs) + "\n);"
    
    return sql_query


def insert_data(db_dir:str, dfs: dict[str, pd.DataFrame],
                primary_keys: dict[str, list[str]], foreign_keys: dict[str, dict[str, str]]):
    # --- Insert Data Into Database --- #

    # Load dataframes into SQL database
    conn = sql.connect(db_dir)
    conn.execute("PRAGMA foreign_keys = ON;")

    # Create tables dynamically
    for table, df in dfs.items():
        pk = primary_keys.get(table, [])
        fk = foreign_keys.get(table, {})
        sql_query = create_table_sql(table, df, pk_columns=pk, fk_dict=fk)
        print(sql_query)  # print generated SQL query
        conn.execute(sql_query)

    # Insert data
    for table, df in dfs.items():
        df.to_sql(table, conn, if_exists='replace', index=False)
    
    conn.close()

def main():
    # Get configurations from YAML file
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        
        # Obtain keys from config
        primary_keys = config['primary_keys']
        foreign_keys = config['foreign_keys']
        
        # Obtain directories from YAML file 
        RAW_DATA_DIR = config['dir']['raw_data'] # folder containing Olist CSV files
        DB_DIR = config['dir']['db'] # folder containing database
    
    # Load CSV files
    raw_df = load_excel(RAW_DATA_DIR)
    
    # Define column names for each table
    customer_cols = ['CustomerID', 'Country']
    product_cols = ['StockCode', 'Description']
    time_cols = ['InvoiceNo', 'InvoiceDate']
    order_cols = ['InvoiceNo', 'CustomerID', 'StockCode', 'Quantity', 'UnitPrice']
    
    # Create Customers, Product, Time and Order DataFrames
    dfs = {}
    
    dfs['Customers'] = create_df(raw_df,customer_cols)
    dfs['Raw_Products'] = create_df(raw_df,product_cols)
    dfs['Time'] = create_time_df(raw_df,time_cols)
    dfs['Orders'] = calc_revenue(raw_df,order_cols)
    
    # Create SQLite DB and fill tables with data
    insert_data(
        db_dir=DB_DIR,
        dfs=dfs,
        primary_keys=primary_keys,
        foreign_keys=foreign_keys
        )
    
    
if __name__ == "__main__":
    main()