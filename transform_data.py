import yfinance as yf
import pandas as pd

def normalize_stock_data(stock_history: pd.DataFrame) -> pd.DataFrame:
    """round open, high, low, close columns to 2 decimal places and rename data column to trade_data

    Args:
        stock_history (pd.DataFrame): stock history price

    Returns:
        pd.DataFrame: stock history price rounded to 2 decimal places
    """
    
    stock_history[['Open', 'High', 'Low', 'Close']]= stock_history[['Open', 'High', 'Low', 'Close']].apply(lambda x: round(x+10e-12, 2))
    stock_history.rename(columns={'Date': 'TradeDate'}, inplace=True)
    return stock_history