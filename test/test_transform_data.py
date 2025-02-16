import pandas as pd
from pandas.testing import assert_series_equal
import pytest

from transform_data import add_stock_returns, normalize_stock_data


def test_add_stock_returns():
    test_df = pd.DataFrame(
        {
            "TradeDate": [
                "2024-10-25 00:00:00-04:00",
                "2024-10-30 00:00:00-04:00",
                "2024-10-28 00:00:00-04:00",
                "2024-10-31 00:00:00-04:00",
                "2024-10-29 00:00:00-04:00",
                "2024-11-01 00:00:00-04:00",
                "2024-11-04 00:00:00-05:00",
            ],
            "Close": [20.65, 23.98, 21.93, 22.22, 20.18, 21.90, 22.00],
        }
    )
    test_add_df = add_stock_returns(test_df)

    manual_add_df = test_df.sort_values(by="TradeDate", ascending=True, inplace=False)
    manual_add_df["last_close"] = manual_add_df["Close"].shift(1)
    manual_add_df["daily_return"] = (
        manual_add_df["Close"] - manual_add_df["last_close"]
    ) / manual_add_df["last_close"]

    cummulative_returns = []
    cummulative_return = 1
    for daily_return in manual_add_df["daily_return"].fillna(0):
        cummulative_return *= 1 + daily_return
        cummulative_returns.append(cummulative_return - 1)
    manual_add_df["cummulative_return"] = cummulative_returns

    for i in range(1, len(test_add_df)):
        assert test_add_df["daily_return"].iloc[i] == pytest.approx(
            manual_add_df["daily_return"].iloc[i], abs=1e-4
        )
    assert test_add_df["cummulative_return"].iloc[i] == pytest.approx(
        manual_add_df["cummulative_return"].iloc[i], abs=1e-4
    )


def test_normalize_stock_data():
    test_df = pd.DataFrame(
        {
            "Open": [21.47, 22.58],
            "High": [22.360001, 22.645],
            "Low": [21.548, 21.940001],
            "Close": [None, 22.999999],
            "Volume": [6702700, 6714800],
        }
    )

    test_nor_df = normalize_stock_data(test_df)
    test_open = test_nor_df["Open"].tolist()
    test_high = test_nor_df["High"].tolist()
    test_low = test_nor_df["Low"].tolist()
    test_close = test_nor_df["Close"].tolist()
    test_volume = test_nor_df["Volume"].tolist()

    assert test_open == [21.47, 22.58]
    assert test_high == [22.36, 22.65]
    assert test_low == [21.55, 21.94]
    assert_series_equal(pd.Series(test_close), pd.Series([None, 23.00]), check_exact=False)
    assert test_volume == [6702700, 6714800]
