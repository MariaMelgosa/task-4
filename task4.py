import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Task 4: María Melgosa")

df = pd.read_csv("airbnb.csv")

df_cleaned = df.drop(columns=["license;;"], errors="ignore")
df_cleaned["number_of_reviews"] = df_cleaned["number_of_reviews"].fillna(0)
df_cleaned["room_type"] = df_cleaned["room_type"].fillna("Unknown")
df_cleaned = df_cleaned.dropna(subset=["price"])

st.sidebar.header("Filters")
neighbourhood_group = st.sidebar.multiselect("Select one neighbourhood", df_cleaned["neighbourhood_group"].unique())
neighbourhood = st.sidebar.multiselect("Select one or multi neighbourhood", df_cleaned["neighbourhood"].unique())
room_type = st.sidebar.multiselect("Select one or multi room_type", df_cleaned["room_type"].unique())

df_filtered = df_cleaned[
                (df_cleaned["neighbourhood_group"].isin(neighbourhood_group))&
                (df_cleaned["neighbourhood"].isin(neighbourhood))&
                (df_cleaned["room_type"].isin(room_type))
                ]

section = st.sidebar.selectbox("Choose Section", ["Listings Analysis", "Host Analysis"])

if section == "Listings Analysis":
    st.subheader("Listings Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Map")
        st.map(df_filtered.dropna(subset=["latitude", "longitude"]), latitude="latitude", longitude="longitude")

    with col2: 
        st.subheader("Boxplot - Price Distribution")
        fig_boxplot_neighbourhood = px.box(df_filtered, x="neighbourhood", y="price")
        st.plotly_chart(fig_boxplot_neighbourhood, key="Boxplot 2")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Availability by Room Type")
        fig_availability = px.box(df_filtered, x="room_type", y="availability_365")
        st.plotly_chart(fig_availability)

    with col2:
        st.subheader("Average Price")
        df_avg = df_filtered.groupby("room_type")["price"].mean().reset_index()
        fig_avg = px.bar(df_avg, x="room_type", y="price", color="room_type")
        st.plotly_chart(fig_avg)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Most Reviews in a Month")
        df_reviews = df_filtered.sort_values(by="reviews_per_month", ascending=False).head(10)
        fig_reviews = px.bar(df_reviews, x="reviews_per_month", y="name", orientation="h", color="neighbourhood_group")
        st.plotly_chart(fig_reviews)

    with col2:
        st.subheader("Price vs Reviews")
        fig_relation = px.scatter(df_filtered, x="price", y="number_of_reviews", color="neighbourhood_group")
        st.plotly_chart(fig_relation)

elif section == "Host Analysis":
    st.subheader("Host Analysis")

    st.subheader("Top 10 Hosts")
    df_host = df_filtered.groupby(["host_id", "host_name"]).size().reset_index()
    df_host["host"] = df_host["host_id"].astype(str) + "---" + df_host["host_name"]
    df_top10_host = df_host.sort_values(by=0, ascending=False).head(10)
    fig = px.bar(df_top10_host, x=0, y="host", orientation="h", hover_name="host_name")
    st.plotly_chart(fig)


st.sidebar.subheader("Simulator")
simulator_neighbourhood = st.sidebar.selectbox("Select a neighbourhood", df_cleaned["neighbourhood"].unique())
simulator_type = st.sidebar.selectbox("Select room type", df_cleaned["room_type"].unique())

df_simulator = df_cleaned[
    (df_cleaned["neighbourhood"] == simulator_neighbourhood) & 
    (df_cleaned["room_type"] == simulator_type)
]

if not df_simulator.empty:
    min_price = df_simulator["price"].min()
    max_price = df_simulator["price"].max()
    avg_price = df_simulator["price"].mean()

    st.sidebar.write("Price recommendation")
    st.sidebar.metric(label="Minimum Price", value=f"€{min_price}")
    st.sidebar.metric(label="Maximum Price", value=f"€{max_price}")
    st.sidebar.metric(label="Average Price", value=f"€{avg_price}")
