# Total Revenue
def total_revenue(df):
    return df["SalesAmount"].sum()


# Total Cost
def total_cost(df):
    return df["TotalCost"].sum()


# Profit
def profit(df):
    return total_revenue(df) - total_cost(df)


# Sales Target
def sales_target(df):
    return total_revenue(df) * 1.10


# Sales Quantity
def sales_quantity(df):
    return df["SalesQuantity"].sum()


# Returned Quantity
def returned_quantity(df):
    return df["ReturnQuantity"].sum()


# Average Temperature
def average_temperature(df):
    return df["EstimatedDailyTemperature"].mean()