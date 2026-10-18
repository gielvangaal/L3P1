import pandas as pd
import json


def extract_csv(path):
    return pd.read_csv(
        path,
        low_memory=False
    )


def extract_excel(path):
    return pd.read_excel(path)


def extract_geojson(path):
    with open(file=path, mode="r", encoding="utf-8") as file:
        return json.load(fp=file)