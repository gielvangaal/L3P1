# DIM DATE
def validate_dim_date(df):
    assert df["Date"].notna().all()
    assert df["Date"].is_unique

# DIM CHANNEL
def validate_dim_channel(df):
    assert df["Channel"].notna().all()
    assert df["Channel"].is_unique

# FACT WEATHER
def validate_fact_weather(df):
    assert df["Date"].notna().all()
    assert df["Country"].notna().all()


# DIM GEOGRAPHY
def validate_dim_geography(df):
    assert df["GeographyKey"].notna().all()
    assert df["GeographyKey"].is_unique


# DIM PRODUCT
def validate_dim_product(df):
    assert df["ProductKey"].notna().all()
    assert df["ProductKey"].is_unique


# DIM PRODUCT CATEGORY
def validate_dim_product_category(df):
    assert df["ProductCategoryKey"].notna().all()
    assert df["ProductCategoryKey"].is_unique


# DIM PRODUCT SUBCATEGORY
def validate_dim_product_subcategory(df):
    assert df["ProductSubcategoryKey"].notna().all()
    assert df["ProductSubcategoryKey"].is_unique


# DIM PROMOTION
def validate_dim_promotion(df):
    assert df["PromotionKey"].notna().all()
    assert df["PromotionKey"].is_unique


# FACT SALES
def validate_fact_sales(df):
    assert df["SalesKey"].notna().all()
    assert df["SalesKey"].is_unique


# DIM STORE
def validate_dim_store(df):
    assert df["StoreKey"].notna().all()
    assert df["StoreKey"].is_unique


# DIM COUNTRY
def validate_dim_country(df):
    assert df["Country"].notna().all()
    assert df["Country"].is_unique
    assert df["CountryISO3"].notna().all()
    assert df["CountryISO3"].is_unique
    assert df["CountryISO3"].str.fullmatch(r"[A-Z]{3}").all()


# GEOJSON
def validate_geojson(data):
    assert data["type"] == "FeatureCollection"
    assert isinstance(data["features"], list)