from __future__ import annotations

import string
from typing import List, Any

import pandas as pd
import numpy as np
from pandas import DataFrame


def open_file(path: string) -> DataFrame:
    return pd.read_csv(path)


def open_file_to_numpy(path: string) -> np.ndarray:
    return to_numpy(open_file(path))


def to_numpy(pandas_dataframe: DataFrame) -> np.ndarray:
    return pandas_dataframe.to_numpy()


class CsvWriter:
    def __init__(self, path: str, columns):
        self.columns = columns
        self.path = path
        self.row_data = []

    def write_row(self, row: np.ndarray | list):
        self.row_data.append(row)

    def get(self) -> list:
        return self.row_data

    def print_(self):
        for item in self.row_data:
            print(item)

    def fresh(self):
        pd.DataFrame(self.row_data, columns=self.columns).to_csv(self.path)
