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
        df['stock'] = stock
        if df.empty:
            raise ValueError(f'{stock}: No data found, symbol may be delisted')
        return df
    except Exception as e:
        print(f'Error occurred: {e}')
        return pd.DataFrame()

def get_exchange_rate(from_currency: str, to_currency: str, period: str, interval: str) -> pd.DataFrame:
    """get the exchange rate of two currencys

    Args:
        from_currency (str): original currency code
        to_currency (str): goal currency code
        period (str): exchange rate period (ex: '5d', '1mo', '1y')
        interval (str): exchange rate time interval (ex: '1d')

    Returns:
        pd.DataFrame: dataframe of currency exchange rate
    """
    try:
        fx_rate_ticker = f"{from_currency}{to_currency}=X"
        fx_rates = yf.download(fx_rate_ticker, period=period, interval=interval).drop(columns = ['Volume']).reset_index()
        fx_rates['Ticker'] = fx_rate_ticker
        fx_rates['From Currency'] = from_currency
        fx_rates['To Currency'] = to_currency
        cols = fx_rates.columns.tolist()
        return fx_rates[cols[:1] + cols[-3:] + cols[1: -3]]
    except Exception as e:
        print(f'Error occurred: {e}')
        return pd.DataFrame()

def get_stock_currency_code(stock: str) -> str:
    """get the currency code for input stock

    Args:
        stock (str): stock symbol

    Returns:
        str: currency code
    """
    try:
        stock_ticker = yf.Ticker(stock)
        currency_code = stock_ticker.info['financialCurrency']
        return currency_code
    except Exception as e:
        print(f'Error occurred: {e}')
        return None
    
def get_news(stock: str) -> pd.DataFrame:
    """get relevant news belongs to that company

    Args:
        stock (str): stock symbol

    Returns:
        pd.DataFrame: dataframe of relative news of company
    """
    try:
        stock_ticker = yf.Ticker(stock)
        news = pd.DataFrame(stock_ticker.news).drop(columns = ['thumbnail', 'relatedTickers'])
        news['providerPublishTime'] = pd.to_datetime(news['providerPublishTime'], unit='s') # timestamp to date
        news['Ticker'] = stock
        return news
    except Exception as e:
        print(f'Error occurred: {e}')
        return pd.DataFrame()
