import json


def load_csv(data, path):
    data.to_csv(path, index=False)


def load_geojson(data, path):
    with open(file=path, mode="w", encoding="utf-8") as file:
        json.dump(obj=data, fp=file, ensure_ascii=False)