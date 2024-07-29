Banks ETL Project
Project Overview
This project demonstrates the process of extracting, transforming, and loading (ETL) data related to the world's largest banks by market capitalization. The data is scraped from a web page, transformed according to specified exchange rates, and then loaded into both a CSV file and a SQLite database. The project also includes logging functionality to track the progress of the ETL process.

Table of Contents
Project Overview
Prerequisites
Project Structure
Setup and Execution
Code Description
1. Logging Function
2. Data Extraction
3. Data Transformation
4. Load Data to CSV
5. Load Data to Database
6. Run SQL Queries
7. Main Script Execution
Logging
Acknowledgements
Prerequisites
To run this project, you need the following libraries:

requests
beautifulsoup4
pandas
numpy
sqlite3
You can install these libraries using pip:

sh
Copy code
pip install requests beautifulsoup4 pandas numpy sqlite3
Project Structure
The project contains the following files:

banks_project.py: The main script containing the ETL process.
exchange_rate.csv: A CSV file containing exchange rates used for data transformation.
code_log.txt: The log file that records the progress of the ETL process.
Setup and Execution
Clone the repository:

sh
Copy code
git clone https://github.com/yourusername/banks-etl-project.git
cd banks-etl-project
Ensure exchange_rate.csv is in the project directory:
Download exchange_rate.csv from the provided source and place it in the same directory as banks_project.py.

Remove existing log file (if any):

sh
Copy code
rm code_log.txt
Run the script:

sh
Copy code
python banks_project.py
Code Description
1. Logging Function
Logs the progress at various stages of the ETL process.

python
Copy code
def log_progress(message):
    with open('code_log.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} : {message}\n")
2. Data Extraction
Extracts data from a specified URL and saves it to a DataFrame.

python
Copy code
def extract(url, table_attribs):
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
3. Data Transformation
Transforms the extracted data by adding columns for GBP, EUR, and INR based on exchange rates.

python
Copy code
def transform(df, csv_path):
    exchange_rates = pd.read_csv(csv_path, index_col=0)
    exchange_rates_dict = exchange_rates.squeeze().to_dict()
    
    df['MC_USD_Billion'] = df['Market cap(US$ billion)'].astype(float)
    
    df['MC_GBP_Billion'] = [np.round(x * exchange_rates_dict['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_rates_dict['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_rates_dict['INR'], 2) for x in df['MC_USD_Billion']]
    
    log_progress("Data transformation complete. Initiating Loading process")
    return df
4. Load Data to CSV
Saves the transformed DataFrame to a CSV file.

python
Copy code
def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    log_progress("Data saved to CSV file")
5. Load Data to Database
Loads the transformed DataFrame to a SQLite database table.

python
Copy code
def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    log_progress("Data loaded to Database as a table, Executing queries")
6. Run SQL Queries
Executes SQL queries on the database and prints the results.

python
Copy code
def run_query(query_statement, sql_connection):
    cursor = sql_connection.cursor()
    cursor.execute(query_statement)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
7. Main Script Execution
Executes the ETL process step-by-step and logs the progress.

python
Copy code
log_progress("Preliminaries complete. Initiating ETL process")

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = {'class': 'wikitable'}
df = extract(url, table_attribs)
print(df)

print("DataFrame columns:", df.columns)

csv_path = 'exchange_rate.csv'
df_transformed = transform(df, csv_path)
print("Transformed DataFrame:")
print(df_transformed)

output_path = 'Largest_banks_data.csv'
load_to_csv(df_transformed, output_path)

connection = sqlite3.connect('Banks.db')
log_progress("SQL Connection initiated")
table_name = 'Largest_banks'
load_to_db(df_transformed, connection, table_name)

print("Query results:")
run_query("SELECT [Bank name] from Largest_banks LIMIT 5", connection)
run_query("SELECT AVG([MC_GBP_Billion]) FROM Largest_banks", connection)
run_query("SELECT [Bank name] from Largest_banks LIMIT 5", connection)

log_progress("Process Complete")
connection.close()
log_progress("Server Connection closed")
Logging
The code_log.txt file contains log entries that track the progress of the ETL process. Each entry includes a timestamp and a message indicating the stage of the process.

Example log entries:

yaml
Copy code
2024-07-29 10:15:00 : Preliminaries complete. Initiating ETL process
2024-07-29 10:15:10 : Data extraction complete. Initiating Transformation process
2024-07-29 10:15:20 : Data transformation complete. Initiating Loading process
2024-07-29 10:15:30 : Data saved to CSV file
2024-07-29 10:15:40 : SQL Connection initiated
2024-07-29 10:15:50 : Data loaded to Database as a table, Executing queries
2024-07-29 10:16:00 : Process Complete
2024-07-29 10:16:10 : Server Connection closed
Acknowledgements
This project was created as part of an educational exercise to demonstrate ETL processes using Python. The data source and exchange rate information used in this project are for demonstration purposes only.
