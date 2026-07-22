import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
@st.cache_data
def load_data():
    return pd.read_csv("novamart_clean.csv")

df = load_data()
st.title("NovaMart Dashboard - Ayas nk")
df["Discount Band"] = pd.cut(
    df["discount"],
    bins=[-1,0,0.15,0.30,1],
    labels=[
        "No Discount",
        "1-15%",
        "16-30%",
        "30%+"
    ]
)
category = st.sidebar.multiselect(
    "Category_y",
    options=sorted(df["category_y"].dropna().unique()),
    default=sorted(df["category_y"].dropna().unique())
)

discount_band = st.sidebar.multiselect(
    "Discount Band",
    options=sorted(df["Discount Band"].dropna().unique()),
    default=sorted(df["Discount Band"].dropna().unique())
)

minimum_profit = st.sidebar.slider(
    "Minimum Profit",
    int(df["profit"].min()),
    int(df["profit"].max()),
    int(df["profit"].min())
)
filtered_df = df.copy()

if category:
    filtered_df = filtered_df[
        filtered_df["category_y"].isin(category)
    ]

if discount_band:
    filtered_df = filtered_df[
        filtered_df["Discount Band"].isin(discount_band)
    ]

filtered_df = filtered_df[
    filtered_df["profit"] >= minimum_profit
]
total_profit = filtered_df["profit"].sum()

avg_margin = filtered_df["profit_margin_pct"].mean()

loss_orders = len(
    filtered_df[filtered_df["profit"] < 0]
)
fig = px.scatter(
    filtered_df,
    x="sales",
    y="profit",
    color="category_y"
)

st.plotly_chart(fig)
margin = filtered_df.groupby(
    "Discount Band"
)["profit_margin_pct"].mean()

st.bar_chart(margin)
fig = px.pie(
    filtered_df,
    names="category_y",
    values="profit",
    hole=0.5
)

st.plotly_chart(fig)
st.download_button(
    "Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_data.csv",
    "text/csv"
)