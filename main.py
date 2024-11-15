from typing import List

import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine

from extract_data import get_news, get_stock_financials, get_stock_history
from load_data import save_df_to_db
from transform_data import (
    add_stock_returns,
    calculate_moving_average,
    normalize_stock_data,
    standardize_price_to_usd,
)

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Loading main.py ...")

ENGINE = create_engine("mysql://airflow_user:airflow_pass@mysql:3306/airflow_db")


def run_pipeline(tickers: List[str], period: str = "1d", interval: str = "1d",) -> None:
    """store stocks price history, news and financials in a period into MySQL/SQLlite database

    Args:
        tickers (List[str]): a list of stock symbols 
        period (str, optional): query period (ex: '5d', '1mo', '1y'). Defaults to "1d".
        interval (str, optional): time interval (ex: '1d'). Defaults to "1d".
    """
    for ticker in tickers:
        logger.info("Staring saving %s history...", ticker)
        stock_history = get_stock_history(ticker, period, interval)
        stock_history = normalize_stock_data(stock_history)
        stock_history = add_stock_returns(stock_history)
        stock_history = standardize_price_to_usd(stock_history)
        stock_history = calculate_moving_average(stock_history)
        save_df_to_db(stock_history, "stock_history", ENGINE)
        logger.info("Successfully saved %s history.", ticker)

        logger.info("Staring saving %s news...", ticker)
        stock_news = get_news(ticker)
        save_df_to_db(stock_news, "news", ENGINE)
        logger.info("Successfully saved %s news.", ticker)

        logger.info("Staring saving %s financials...", ticker)
        stock_financials = get_stock_financials(ticker)
        save_df_to_db(stock_financials, "financial", ENGINE)
        logger.info("Successfully saved %s financials.", ticker)


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

    logger.info(
        "Finished running ETL job to save stock related market data into mysql database."
    )
