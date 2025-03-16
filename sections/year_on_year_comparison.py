import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


#region Year-over-Year Comparison

def show_yoy_comparison(df_all):

    df_all = df_all[~df_all["Person_id"].str.len().eq(4)] # Filtrar invitats

    st.subheader("📊 Year-on-Year Comparison - Individual Evolution")

    # User selects participants
    participants = st.multiselect("Select Participants:", df_all["pseudonim"].unique(), default=df_all["pseudonim"].unique())

    # Aggregation choice (Half-Year, Yearly, etc.)
    aggregation = st.selectbox("Select Aggregation Level:", ["Half-Year", "Yearly"])

    # Extract Year and aggregation period
    df_all["Year"] = df_all["Day"].dt.year

    if aggregation == "Half-Year":
        df_all["Period"] = df_all["Day"].dt.month.map(lambda x: "First Half" if x <= 6 else "Second Half")
    elif aggregation == "Yearly":
        df_all["Period"] = df_all["Year"]

    # Filter dataset by selected participants
    df_comparison = df_all[df_all["pseudonim"].isin(participants)]
    df_comparison = df_comparison.groupby(["Year", "Period", "pseudonim"]).size().reset_index(name="Total Events")

    # Create the connected dot plot
    fig = px.line(
        df_comparison, 
        x="Year", 
        y="Total Events", 
        color="pseudonim",
        facet_col="pseudonim",  # Creates separate subplots per person
        markers=True,  # Adds dots at each point
        title="📊 Yearly Event Evolution per Person",
        height=600
    )

    # Improve layout
    fig.update_traces(marker=dict(size=10))  # Bigger dots
    fig.update_layout(showlegend=False)  # Hide legend since each person has their own plot

    st.plotly_chart(fig)

