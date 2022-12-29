import pathlib
import sqlite3
import pandas as pd





def get_wind_data():
    """
    Query wind data rows between two ranges

    :params start: start row id
    :params end: end row id
    :returns: pandas dataframe object
    """
    data = pd.read_csv("../soil.csv")
    data.set_index(['date'], inplace = True)
    df= data["segment1(10-30cm)"]
    return df


def get_wind_data_by_id(i):
    """
    Query a row from the Wind Table

    :params id: a row id
    :returns: pandas dataframe object
    """
    df = pd.read_csv("../soil.csv")
    df.set_index(['date'], inplace = True)

    return df
