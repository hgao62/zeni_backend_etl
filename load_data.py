import yfinance as yf
import pandas as pd
import sqlite3
import sqlalchemy

def save_df_to_db(
        df:pd.DataFrame, table_name:str,  engine: sqlalchemy.engine.Engine, if_exists:str = "append", dtype=None,
) -> None:
    """Function to send a dataframe to SQL database.

    Args:
        df (pd.DataFrame): DataFrame to be sent to the SQL database.
        table_name (str): Name of the table in the SQL database.
        engine (sqlalchemy.engine.Engine): db engine type (sqlite or mysql)
        if_exists (str, optional): Action to take if the table already exists in the SQL database.
                                   Options: "fail", "replace", "append" 
                                   Defaults to"append".
        dtype (_type_, optional): Dictionary of column names and data types to be used when creating the table.
                                  Defaults to None.
    """
    df.to_sql(df, table_name, engine, if_exists, dtype)