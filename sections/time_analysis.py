import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def show_time_analysis(df):
    df_2025 = df[df["Year"] == 2025]  # Filter only 2025 data

    st.markdown("## ⏳ Time Period Analysis (2025 Only)")

    # 🔥 Activity Heatmap
    st.subheader("🔥 Activity Heatmap (Time Period vs. Weekday)")

    # Prepare heatmap data
    heatmap_data = df_2025.groupby(["Weekday", "Time_period"]).size().unstack().fillna(0)
    heatmap_data = heatmap_data.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(heatmap_data, cmap="Blues", linewidths=0.5, annot=True, fmt=".0f", ax=ax)
    ax.set_title("Event Frequency by Time Period & Weekday")

    st.pyplot(fig)

    # ⏳ Hexagon Plot (Radar Chart)
    st.subheader("⏳ Timeframe Distribution (Hexagon Plot)")

    # Ensure all time slots are represented
    time_slots = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24"]
    time_counts = df_2025["Time_period"].value_counts().reindex(time_slots, fill_value=0)

    # Radar plot
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=time_counts.values,
        theta=time_counts.index,
        fill='toself',
        name='Overall Activity',
        line=dict(color="blue")  # Ensure it's visible
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(time_counts.values) + 1])),
        showlegend=False,
        title="Time Period Presence"
    )

    st.plotly_chart(fig)

    