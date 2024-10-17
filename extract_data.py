import yfinance as yf
import pandas as pd

def get_stock_history(stock: str) -> pd.DataFrame:
    """pull 1 week stock history given a stock symbol input

    Args:
        stock (str): stock symbol

    Returns:
        pd.DataFrame: dataframe of 1 week daily stock price history on yahoo finance api
    """
    try:
        ticker = yf.Ticker(stock)
        df = ticker.history(period = '7d', interval = '1d').drop(columns=['Stock Splits']).reset_index()
        df['stock'] = stock
        return df
    except Exception as e:
        print(f'Error occurred: {e}')
        return pd.DataFrame()

def get_stock_financials(stock: str) -> pd.DataFrame:
    """get share holders of a stock given a stock name input

    Args:
        stock (str): stock name

    Returns:
        pd.DataFrame: dataframe of company income statement
    """
    try:
        ticker = yf.Ticker(stock)
        df = ticker.income_stmt.T
        if df.empty:
            raise ValueError(f'{stock}: No data found, symbol may be delisted')
        return df
    except Exception as e:
        print(f'Error occurred: {e}')
        return pd.DataFrame()