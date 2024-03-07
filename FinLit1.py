import yfinance as yf
import pandas as pd
from pypfopt.expected_returns import mean_historical_return
from pypfopt import risk_models
from pypfopt import expected_returns
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

class FinancialDataFetcher:
    def __init__(self, tickers):
        self.tickers = tickers

    def get_current_price(self, ticker):
        stock = yf.Ticker(ticker)
        todays_data = stock.history(period='1d')
        return todays_data['Close'].iloc[-1] if not todays_data.empty else "No data available"

    def get_next_earnings_date(self, ticker):
        stock = yf.Ticker(ticker)
        earnings_calendar = stock.calendar

        # Handle the earnings calendar when it's a dictionary
        if isinstance(earnings_calendar, dict):
            earnings_dates = earnings_calendar.get('Earnings Date')
            if earnings_dates:
                # Assuming 'Earnings Date' provides a list of dates or a single date
                if isinstance(earnings_dates, list):
                    # Convert dates to datetime.date objects if they're not already
                    earnings_dates = [datetime.strptime(str(date), '%Y-%m-%d').date() for date in earnings_dates]
                    future_dates = [date for date in earnings_dates if date > datetime.now().date()]
                    if future_dates:
                        # Return the nearest future date formatted as a string
                        return str(min(future_dates))
                else:
                    # Handle a single date (assuming it's already a datetime.date object or similar)
                    return str(earnings_dates)
        return "N/A"

    def calculate_pb_ratio(self, ticker):
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Fetch the last available close price and book value per share
            current_price = self.get_current_price(ticker)
            book_value_per_share = info.get('bookValue')
            
            # Calculate the P/B ratio if both values are available and book value is not zero
            if current_price and book_value_per_share and book_value_per_share != 0:
                pb_ratio = current_price / book_value_per_share
                return pb_ratio
            return "N/A"

    def fetch_financial_data(self):
        financial_data = {}
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            current_price = self.get_current_price(ticker)
            next_earnings_date = self.get_next_earnings_date(ticker)
            pb_ratio = self.calculate_pb_ratio(ticker)

            financial_data[ticker] = {
                'Current Price': current_price,
                'Volume': info.get('volume', "N/A"),
                'Market Cap': info.get('marketCap', "N/A"),
                'Beta (5Y Monthly)': info.get('beta', "N/A"),
                'PE Ratio (TTM)': info.get('trailingPE', "N/A"),
                'EPS (TTM)': info.get('trailingEps', "N/A"),
                'Next Earning Call Date': next_earnings_date,
                'P/B Ratio': pb_ratio
            }
        return financial_data

import unittest
from FinLit1 import FinancialDataFetcher  # Adjust 'your_module' to the name of your Python file containing the class

class TestFinancialDataFetcher(unittest.TestCase):
    def test_calculate_pb_ratio(self):
        fetcher = FinancialDataFetcher(tickers=['AAPL'])
        pb_ratio = fetcher.calculate_pb_ratio('AAPL')  # Use a well-known ticker to ensure data availability

        # Check if pb_ratio is a number and not "N/A"
        self.assertNotEqual(pb_ratio, "N/A", "P/B Ratio should not be 'N/A'")
        self.assertIsInstance(pb_ratio, (float, int), "P/B Ratio should be a number")

if __name__ == '__main__':
    # unittest.main()
    tickers = ["SMCI","AAPL","GOOGL"]
    data_fetcher = FinancialDataFetcher(tickers)
    financial_info = data_fetcher.fetch_financial_data()
    print(financial_info)



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


