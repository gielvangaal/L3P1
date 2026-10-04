import matplotlib.pyplot as plt

from src.measures import total_revenue, total_cost, profit


# US-CEO-1
# Totale omzet, totale kosten en winst
def visual_ceo_1(df):
    labels = ["Omzet", "Kosten", "Winst"]

    values = [
        total_revenue(df),
        total_cost(df),
        profit(df)
    ]

    plt.bar(labels, values)

    plt.title("Financiële prestaties Contoso")
    plt.ylabel("Bedrag")

    plt.show()