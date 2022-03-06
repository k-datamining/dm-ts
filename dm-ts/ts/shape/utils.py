import os
import numpy as np
import pandas as pd
import time

import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError


def get_finance_data(ticker_symbol:str, source="yahoo",start="2021-01-01", end="2021-06-30", savedir="data") -> pd.DataFrame:
    """株価を記録したデータを取得します

    Args:
        ticker_symbol (str): Description of param1
        start (str): 期間はじめの日付, optional.
        end (str): 期間終わりの日付, optional.

    Returns:
        res: 株価データ

    """
    res = None
    filepath = os.path.join(savedir, f"{ticker_symbol}_{start}_{end}_historical.csv")
    os.makedirs(savedir, exist_ok=True)

    if not os.path.exists(filepath):
        try:
            time.sleep(5.0)  # MEMO: 連続アクセスを避ける
            res = web.DataReader(ticker_symbol, source, start=start, end=end)
            res.to_csv(filepath, encoding="utf-8-sig")
        except (RemoteDataError, KeyError):
            print(f"ticker_symbol ${ticker_symbol} が正しいか確認してください。")
    else:
        res = pd.read_csv(filepath, index_col="Date")
        res.index = pd.to_datetime(res.index)

    assert res is not None, "データ取得に失敗しました"
    return res
