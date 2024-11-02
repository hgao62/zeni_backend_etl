import pandas as pd
from sqlalchemy import create_engine

ENGINE = create_engine("sqlite:///yf_finance.db")
def save_df_to_db(
        df:pd.DataFrame, table_name:str, engine, if_exists:str = "append", dtype=None,
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
    with engine.connect() as connection:
        df.to_sql(table_name, con=connection, if_exists = if_exists, index=False, dtype = dtype)

import extract_data as ed
df = ed.get_stock_history('msft')
save_df_to_db(df, 'test_table', ENGINE)