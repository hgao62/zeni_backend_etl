import logging
from enum import Enum

import pandas as pd

from extract_data import get_exchange_rate, get_stock_currency_code

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
ZERO = 0
ONE = 1
TWO = 2

class stock_his(Enum):
    STOCK_SPLITES = "Stock Splits"
    DATE = "Date"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"
    VOLUME = "Volume"
    STOCK = "stock"
    TRADEDATE = "TradeDate"
    DAILY_RETURN = "daily_return"
    CUL_RETURN = "cummulative_return"
    CLOSE_AVG = "close_average"


def normalize_stock_data(stock_history: pd.DataFrame) -> pd.DataFrame:
    """round open, high, low, close columns to 2 decimal places and rename data column to trade_data

    Args:
        stock_history (pd.DataFrame): stock history price

    Returns:
        pd.DataFrame: stock history price rounded to 2 decimal places
    """
    try:
        stock_history[
            [stock_his.OPEN, stock_his.HIGH, stock_his.LOW, stock_his.CLOSE]
        ] = stock_history[
            [stock_his.OPEN, stock_his.HIGH, stock_his.LOW, stock_his.CLOSE]
        ].apply(
            lambda x: round(x + 10e-12, TWO)
        )
        stock_history.rename(
            columns={stock_his.DATE: stock_his.TRADEDATE}, inplace=True
        )
        return stock_history
    except Exception as e:
        logger.error(f"Error occurred normalize_stock_data: {e}", exc_info=True)


def add_stock_returns(stock_history: pd.DataFrame) -> pd.DataFrame:
    """adds two columns to stock_history data frame
        a. "daily_return": this is caluclated using the "close" price column
        b. "cummulative_return": this is caculated using the "daily_return" caculated 

    Args:
        stock_history (pd.DataFrame): stock history price

    Returns:
        pd.DataFrame: stock history with 2 return added
    """
    try:
        stock_history.sort_values(by=stock_his.TRADEDATE, ascending=True, inplace=True)
        stock_history[stock_his.DAILY_RETURN] = stock_history[
            stock_his.CLOSE
        ].pct_change()
        stock_history[stock_his.CUL_RETURN] = (
            ONE + stock_history[stock_his.DAILY_RETURN]
        ).cumprod() - ONE
        return stock_history
    except Exception as e:
        logger.error(f"Error occurred add_stock_returns: {e}", exc_info=True)


class to_usd(Enum):
    STOCK = "stock"
    USD_CLOSE = "usd_close"
    CLOSE = "Close"


def standardize_price_to_usd(stock_history: pd.DataFrame) -> pd.DataFrame:
    """stock price convert it to USD

    Args:
        stock_history (pd.DataFrame): stock history price

    Returns:
        pd.DataFrame: stock history with close price convert in USD
    """
    try:
        stock_ticker = stock_history["stock"].iloc[0]
        currency_code = get_stock_currency_code(stock_ticker)
        if currency_code == "USD":
            stock_history[to_usd.USD_CLOSE] = stock_history[to_usd.CLOSE]
        if not currency_code:
            raise ValueError(f"Could not retrieve currency code for {stock_ticker}")
        exchange_rate = get_exchange_rate(currency_code, "USD", "1d", "1d")[
            "Close"
        ].iloc[0]
        stock_history[to_usd.USD_CLOSE] = stock_history[to_usd.CLOSE] * exchange_rate
        return stock_history
    except Exception as e:
        logger.error(f"Error occurred standardize_price_to_usd: {e}", exc_info=True)


def calculate_moving_average(
    stock_history: pd.DataFrame, window: int = 5
) -> pd.DataFrame:
    """calculate the moving average of stock close price

    Args:
        stock_history (pd.DataFrame): stock history price
        window (int, optional): moving windows size. Defaults to 5.

    Returns:
        pd.DataFrame: stock history with moving average for 5 days
    """
    try:
        stock_history[stock_his.CLOSE_AVG] = (
            stock_history[stock_his.CLOSE].rolling(window=window).mean()
        )
        return stock_history
    except Exception as e:
        logger.error(f"Error occurred calculate_moving_average: {e}", exc_info=True)
