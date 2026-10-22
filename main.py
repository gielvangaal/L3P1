from src.config import FILES
from src.extract import *
from src.transform import *
from src.validate import *
from src.load import *
from src.model import *
from src.visuals import *
from src.export import *

print("\n#################################################################")
print ("Start pipeline: van ruwe data naar inzicht")
print("#################################################################")

# ------------------------------------------------------------
# 1.1) ETL: Brontabellen inlezen, transformeren, valideren en opslaan
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
    ("countries_geojson", extract_geojson, transform_geojson, validate_geojson),
]

processed = {}

print ("\n1.1) Start ETL: brontabellen inlezen, transformeren, valideren en opslaan")

for name, extract, transform, validate in datasets:

    # Extract
    data = extract(path=FILES[name]["raw"])

    # Transform
    data = transform(data)

    # Validate
    validate(data)

    # Beschikbaar maken voor model.py
    processed[name] = data

    # Opslaan als CSV of GeoJSON
    load = load_geojson if name == "countries_geojson" else load_csv

    load(
        data=data,
        path=FILES[name]["processed"]
    )

    print(f"-> {name} succesvol verwerkt")


# ------------------------------------------------------------
# 1.2) DimCountry opbouwen
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

print("-> country succesvol verwerkt.")

print("\n-> ETL succesvol afgerond.")

# ------------------------------------------------------------
# 2) Modellen per user story opbouwen
# model.py bevat alleen de benodigde relaties / merges
# ------------------------------------------------------------

print ("\n2. Modellen per user story opbouwen")

# CEO
ceo_1 = model_ceo_1(processed=processed)
ceo_2 = model_ceo_2(processed=processed)
ceo_3 = model_ceo_3(processed=processed)
ceo_4 = model_ceo_4(processed=processed)
ceo_5 = model_ceo_5(processed=processed)

# Filiaalmanager
# StoreKey 1 wordt voorlopig gebruikt als testfiliaal
fm_1 = model_fm_1(processed=processed)
fm_2 = model_fm_2(processed=processed, store_key=1)
fm_3 = model_fm_3(processed=processed, store_key=1)
fm_4 = model_fm_4(processed=processed, store_key=1)
fm_5 = model_fm_5(processed=processed, store_key=1)

print("-> modellen succesvol opgebouwd.")

# ------------------------------------------------------------
# 3) Visualisaties genereren en exporteren
# ------------------------------------------------------------

print ("\n3) Visualisaties genereren en exporteren")

# US-CEO-1
export_matplotlib(
    fig=visual_ceo_1(df=ceo_1),
    filename="US-CEO-1.png"
)

# US-CEO-2
export_plotly(
    fig=visual_ceo_2(df=ceo_2),
    filename="US-CEO-2.html"
)

# US-CEO-3
export_matplotlib(
    fig=visual_ceo_3(df=ceo_3),
    filename="US-CEO-3.png"
)

# US-CEO-4
export_folium(
    map_object=visual_ceo_4(
        df=ceo_4,
        geojson=processed["countries_geojson"]
    ),
    filename="US-CEO-4.html"
)

# US-CEO-5
export_altair(
    chart=visual_ceo_5(df=ceo_5),
    filename="US-CEO-5.html"
)

# US-FM-1
export_matplotlib(
    fig=visual_fm_1(df=fm_1, store_key=1),
    filename="US-FM-1.png"
)

# US-FM-2
export_plotly(
    fig=visual_fm_2(df=fm_2),
    filename="US-FM-2.html"
)

# US-FM-3
export_matplotlib(
    fig=visual_fm_3(df=fm_3),
    filename="US-FM-3.png"
)

# US-FM-4
export_altair(
    chart=visual_fm_4(df=fm_4),
    filename="US-FM-4.html"
)

export_plotly(
    fig=visual_fm_5(df=fm_5),
    filename="US-FM-5.html"
)

print("-> visualisaties succesvol geëxporteerd.\n")

print("#################################################################")
print("De pipeline heeft succesvol gedraaid.")
print("-> alle output is te vinden in /l3p1/output/")
print("#################################################################")