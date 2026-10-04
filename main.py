from src.config import FILES
from src.extract import *
from src.transform import *
from src.validate import *
from src.load import *
from src.model import *
from src.visuals import *


# ------------------------------------------------------------
# 1. Brontabellen inlezen, transformeren, valideren en opslaan
# ------------------------------------------------------------

datasets = [
    ("calendar", extract_csv, transform_dim_date, validate_dim_date),
    ("channel", extract_csv, transform_dim_channel, validate_dim_channel),
    ("weather", extract_excel, transform_fact_weather, validate_fact_weather),
    ("geography", extract_csv, transform_dim_geography, validate_dim_geography),
    ("product", extract_csv, transform_dim_product, validate_dim_product),
    ("product_category", extract_csv, transform_dim_product_category, validate_dim_product_category),
    ("product_sub_category", extract_csv, transform_dim_product_subcategory, validate_dim_product_subcategory),
    ("promotion", extract_csv, transform_dim_promotion, validate_dim_promotion),
    ("sales", extract_csv, transform_fact_sales, validate_fact_sales),
    ("store", extract_csv, transform_dim_store, validate_dim_store),
]

processed = {}

for name, extract, transform, validate in datasets:
    # Extract
    df = extract(FILES[name]["raw"])

    # Transform
    df = transform(df)

    # Validate
    validate(df)

    # Bewaren voor gebruik in model.py
    processed[name] = df

    # Load naar data/processed
    load_csv(
        df,
        FILES[name]["processed"]
    )

    print(f"{name} succesvol verwerkt.")


# ------------------------------------------------------------
# 2. DimCountry opbouwen
# Koppeltabel tussen Geography en Weather
# ------------------------------------------------------------

dim_country = transform_dim_country(
    processed["geography"],
    processed["weather"]
)

validate_dim_country(dim_country)

load_csv(
    dim_country,
    FILES["country"]["processed"]
)

# Ook beschikbaar maken voor later gebruik
processed["country"] = dim_country

print("country succesvol verwerkt.")


# ------------------------------------------------------------
# 3. Modellen per user story opbouwen
# model.py bevat alleen de benodigde relaties / merges
# ------------------------------------------------------------

# CEO
ceo_1 = model_ceo_1(processed)
ceo_2 = model_ceo_2(processed)
ceo_3 = model_ceo_3(processed)
ceo_4 = model_ceo_4(processed)
ceo_5 = model_ceo_5(processed)

# Filiaalmanager
# StoreKey 1 wordt voorlopig gebruikt als testfiliaal
fm_1 = model_fm_1(processed)
fm_2 = model_fm_2(processed, 1)
fm_3 = model_fm_3(processed, 1)
fm_4 = model_fm_4(processed)
fm_5 = model_fm_5(processed, 1)

print("Modellen succesvol opgebouwd.")

# VISUALSSSS
visual_ceo_1(ceo_1)