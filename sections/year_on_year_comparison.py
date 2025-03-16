import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import streamlit as st
import pandas as pd
import plotly.express as px

def show_yoy_comparison(df_all):
    st.markdown("## 📊 Year-over-Year Comparison")
    df_all = df_all[~df_all["Person_id"].str.len().eq(4)]  # Exclude invitees

    st.subheader("📊 Year-on-Year Comparison - Individual Evolution")

    # User selects participants
    participants = st.multiselect("Select Participants:", df_all["Person_id"].unique(), default=df_all["Person_id"].unique())

    # Aggregation choice (Half-Year, Monthly, Yearly)
    aggregation = st.selectbox("Select Aggregation Level:", ["Monthly", "Half-Year", "Yearly"])

    # Extract Year
    df_all["Year"] = df_all["Day"].dt.year

    # Define period type and number of iterations
    if aggregation == "Half-Year":
        df_all["Period"] = df_all["Day"].dt.month.map(lambda x: "First Half" if x <= 6 else "Second Half")
        periods = ["First Half", "Second Half"]
    elif aggregation == "Monthly":
        catalan_months = {1: "Gener", 2: "Febrer", 3: "Març", 4: "Abril", 5: "Maig", 6: "Juny",
                          7: "Juliol", 8: "Agost", 9: "Setembre", 10: "Octubre", 11: "Novembre", 12: "Desembre"}
        df_all["Period"] = df_all["Day"].dt.month.map(catalan_months)
        periods = list(catalan_months.values())  # Ordered month names
    elif aggregation == "Yearly":
        present_year = pd.Timestamp.today().year  # Get the current year
        df_all["Period"] = df_all["Year"].apply(lambda year: "years" if year != present_year else "exclude")
        periods = ["years"]  # Define only the relevant period

    # Filter dataset by selected participants
    df_comparison = df_all[df_all["Person_id"].isin(participants)]
    df_comparison = df_comparison.groupby(["Year", "Period", "Person_id"]).size().reset_index(name="Total Events")

    # Create separate plots per period
    for period in periods:
        df_period = df_comparison[df_comparison["Period"] == period]

        if df_period.empty:
            continue  # Skip empty plots

        fig = px.line(
            df_period, 
            x="Year", 
            y="Total Events", 
            color="Person_id",
            facet_col="Person_id",
            markers=True,  # Adds dots at each point
            title=f"📊 Evolution for {period}",  # Dynamic title per period
            height=500
        )

        fig.update_layout(
            annotations=[
                a.update(text=a.text.split("=")[-1]) for a in fig.layout.annotations
            ]
        )
        fig.update_xaxes(type="category")

        fig.update_traces(marker=dict(size=10))  # Bigger dots
        st.plotly_chart(fig)
