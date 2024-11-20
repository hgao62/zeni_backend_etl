import logging
from enum import Enum

import pandas as pd
import yfinance as yf

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class stock_history(Enum):
    STOCK_SPLITES = "Stock Splits"
    DATE = "Date"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"
    VOLUME = "Volume"
    DIVIDENDS = "Dividends"
    STOCK = "stock"


def get_stock_history(
    stock: str, period: str = "1d", interval: str = "1d"
) -> pd.DataFrame:
    """pull 1 week stock history given a stock symbol input

    Args:
        stock (str): stock symbol
        period (str): query period (ex: '5d', '1mo', '1y'). Defaults to '1d'.
        interval (str): time interval (ex: '1d'). Defaults to '1d'.

    Returns:
        pd.DataFrame: dataframe of 1 week daily stock price history on yahoo finance api
    """
    try:
        ticker = yf.Ticker(stock)
        df = (
            ticker.history(period=period, interval=interval)
            .drop(columns=[stock_history.STOCK_SPLITES.value])
            .reset_index()
        )
        df[stock_history.STOCK.value] = stock
        return df
    except Exception as e:
        logger.error(f"Error occurred get_stock_history: {e}", exc_info=True)
        return pd.DataFrame()


class stock_financials(Enum):
    INDEX = "index"
    DATE = "date"
    STOCK = "stock"


def get_stock_financials(stock: str) -> pd.DataFrame:
    """get share holders of a stock given a stock name input

    Args:
        stock (str): stock name

    Returns:
        pd.DataFrame: dataframe of company income statement
    """
    output_columns = [
        "date",
        "Tax Effect Of Unusual Items",
        "Tax Rate For Calcs",
        "Normalized EBITDA",
        "Net Income From Continuing Operation Net Minority Interest",
        "Reconciled Depreciation",
        "Reconciled Cost Of Revenue",
        "EBITDA",
        "EBIT",
        "Net Interest Income",
        "Interest Expense",
        "Interest Income",
        "Normalized Income",
        "Net Income From Continuing And Discontinued Operation",
        "Total Expenses",
        "Total Operating Income As Reported",
        "Diluted Average Shares",
        "Basic Average Shares",
        "Diluted EPS",
        "Basic EPS",
    ]
    try:
        ticker = yf.Ticker(stock)
        df = ticker.income_stmt.T.reset_index()
        df.rename(columns={stock_financials.INDEX.value: stock_financials.DATE.value}, inplace=True)
        df[stock_financials.INDEX.value] = pd.to_datetime(df[stock_financials.INDEX.value])
        df = df[output_columns]
        output_columns_renamed = {col: col.replace(" ", "_") for col in output_columns}
        df.rename(columns=output_columns_renamed, inplace=True)
        df[stock_financials.STOCK.value] = stock
        if df.empty:
            raise ValueError(f"{stock}: No data found, symbol may be delisted")
        return df
    except Exception as e:
        logger.error(f"Error occurred get_stock_financials: {e}", exc_info=True)
        return pd.DataFrame()


class exchange_rate(Enum):
    VOLUME = "Volume"
    TICKER = "Ticker"
    FROM_CURRENCY = "From Currency"
    TO_CURRENCY = "To Currency"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"


def get_exchange_rate(
    from_currency: str, to_currency: str, period: str = "1d", interval: str = "1d"
) -> pd.DataFrame:
    """get the exchange rate of two currencys

    Args:
        from_currency (str): original currency code
        to_currency (str): goal currency code
        period (str): exchange rate period (ex: '5d', '1mo', '1y'). Defaults to '1d'
        interval (str): exchange rate time interval (ex: '1d'). Defaults to '1d'

    Returns:
        pd.DataFrame: dataframe of currency exchange rate
    """
    try:
        fx_rate_ticker = f"{from_currency}{to_currency}=X"
        fx_rates = (
            yf.download(fx_rate_ticker, period=period, interval=interval)
            .drop(columns=[exchange_rate.VOLUME.value])
            .reset_index()
        )
        fx_rates[exchange_rate.TICKER.value] = fx_rate_ticker
        fx_rates[exchange_rate.FROM_CURRENCY.value] = from_currency
        fx_rates[exchange_rate.TO_CURRENCY.value] = to_currency
        return fx_rates[
            [
                "Date",
                "Ticker",
                "From Currency",
                "To Currency",
                "Open",
                "High",
                "Low",
                "Close",
                "Adj Close",
            ]
        ]
    except Exception as e:
        logger.error(f"Error occurred get_exchange_rate: {e}", exc_info=True)
        return pd.DataFrame()


class stock_currency(Enum):
    FINANCIAL = "financialCurrency"


def get_stock_currency_code(stock: str) -> str:
    """get the currency code for input stock

    Args:
        stock (str): stock symbol

    Returns:
        str: currency code
    """
    try:
        stock_ticker = yf.Ticker(stock)
        currency_code = stock_ticker.info[stock_currency.FINANCIAL.value]
        return currency_code
    except Exception as e:
        logger.error(f"Error occurred get_stock_currency_code: {e}", exc_info=True)
        return None


class news(Enum):
    THUMBNAIL = "thumbnail"
    RELATED_TICKERS = "relatedTickers"
    PUBLISHTIME = "providerPublishTime"


def get_news(stock: str) -> pd.DataFrame:
    """get relevant news belongs to that company

    Args:
        stock (str): stock symbol

    Returns:
        pd.DataFrame: dataframe of relative news of company
    """
    try:
        stock_ticker = yf.Ticker(stock)
        stock_news = pd.DataFrame(stock_ticker.news)
        stock_news = stock_news.drop(columns=[news.THUMBNAIL.value, news.RELATED_TICKERS.value])
        stock_news[news.PUBLISHTIME.value] = pd.to_datetime(
            stock_news[news.PUBLISHTIME.value], unit="s"
        )  # timestamp to date
        stock_news["Ticker"] = stock
        return stock_news
    except Exception as e:
        logger.error(f"Error occurred get_news: {e}", exc_info=True)
        return pd.DataFrame()
