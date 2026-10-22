# US-CEO-1
# FactSales
def model_ceo_1(processed):
    return processed["sales"]


# US-CEO-2
# FactSales * ---> 1 DimDate
def model_ceo_2(processed):
    return processed["sales"].merge(
        processed["calendar"],
        left_on="DateKey",
        right_on="Date",
        how="left"
    )


# US-CEO-3
# FactSales * ---> 1 DimChannel
def model_ceo_3(processed):
    return processed["sales"].merge(
        processed["channel"],
        left_on="channelKey",
        right_on="Channel",
        how="left"
    )


# US-CEO-4
# FactSales * ---> 1 DimStore
# DimStore * ---> 1 DimGeography
# DimGeography * ---> 1 DimCountry
def model_ceo_4(processed):
    df = processed["sales"].merge(
        right=processed["store"],
        on="StoreKey",
        how="left"
    )

    df = df.merge(
        right=processed["geography"],
        on="GeographyKey",
        how="left"
    )

    df = df.merge(
        right=processed["country"],
        left_on="RegionCountryName",
        right_on="Country",
        how="left",
        validate="many_to_one"
    )

    return df


# US-CEO-5
# FactSales * ---> 1 DimDate
# FactWeather * ---> 1 DimDate
def model_ceo_5(processed):
    sales = processed["sales"].merge(
        processed["calendar"],
        left_on="DateKey",
        right_on="Date",
        how="left"
    )

    sales_monthly = (
        sales
        .groupby(["Year", "MonthOfYear"])["SalesAmount"]
        .sum()
        .reset_index()
    )

    weather_monthly = (
        processed["weather"]
        .groupby(["Year", "MonthNumber"])["EstimatedDailyTemperature"]
        .mean()
        .reset_index()
    )

    return sales_monthly.merge(
        weather_monthly,
        left_on=["Year", "MonthOfYear"],
        right_on=["Year", "MonthNumber"],
        how="left"
    )


# US-FM-1
# FactSales
def model_fm_1(processed):
    return processed["sales"]


# US-FM-2
# FactSales * ---> 1 DimDate
def model_fm_2(processed, store_key):
    sales = processed["sales"][
        processed["sales"]["StoreKey"] == store_key
    ]

    return sales.merge(
        processed["calendar"],
        left_on="DateKey",
        right_on="Date",
        how="left"
    )


# US-FM-3
# FactSales * ---> 1 DimProduct
def model_fm_3(processed, store_key):
    sales = processed["sales"][
        processed["sales"]["StoreKey"] == store_key
    ]

    return sales.merge(
        processed["product"],
        on="ProductKey",
        how="left"
    )


# US-FM-4
# FactSales
def model_fm_4(processed, store_key):
    return processed["sales"].loc[
        processed["sales"]["StoreKey"] == store_key
    ]


# US-FM-5
# FactSales * ---> 1 DimStore
# DimStore * ---> 1 DimGeography
# FactSales.DateKey ---> FactWeather.Date
def model_fm_5(processed, store_key):
    sales = processed["sales"][
        processed["sales"]["StoreKey"] == store_key
    ]

    store = processed["store"].merge(
        processed["geography"],
        on="GeographyKey",
        how="left"
    )

    country = store.loc[
        store["StoreKey"] == store_key,
        "RegionCountryName"
    ].iloc[0]

    weather = processed["weather"][
        processed["weather"]["Country"] == country
    ]

    return sales.merge(
        weather,
        left_on="DateKey",
        right_on="Date",
        how="left",
        suffixes=("", "_weather")
    )