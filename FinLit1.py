import yfinance as yf
import pandas as pd
from datetime import datetime

def check_tickers():
    """
    Prompts the user to input a list of stock ticker symbols separated by commas.
    Validates each ticker using yfinance to ensure it exists and is actively traded.
    A ticker is considered valid if its info dictionary contains 'regularMarketPrice',
    'longName', or 'shortName'. If any tickers are invalid, the user is prompted
    to re-enter the entire list. The process repeats until all tickers are valid.
    Once validated, it prints and returns the list of valid tickers.
    
    Returns:
        list: A list of valid ticker symbols entered by the user.
    """
    while True:  # Keep asking for input until all tickers are valid
        user_input = input("Enter your portfolio tickers separated by a comma (e.g., AAPL,GOOGL): ")
        tickers = [ticker.strip() for ticker in user_input.split(',')]  # Split and trim input string into a list

        tickers_not_found = []  # Initialize a list for tickers not found
        valid_tickers = []  # Initialize a list for valid tickers

        for ticker in tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            # Check for specific fields that are expected to be populated for valid tickers
            if 'regularMarketPrice' not in info and 'longName' not in info and 'shortName' not in info:
                tickers_not_found.append(ticker)
            else:
                valid_tickers.append(ticker)
        
        if tickers_not_found:
            # Inform the user which tickers were not found and prompt for re-entry
            print("The following tickers were not found: ", ', '.join(tickers_not_found))
            print("Please review them and try again.")
        else:
            # If all tickers are valid, inform the user
            print("All tickers are valid:", ', '.join(valid_tickers))
            return valid_tickers  # Return the list of valid tickers directly

# print(check_tickers())

def fetch_financial_data(tickers):
    financial_data = {}
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Attempt to fetch the earnings calendar
        earnings_calendar = stock.calendar

        # Handle the earnings date based on its format
        if isinstance(earnings_calendar, dict) and 'Earnings Date' in earnings_calendar:
            earnings_dates = earnings_calendar['Earnings Date']
            # Check if earnings_dates is a list and find the next earnings date
            if isinstance(earnings_dates, list):
                next_earnings_date = next((date for date in earnings_dates if date > datetime.now().date()), "N/A")
            else:
                next_earnings_date = "N/A"
        else:
            next_earnings_date = "N/A"
        
        financial_data[ticker] = {
            'Current Price': info.get('regularMarketPrice'),
            'Volume': info.get('volume'),
            'Market Cap': info.get('marketCap'),
            'Beta (5Y Monthly)': info.get('beta'),
            'PE Ratio (TTM)': info.get('trailingPE'),
            'EPS (TTM)': info.get('trailingEps'),
            'Next Earning Call Date': str(next_earnings_date)  # Convert to string for consistency
        }

    return financial_data

# Example usage
# valid_tickers = ['GTLB', 'MSFT']  # Use the output from your ticker validation function
# financial_info = fetch_financial_data(valid_tickers)
# print(financial_info)


# def export_earnings_calendar_to_csv(ticker_symbol):
#     """
#     Fetches the earnings calendar for the specified ticker symbol and exports it to a CSV file.
    
#     Parameters:
#     ticker_symbol (str): The stock ticker symbol to fetch the earnings calendar for.
#     """
#     stock = yf.Ticker(ticker_symbol)
#     earnings_calendar = stock.calendar
    
#     # Define the CSV file name based on the ticker symbol
#     csv_file_name = f"{ticker_symbol}_earnings_calendar.csv"
    
#     if isinstance(earnings_calendar, dict):
#         # If earnings_calendar is a dict, convert it to a DataFrame
#         df = pd.DataFrame(list(earnings_calendar.items()), columns=['Event', 'Date'])
#         df.to_csv(csv_file_name, index=False)
#         print(f"Earnings Calendar for {ticker_symbol} has been saved to {csv_file_name}")
#     elif not earnings_calendar.empty:
#         # If earnings_calendar is already a DataFrame and not empty, save it directly
#         earnings_calendar.to_csv(csv_file_name, index=False)
#         print(f"Earnings Calendar for {ticker_symbol} has been saved to {csv_file_name}")
#     else:
#         print(f"No earnings calendar data available for {ticker_symbol} to export.")

# # Example usage - Replace 'AAPL' with any ticker you're interested in
# ticker_symbol = 'AAPL'
# export_earnings_calendar_to_csv(ticker_symbol)


