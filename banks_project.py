from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    with open('code_log.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} : {message}\n")

def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', attrs=table_attribs)
    
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        rows.append(cols)
    
    df = pd.DataFrame(rows, columns=headers)
    log_progress("Data extraction complete. Initiating Transformation process")
    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    exchange_rates = pd.read_csv(csv_path, index_col=0)
    exchange_rates_dict = exchange_rates.squeeze().to_dict()
    
    df['MC_USD_Billion'] = df['Market cap(US$ billion)'].astype(float)
    
    df['MC_GBP_Billion'] = [np.round(x * exchange_rates_dict['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_rates_dict['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_rates_dict['INR'], 2) for x in df['MC_USD_Billion']]
    
    log_progress("Data transformation complete. Initiating Loading process")
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path, index=False)
    log_progress("Data saved to CSV file")

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    log_progress("Data loaded to Database as a table, Executing queries")

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    cursor = sql_connection.cursor()
    cursor.execute(query_statement)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Main script
log_progress("Preliminaries complete. Initiating ETL process")

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = {'class': 'wikitable'}
df = extract(url, table_attribs)
print(df)

csv_path = 'D:\\Projects\\data eng\\Banks\\exchange_rate.csv'
df_transformed = transform(df, csv_path)
print(df_transformed)

# Load the transformed DataFrame to a CSV file
output_path = 'D:\\Projects\\data eng\\Banks\\Largest_banks_data.csv'
load_to_csv(df_transformed, output_path)

# Load the transformed DataFrame to a database
connection = sqlite3.connect('D:\\Projects\\data eng\\Banks\\Banks.db')
log_progress("SQL Connection initiated")
table_name = 'Largest_banks'
load_to_db(df_transformed, connection, table_name)

# Run the specified queries
print("Query results:")
run_query("SELECT [Bank name] from Largest_banks LIMIT 5", connection)
run_query("SELECT AVG([MC_GBP_Billion]) FROM Largest_banks", connection)
run_query("SELECT [Bank name] from Largest_banks LIMIT 5", connection)

log_progress("Process Complete")
connection.close()
log_progress("Server Connection closed")
