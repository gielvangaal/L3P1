import pandas as pd


def extract_csv(path):
    return pd.read_csv(
        path,
        low_memory=False
    )


def extract_excel(path):
    return pd.read_excel(path)