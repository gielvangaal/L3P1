import pandas as pd
import pycountry


# DIM DATE
def transform_dim_date(df):
    df = df.copy()

    df = df[df["Year"].between(2011, 2013)]

    df = df.drop(columns=["Year.1"])

    df["Date"] = pd.to_datetime(
        df["DateInt"].astype(str),
        format="%Y%m%d"
    )

    return df


# DIM CHANNEL
def transform_dim_channel(df):
    df = df.copy()

    return df


# FACT WEATHER
def transform_fact_weather(df):
    df = df.copy()

    df = df.drop(columns=["ValueType"])

    # Datum als echte datum opslaan
    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%Y-%m-%d"
    )

    return df


# DIM GEOGRAPHY
def transform_dim_geography(df):
    df = df.copy()

    return df


# DIM PRODUCT
def transform_dim_product(df):
    df = df.copy()

    for column in ["UnitCost", "UnitPrice"]:
        df[column] = pd.to_numeric(
            df[column]
                .astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(",", ".", regex=False),
            errors="coerce"
        )

    return df


# DIM PRODUCT CATEGORY
def transform_dim_product_category(df):
    df = df.copy()

    return df


# DIM PRODUCT SUBCATEGORY
def transform_dim_product_subcategory(df):
    df = df.copy()

    return df


# DIM PROMOTION
def transform_dim_promotion(df):
    df = df.copy()

    df = df.rename(columns={
        "Year": "EndYear",
        "Quarter": "EndQuarter",
        "Month": "EndMonth",
        "Day": "EndDay",
        "Year.1": "StartYear",
        "Quarter.1": "StartQuarter",
        "Month.1": "StartMonth",
        "Day.1": "StartDay",
    })

    return df


# FACT SALES
def transform_fact_sales(df):
    df = df.copy()

    df["DateKey"] = pd.to_datetime(
        df["DateKey"],
        format="%Y-%m-%d %H:%M:%S,%f"
    )

    money_columns = [
        "UnitCost",
        "UnitPrice",
        "ReturnAmount",
        "DiscountAmount",
        "TotalCost",
        "SalesAmount"
    ]

    for column in money_columns:
        df[column] = pd.to_numeric(
            df[column]
                .astype(str)
                .str.replace(",", ".", regex=False),
            errors="coerce"
        )

    return df


# DIM STORE
def transform_dim_store(df):
    df = df.copy()

    return df


# DIM COUNTRY
def transform_dim_country(dim_geography, fact_weather):
    countries = pd.concat([
        dim_geography["RegionCountryName"],
        fact_weather["Country"]
    ])

    dim_country = (
        countries
        .dropna()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
        .to_frame(name="Country")
    )

    country_mapping = {
        "Russia": "RUS",
        "the Netherlands": "NLD"
    }

    def get_iso3(country):
        if country in country_mapping:
            return country_mapping[country]

        return pycountry.countries.lookup(country).alpha_3

    dim_country["CountryISO3"] = dim_country["Country"].apply(
        get_iso3
    )

    return dim_country


# GEOJSON
def transform_geojson(data):
    return data