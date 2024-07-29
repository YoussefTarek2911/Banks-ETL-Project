# Banks ETL Project

## Project Overview

This project demonstrates the process of extracting, transforming, and loading (ETL) data related to the world's largest banks by market capitalization. The data is scraped from a web page, transformed according to specified exchange rates, and then loaded into both a CSV file and a SQLite database. The project also includes logging functionality to track the progress of the ETL process.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup and Execution](#setup-and-execution)
- [Code Description](#code-description)
  - [1. Logging Function](#1-logging-function)
  - [2. Data Extraction](#2-data-extraction)
  - [3. Data Transformation](#3-data-transformation)
  - [4. Load Data to CSV](#4-load-data-to-csv)
  - [5. Load Data to Database](#5-load-data-to-database)
  - [6. Run SQL Queries](#6-run-sql-queries)
  - [7. Main Script Execution](#7-main-script-execution)
- [Logging](#logging)
- [Acknowledgements](#acknowledgements)

## Prerequisites

To run this project, you need the following libraries:
- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `sqlite3`

You can install these libraries using pip:
```sh
pip install requests beautifulsoup4 pandas numpy
