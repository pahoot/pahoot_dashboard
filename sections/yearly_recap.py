import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

mesos = ["Gener", "Febrer", "Març", "Abril", "Maig", "Juny", "Juliol", "Agost", "Setembre", "Octubre", "Novembre", "Desembre"]

def show_yearly_recap(df_all : pd.DataFrame):

    st.markdown("## 📆 Yearly Recap")

    # Year selection dropdown
    year_selected = st.selectbox("Select a Year:", sorted(df_all["Year"].unique()), index=len(df_all["Year"].unique())-1)

    # Filter data to selected year (excluding invitees)
    df_year = df_all[(df_all["Year"] == year_selected) & (~df_all["Person_id"].str.endswith("c"))]

    # --------------------------------------
    st.subheader(f"🎯 Gaioles per persona {year_selected}")

    # Count total events per person
    person_counts = df_year["pseudonim"].value_counts().reset_index()
    person_counts.columns = ["pseudonim", "Total Events"]

    # Tile plot
    fig = px.treemap(person_counts, path=["pseudonim"], values="Total Events", title=f"Total Events per Person ({year_selected})", color="Total Events")
    st.plotly_chart(fig)

    # --------------------------------------

    st.subheader(f"📈 Gaioles mensuals per persona {year_selected}")

    # Count events per person per month
    df_year["Month"] = df_year["Day"].dt.month
    monthly_counts = df_year.groupby(["Month", "pseudonim"]).size().reset_index(name="Total Events")

    # Line plot with multiple persons
    fig = px.line(
        monthly_counts, 
        x="Month", 
        y="Total Events", 
        color="pseudonim",
        markers=True
    )

    # Relabel the x-axis
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1, 13)),  # Month numbers (1-12)
        ticktext=mesos
    )

    st.plotly_chart(fig)

    # --------------------------------------

    st.subheader(f"📅 Distribució de gaioles per dia de la setmana {year_selected}")    

    # Count events per weekday per person
    weekday_counts = df_year.groupby(["Weekday", "pseudonim"]).size().reset_index(name="Total Events")

    # Convert to percentage per person
    weekday_counts["Percentage"] = weekday_counts.groupby("pseudonim")["Total Events"].transform(lambda x: (x / x.sum()) * 100)

    # Define correct weekday order in Catalan
    weekday_order = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"]
    weekday_counts["Weekday"] = pd.Categorical(weekday_counts["Weekday"], categories=weekday_order, ordered=True)

    # Grouped bar chart (percentages)
    fig = px.bar(
        weekday_counts, 
        x="Weekday", 
        y="Percentage", 
        color="pseudonim",
        barmode="group",
        category_orders={"Weekday": weekday_order}  # ⬅️ Forces correct order
    )

    st.plotly_chart(fig)

    # --------------------------------------

    st.subheader(f"🔥 Heatmap de gaioles setmanals {year_selected}")

    # Extract week numbers from the date
    df_year["Week"] = df_year["Day"].dt.strftime("%U").astype(int)  # %U gives week number (0-53)

    # Count events per (week, person)
    weekly_counts = df_year.groupby(["Week", "pseudonim"]).size().reset_index(name="Total Events")

    # Pivot the data for heatmap format (weeks as rows, persons as columns)
    heatmap_data = weekly_counts.pivot(index="Week", columns="pseudonim", values="Total Events").fillna(0)

    # Create the heatmap
    fig = px.imshow(
        heatmap_data.T,  # Transpose so persons are columns
        labels=dict(x="Week", y="Person", color="Events"),
        color_continuous_scale="Oranges",  # Heatmap color
        aspect="auto"
    )

    # Customize x-axis to show week numbers clearly
    fig.update_xaxes(title="Week of the Year", tickmode="linear")

    # Show plot
    st.plotly_chart(fig)

