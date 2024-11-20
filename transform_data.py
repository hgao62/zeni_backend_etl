import logging
from enum import Enum

import pandas as pd

from extract_data import get_exchange_rate, get_stock_currency_code

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
ZERO = 0
ONE = 1
TWO = 2

class StockHis(str, Enum):
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
            [StockHis.OPEN, StockHis.HIGH, StockHis.LOW, StockHis.CLOSE]
        ] = stock_history[
            [StockHis.OPEN, StockHis.HIGH, StockHis.LOW, StockHis.CLOSE]
        ].apply(
            lambda x: round(x + 10e-12, TWO)
        )
        stock_history.rename(
            columns={StockHis.DATE: StockHis.TRADEDATE}, inplace=True
        )
        return stock_history
    except Exception as e:
        logger.error("Error occurred normalize_stock_data: %s", e, exc_info=True)


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
        stock_history.sort_values(by=StockHis.TRADEDATE, ascending=True, inplace=True)
        stock_history[StockHis.DAILY_RETURN] = stock_history[
            StockHis.CLOSE
        ].pct_change()
        stock_history[StockHis.CUL_RETURN] = (
            ONE + stock_history[StockHis.DAILY_RETURN]
        ).cumprod() - ONE
        return stock_history
    except Exception as e:
        logger.error("Error occurred add_stock_returns: %s", e, exc_info=True)


class ToUsd(str, Enum):
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
            stock_history[ToUsd.USD_CLOSE] = stock_history[ToUsd.CLOSE]
        if not currency_code:
            raise ValueError(f"Could not retrieve currency code for {stock_ticker}")
        exchange_rate = get_exchange_rate(currency_code, "USD", "1d", "1d")[
            "Close"
        ].iloc[0]
        stock_history[ToUsd.USD_CLOSE] = stock_history[ToUsd.CLOSE] * exchange_rate
        return stock_history
    except Exception as e:
        logger.error("Error occurred standardize_price_to_usd: %s", e, exc_info=True)


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
        stock_history[StockHis.CLOSE_AVG] = (
            stock_history[StockHis.CLOSE].rolling(window=window).mean()
        )
        return stock_history
    except Exception as e:
        logger.error("Error occurred calculate_moving_average: %s", e, exc_info=True)
