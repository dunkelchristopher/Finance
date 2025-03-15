import pandas as pd
import requests
from fredapi import Fred
import datetime as dt

# Initialize FRED API
# Function to load API key from a text file
def load_api_key(service_name, filename="C:/Users/chdar/PycharmProjects/api_keys.txt"):  # Adjust path
    """Load the API key for a specific service from a text file."""
    with open(filename, "r") as file:
        for line in file:
            if line.startswith(service_name + "="):
                return line.split("=")[1].strip()
    raise ValueError(f"API key for {service_name} not found in {filename}")

# Load the FRED API key
api_key = load_api_key("FRED")

fred = Fred(api_key=api_key)

ticker_start = '2000-01-01'
ticker_end = '2025-02-28'

# List of ticker descriptions to retrieve data for
ticker_descriptions = [
    'S&P CoreLogic Case-Shiller U.S. National Home Price Index',
    'Crude Oil Prices: Brent - Europe',
    'Industrial Production: Total Index',
    'Sticky Price Consumer Price Index less Food and Energy',
    'Employed full time: Median usual weekly real earnings: Wage and salary workers: 16 years and over',
    'Job Openings: Total Nonfarm',
    'Quits: Total Nonfarm',
    'Unemployment Rate',
    '10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity',
    'GDPNow',
    'CBOE Volatility Index',
    'Personal Consumption Expenditures'

]

# Initialize an empty DataFrame to store results
finance_data = pd.DataFrame()

for ticker_description in ticker_descriptions:
    ticker_info = fred.search(ticker_description)

    if ticker_info is None or ticker_info.empty:
        print(f"Did not find ticker for '{ticker_description}'. Please revise your search.")
        continue

    ticker_id = ticker_info['id'].values[0]
    print(f"Fetching data for {ticker_id} ({ticker_description})")

    try:
        # Query the data from FRED
        series_data = fred.get_series(ticker_id, observation_start=ticker_start, observation_end=ticker_end)

        # Add to finance_data DataFrame
        finance_data[ticker_id] = series_data
    except Exception as e:
        print(f"Problem downloading '{ticker_id}' series: {e}")

# Display the last few rows of the data
print(finance_data.tail(15))
