import matplotlib.pyplot as plt # US-CEO-1
import plotly.graph_objects as go # US-CEO-2, 3
import folium # US-CEO-4
import math # US-CEO-4
import altair as alt # US-CEO-5
import seaborn as sns # US-FM-1

from src.measures import total_revenue, total_cost, profit # US-CEO-1, 2, 3
from shapely.geometry import shape # US-CEO-4
from branca.element import Element # US-CEO-4


# subplots() maakt object aan van fig en ax;
# ax bevat de grafiek, fig het canvas
# objecten worden doorgegeven aan show(), die rendert het geheel.


# US-CEO-1
def visual_ceo_1(df):
    labels = ["Total Revenue", "Total Cost", "Profit"]

    values = [
        total_revenue(df) / 1_000_000_000,
        total_cost(df) / 1_000_000_000,
        profit(df) / 1_000_000_000
    ]

    fig, ax = plt.subplots()

    ax.bar(x=labels, height=values)

    fig.suptitle(t="Financial Performance Contoso", fontsize=14)
    ax.set_title(label="US-CEO-1", fontsize=9)
    ax.set_ylabel(ylabel="Amount ($bn)")

    return fig


# US-CEO-2
def visual_ceo_2(df):
    data = df.copy()

    data["Quarter"] = (data["MonthOfYear"] - 1) // 3 + 1

    yearly = (
        data.groupby(by="Year")["SalesAmount"]
        .sum()
        .reset_index()
    )

    quarterly = (
        data.groupby(by=["Year", "Quarter"])["SalesAmount"]
        .sum()
        .reset_index()
    )

    monthly = (
        data.groupby(by=["Year", "MonthOfYear"])["SalesAmount"]
        .sum()
        .reset_index()
    )

    fig = go.Figure()

    # Jaar
    fig.add_trace(go.Scatter(
        x=yearly["Year"].astype(str),
        y=yearly["SalesAmount"] / 1_000_000_000,
        mode="lines+markers",
        name="Year"
    ))

    # Kwartaal
    fig.add_trace(go.Scatter(
        x=quarterly["Year"].astype(str) + " Q" + quarterly["Quarter"].astype(str),
        y=quarterly["SalesAmount"] / 1_000_000_000,
        mode="lines+markers",
        name="Quarter",
        visible=False
    ))

    # Maand
    fig.add_trace(go.Scatter(
        x=monthly["Year"].astype(str) + "-" + monthly["MonthOfYear"].astype(str).str.zfill(2),
        y=monthly["SalesAmount"] / 1_000_000_000,
        mode="lines+markers",
        name="Month",
        visible=False
    ))

    fig.update_layout(
        title={
            "text": "Revenue over Time<br><sup>US-CEO-2</sup>"
        },
        xaxis_title="Period",
        yaxis_title="Revenue ($bn)",
        template="plotly_white",
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": "Year",
                        "method": "update",
                        "args": [{"visible": [True, False, False]}]
                    },
                    {
                        "label": "Quarter",
                        "method": "update",
                        "args": [{"visible": [False, True, False]}]
                    },
                    {
                        "label": "Month",
                        "method": "update",
                        "args": [{"visible": [False, False, True]}]
                    }
                ],
                "direction": "down",
                "showactive": True
            }
        ]
    )

    return fig

# US-CEO-3
def visual_ceo_3(df):
    revenue_by_channel = (
        df.groupby("ChannelName")["SalesAmount"].sum()
    )

    fig, ax = plt.subplots()

    ax.pie(
        x=revenue_by_channel,
        labels=revenue_by_channel.index,
        autopct="%1.2f%%",
        startangle=90,
        pctdistance=1.15,
        labeldistance=1.35,
        colors=["#1D267D", "#344C9C", "#527FE8", "#85A9F4"],
        wedgeprops={"width": 0.35}
    )

    ax.text(
        x=0,
        y=0,
        s=f"${total_revenue(df) / 1_000_000_000:.1f}bn",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold"
    )

    fig.suptitle(t="Revenue by Sales Channel", fontsize=14)
    ax.set_title(label="US-CEO-3", fontsize=9)

    return fig


# US-CEO-4
def visual_ceo_4(df, geojson):
    revenue_by_country = (
        df.groupby(
            by=["CountryISO3", "RegionCountryName"],
            as_index=False
        )["SalesAmount"].sum()
    )

    # Punt binnen landgrenzen opslaan onder de ISO3-landcode.
    coordinates = {}

    for feature in geojson["features"]:
        iso3 = feature["properties"]["ISO3166-1-Alpha-3"]
        point = shape(feature["geometry"]).representative_point()

        coordinates[iso3] = (point.y, point.x)

    # Map initialiseren
    map_ceo_4 = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles="OpenStreetMap"
    )

    # Bolletjes tekenen op basis van omzet
    max_revenue = revenue_by_country["SalesAmount"].max()

    for _, row in revenue_by_country.iterrows():
        iso3 = row["CountryISO3"]

        if iso3 not in coordinates:
            print(f"Geen coördinaten voor: {iso3}")
            continue

        latitude, longitude = coordinates[iso3]
        revenue = row["SalesAmount"]

        radius = 4 + 20 * math.sqrt(revenue / max_revenue)

        folium.CircleMarker(
            location=[latitude, longitude],
            radius=radius,
            color="#527FE8",
            fill=True,
            fill_color="#527FE8",
            fill_opacity=0.7,
            popup=folium.Popup(
                html=(
                    f"<b>{row['RegionCountryName']}</b><br>"
                    f"Revenue: ${revenue / 1_000_000:,.2f}M"
                ),
                max_width=250
            ),
            tooltip=row["RegionCountryName"]
        ).add_to(map_ceo_4)

    # Header en legenda
    header = """
    <div style="
        position: fixed;
        top: 20px;
        left: 60px;
        z-index: 1000;
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 6px #999;
        font-family: Arial;
    ">
        <b>Revenue by Country</b><br>
        <small>US-CEO-4</small>
        <hr>
        <span style="color: #527FE8;">●</span>
        Bubble size = Total Revenue
    </div>
    """

    map_ceo_4.get_root().html.add_child(
        Element(header)
    )

    return map_ceo_4


# US-CEO-5
def visual_ceo_5(df):
    monthly = (
        df.groupby(
            by="MonthOfYear",
            as_index=False
        )
        .agg({
            "SalesAmount": "sum",
            "EstimatedDailyTemperature": "mean"
        })
    )

    monthly["RevenueBn"] = monthly["SalesAmount"] / 1_000_000_000

    monthly["Month"] = monthly["MonthOfYear"].map({
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    })

    # Omzet per maand
    bars = alt.Chart(data=monthly).mark_bar(
        color="#527FE8"
    ).encode(
        x=alt.X(
            shorthand="Month:N",
            sort=list(monthly["Month"])
        ),
        y=alt.Y(
            shorthand="RevenueBn:Q",
            title="Revenue ($bn)"
        ),
        tooltip=[
            alt.Tooltip("Month:N", title="Month"),
            alt.Tooltip("RevenueBn:Q", title="Revenue ($bn)", format=".2f")
        ]
    )

    # Gemiddelde temperatuur per maand
    line = alt.Chart(data=monthly).mark_line(
        color="#D94F4F",
        point=True,
        strokeWidth=3
    ).encode(
        x=alt.X(
            shorthand="Month:N",
            sort=list(monthly["Month"])
        ),
        y=alt.Y(
            shorthand="EstimatedDailyTemperature:Q",
            title="Temperature (°C)"
        ),
        tooltip=[
            alt.Tooltip("Month:N", title="Month"),
            alt.Tooltip(
                "EstimatedDailyTemperature:Q",
                title="Temperature (°C)",
                format=".1f"
            )
        ]
    )

    chart = alt.layer(
        bars,
        line
    ).resolve_scale(
        y="independent"
    ).properties(
        width=900,
        height=400,
        title={
            "text": "Revenue vs Average Temperature",
            "subtitle": "US-CEO-5"
        }
    ).interactive()

    return chart


# US-FM-1
def visual_fm_1(df, store_key=1):
    store = df.loc[df["StoreKey"] == store_key].copy()

    store["Year"] = store["DateKey"].dt.year

    yearly = (
        store.groupby(by="Year", as_index=False)["SalesAmount"]
        .sum()
    )

    yearly["SalesTarget"] = yearly["SalesAmount"] * 1.10

    yearly = yearly.melt(
        id_vars="Year",
        value_vars=["SalesAmount", "SalesTarget"],
        var_name="Metric",
        value_name="Amount"
    )

    yearly["Amount"] = yearly["Amount"] / 1_000_000

    fig, ax = plt.subplots()

    sns.barplot(
        data=yearly,
        x="Year",
        y="Amount",
        hue="Metric",
        palette={
            "SalesAmount": "#527FE8",
            "SalesTarget": "#344C9C"
        },
        ax=ax
    )

    fig.suptitle(t="Revenue vs Target by Year", fontsize=14)
    ax.set_title(label="US-FM-1", fontsize=9)
    ax.set_xlabel(xlabel="Year")
    ax.set_ylabel(ylabel="Amount ($M)")
    ax.legend(title=None)

    return fig


# US-FM-2
def visual_fm_2(df):
    data = df.copy()

    data["Quarter"] = (data["MonthOfYear"] - 1) // 3 + 1

    yearly = (
        data.groupby(by="Year")["SalesAmount"]
        .sum()
        .reset_index()
    )

    quarterly = (
        data.groupby(by=["Year", "Quarter"])["SalesAmount"]
        .sum()
        .reset_index()
    )

    monthly = (
        data.groupby(by=["Year", "MonthOfYear"])["SalesAmount"]
        .sum()
        .reset_index()
    )

    fig = go.Figure()

    # Jaar
    fig.add_trace(go.Scatter(
        x=yearly["Year"].astype(str),
        y=yearly["SalesAmount"] / 1_000_000,
        mode="lines+markers",
        name="Year"
    ))

    # Kwartaal
    fig.add_trace(go.Scatter(
        x=quarterly["Year"].astype(str) + " Q" + quarterly["Quarter"].astype(str),
        y=quarterly["SalesAmount"] / 1_000_000,
        mode="lines+markers",
        name="Quarter",
        visible=False
    ))

    # Maand
    fig.add_trace(go.Scatter(
        x=monthly["Year"].astype(str) + "-" + monthly["MonthOfYear"].astype(str).str.zfill(2),
        y=monthly["SalesAmount"] / 1_000_000,
        mode="lines+markers",
        name="Month",
        visible=False
    ))

    fig.update_layout(
        title={
            "text": "Store Revenue over Time<br><sup>US-FM-2</sup>"
        },
        xaxis_title="Period",
        yaxis_title="Revenue ($M)",
        template="plotly_white",
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": "Year",
                        "method": "update",
                        "args": [{"visible": [True, False, False]}]
                    },
                    {
                        "label": "Quarter",
                        "method": "update",
                        "args": [{"visible": [False, True, False]}]
                    },
                    {
                        "label": "Month",
                        "method": "update",
                        "args": [{"visible": [False, False, True]}]
                    }
                ],
                "direction": "down",
                "showactive": True
            }
        ]
    )

    return fig