import logging

import pandas as pd

from extract_data import get_exchange_rate, get_stock_currency_code

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize_stock_data(stock_history: pd.DataFrame) -> pd.DataFrame:
    """round open, high, low, close columns to 2 decimal places and rename data column to trade_data

    Args:
        stock_history (pd.DataFrame): stock history price

    Returns:
        pd.DataFrame: stock history price rounded to 2 decimal places
    """
    try:
        stock_history[["Open", "High", "Low", "Close"]] = stock_history[
            ["Open", "High", "Low", "Close"]
        ].apply(lambda x: round(x + 10e-12, 2))
        stock_history.rename(columns={"Date": "TradeDate"}, inplace=True)
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
        stock_history.sort_values(by="TradeDate", ascending=True, inplace=True)
        stock_history["daily_return"] = stock_history["Close"].pct_change()
        stock_history["cummulative_return"] = (
            1 + stock_history["daily_return"]
        ).cumprod() - 1
        return stock_history
    except Exception as e:
        logger.error(f"Error occurred add_stock_returns: {e}", exc_info=True)


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
            stock_history["usd_close"] = stock_history["Close"]
        if not currency_code:
            raise ValueError(f"Could not retrieve currency code for {stock_ticker}")
        exchange_rate = get_exchange_rate(currency_code, "USD", "1d", "1d")[
            "Close"
        ].iloc[0]
        stock_history["usd_close"] = stock_history["Close"] * exchange_rate
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
        stock_history["close_average"] = (
            stock_history["Close"].rolling(window=window).mean()
        )
        return stock_history
    except Exception as e:
        logger.error(f"Error occurred calculate_moving_average: {e}", exc_info=True)
