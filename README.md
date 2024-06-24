# Real-Time Stock Market Data Pipeline

## Objective
The objective of this project is to build a data pipeline that collects, processes, and analyzes real-time stock market data. The pipeline extracts data from a financial market API, processes it to calculate key metrics, and stores the processed data in a database for visualization using tools like Tableau or Power BI.

## API
This project uses the Finnhub API to fetch real-time stock data. You can replace it with other financial market APIs like Alpha Vantage, Yahoo Finance API, or IEX Cloud if needed.

## Features
- Extract real-time stock data using the Finnhub API.
- Process the data to calculate key metrics.
- Store the processed data in a SQLite database.
- Transform the data to include additional time-based columns.
- Load the data into a database for further analysis and visualization.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/real-time-stock-market-data-pipeline.git
    cd real-time-stock-market-data-pipeline
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
1. Obtain an API key from [Finnhub](https://finnhub.io).
2. Replace `'your_finnhub_api_key'` in the code with your actual API key.

## Usage
### Extract Data
The `extract_stock_data` function fetches real-time stock quotes for the given symbols using the Finnhub API and stores the data in a pandas DataFrame.

### Transform Data
The `transform_stock_data` function cleans the data, removes unwanted columns, converts timestamps, and extracts additional time-based columns.

### Load Data
The `load_data_to_sqlite` function creates a SQLite database and table (if they don't exist) and inserts the transformed data into the table.

## Code
Here's the complete code for the ETL pipeline:
