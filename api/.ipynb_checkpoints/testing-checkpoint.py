import time
import pandas as pd
from polygon.rest import RESTClient
import config
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from ratelimit import limits, sleep_and_retry

start_time = time.time()

# List of API keys (replace with your actual keys)
api_keys = [
    config.polygon_api_1, config.polygon_api_2, config.polygon_api_3, config.polygon_api_4, config.polygon_api_5,
    config.polygon_api_6, config.polygon_api_7, config.polygon_api_8, config.polygon_api_9, config.polygon_api_10,
    config.polygon_api_11, config.polygon_api_12, config.polygon_api_13, config.polygon_api_14, config.polygon_api_15,
    config.polygon_api_16, config.polygon_api_17, config.polygon_api_18, config.polygon_api_19, config.polygon_api_20,
    config.polygon_api_21, config.polygon_api_22, config.polygon_api_23, config.polygon_api_24, config.polygon_api_25
]

# List of company symbols
#List of companies has been changed based on the use case,firstly used a lot of companies then changed after to get testing data for specified companies
symbols = [
    "AAPL", "GOOGL", "MSFT", "AMZN", "META",
    "TSLA", "F", "GM", "TM",
    "V", "MA", "JPM", "BAC", "WFC", "C",
    "KO", "PEP", "WMT", "COST", "HD",
    "JNJ", "PFE", "MRK", "ABBV", "MRNA", "BIIB",
    "XOM", "PSX", "DUK", "SHEL", "MPC"
]


# Set parameters for the API request
timeframe = 'day'
start_date = '2025-01-01'
end_date = '2025-01-31'

# API rate limit configuration
RATE_LIMIT_CALLS = 5
RATE_LIMIT_PERIOD = 60

@sleep_and_retry
@limits(calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_PERIOD)
def rate_limited_api_call(func, *args, **kwargs):
    return func(*args, **kwargs)

def get_bulk_data(symbol, start_date, end_date, api_key):
    """
    Retrieve data for a symbol within a date range using a specific API key.
    """
    client = RESTClient(api_key)
    try:
        return rate_limited_api_call(
            client.get_aggs, symbol, 1, timeframe, start_date, end_date, limit=50000
        )
    except Exception as e:
        print(f"Error retrieving data for {symbol} with key {api_key}: {e}")
        return None

def process_data(aggs, symbol):
    """
    Process raw aggregation data into a list of dictionaries.
    """
    return [
        {
            'symbol': symbol,
            't': agg.timestamp,
            'o': agg.open,
            'h': agg.high,
            'l': agg.low,
            'c': agg.close,
            'v': agg.volume,
            'n': agg.transactions,
        }
        for agg in aggs
    ]

def retrieve_data_for_symbol(symbol, api_key):
    """
    Retrieve data for a single symbol in one API call.
    """
    data = get_bulk_data(symbol, start_date, end_date, api_key)
    if data:
        return process_data(data, symbol)
    return []

def process_batch(batch_symbols, api_keys, batch_number):
    """
    Process a batch of symbols using the given API keys and save to a CSV file.
    """
    symbol_key_map = {symbol: api_keys[i % len(api_keys)] for i, symbol in enumerate(batch_symbols)}
    all_batch_data = []

    with ThreadPoolExecutor(max_workers=len(api_keys)) as executor:
        futures = {
            executor.submit(retrieve_data_for_symbol, symbol, api_key): symbol
            for symbol, api_key in symbol_key_map.items()
        }
        for future in as_completed(futures):
            symbol = futures[future]
            try:
                data = future.result()
                all_batch_data.extend(data)
                print(f"Data retrieval complete for symbol: {symbol}")
            except Exception as e:
                print(f"Error processing symbol {symbol}: {e}")

    # Convert to DataFrame
    final_df = pd.DataFrame(all_batch_data)
    final_df['t'] = pd.to_datetime(final_df['t'], unit='ms')

    # Save to CSV
    output_filename = f'batch_{batch_number}_data.csv'
    final_df.to_csv(output_filename, index=False)
    print(f"Batch {batch_number} saved to {output_filename}")

def main():
    batch_size = len(api_keys)
    total_batches = (len(symbols) + batch_size - 1) // batch_size

    for batch_number in range(total_batches):
        start_idx = batch_number * batch_size
        end_idx = min(start_idx + batch_size, len(symbols))
        batch_symbols = symbols[start_idx:end_idx]
        print(f"Processing batch {batch_number + 1}/{total_batches} with symbols: {batch_symbols}")
        process_batch(batch_symbols, api_keys, batch_number + 1)

if __name__ == "__main__":
    main()
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")
