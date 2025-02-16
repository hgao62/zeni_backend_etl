import logging

import pandas as pd
from sqlalchemy import engine

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def save_df_to_db(
    df: pd.DataFrame,
    table_name: str,
    engine: engine,
    if_exists: str = "append",
    dtype=None,
) -> None:
    """Function to send a dataframe to SQL database.

    Args:
        df (pd.DataFrame): DataFrame to be sent to the SQL database.
        table_name (str): Name of the table in the SQL database.
        engine (sqlalchemy.engine): db engine type (sqlite or mysql)
        if_exists (str, optional): Action to take if the table already exists in the SQL database.
                                   Options: "fail", "replace", "append" 
                                   Defaults to"append".
        dtype (_type_, optional): Dictionary of column names and data types to be used when creating the table.
                                  Defaults to None.
    """

    if df.empty or df.columns.empty:
        logger.warning(f"No data to save to table {table_name}")
        return
    
    try:
        with engine.connect() as connection:
            df.to_sql(
                table_name,
                con=connection,
                if_exists=if_exists,
                index=False,
                dtype=dtype,
            )
    except AssertionError:
        logger.error("Dataframe is empty or database ENGINE is not initialized.")
    except Exception as e:
        logger.error(f"Unexcepted error {e}", exc_info=True)
