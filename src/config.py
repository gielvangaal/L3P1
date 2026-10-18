RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

# f"" = f-string = template literals = variabelen in de string zetten

FILES = {
    "calendar": {
        "raw": f"{RAW_DIR}/Contoso_Calendar.csv",
        "processed": f"{PROCESSED_DIR}/dim_date.csv",
    },
    "channel": {
        "raw": f"{RAW_DIR}/Contoso_Channel.csv",
        "processed": f"{PROCESSED_DIR}/dim_channel.csv",
    },
    "weather": {
        "raw": f"{RAW_DIR}/Contoso_Daily_Weather_2011_2013_NIJE3.xlsx",
        "processed": f"{PROCESSED_DIR}/fact_weather.csv",
    },
    "geography": {
        "raw": f"{RAW_DIR}/Contoso_Geography.csv",
        "processed": f"{PROCESSED_DIR}/dim_geography.csv",
    },
    "product": {
        "raw": f"{RAW_DIR}/Contoso_Product.csv",
        "processed": f"{PROCESSED_DIR}/dim_product.csv",
    },
    "product_category": {
        "raw": f"{RAW_DIR}/Contoso_Product_Category.csv",
        "processed": f"{PROCESSED_DIR}/dim_product_category.csv",
    },
    "product_sub_category": {
        "raw": f"{RAW_DIR}/Contoso_ProductSubcategory.csv",
        "processed": f"{PROCESSED_DIR}/dim_product_sub_category.csv",
    },
    "promotion": {
        "raw": f"{RAW_DIR}/Contoso_Promotion.csv",
        "processed": f"{PROCESSED_DIR}/dim_promotion.csv",
    },
    "sales": {
        "raw": f"{RAW_DIR}/Contoso_Sales.csv",
        "processed": f"{PROCESSED_DIR}/fact_sales.csv",
    },
    "store": {
        "raw": f"{RAW_DIR}/Contoso_Stores.csv",
        "processed": f"{PROCESSED_DIR}/dim_store.csv",
    },
    "country": {
        "processed": f"{PROCESSED_DIR}/dim_country.csv",
    },
    "countries_geojson": {
        "raw": f"{RAW_DIR}/countries.geojson",
        "processed": f"{PROCESSED_DIR}/countries.geojson",
    },
}