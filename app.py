import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime


# Internal imports
from sections import *
import src.database as db
import src.analysis as analysis

st.set_page_config(page_title="Pahoot Dashboard", layout="wide")

# Load data
df = db.fetch_data()
streaks = analysis.calculate_streaks(df)

df_2025 = df[df["Year"] == 2025]  # Only 2025 for time-based plots
df_all = df  # All years for general plots

# Dashboard Title
st.title("📊 Pahoot: Event Dashboard")

# KPI Metrics
col1, col2 = st.columns(2)
col1.metric(label="Total Events", value=len(df))
# Count number of days from 1-1-2023
col2.metric(label="Total recording days", value=(datetime.today() - datetime(2023,1,1)).days)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["General Overview", "Yearly Recap", "Year-over-Year Comparison", "Streak analisis", "Time Analysis"])

# if page == "General Overview":
#     show_general_overview(df_all)

if page == "Yearly Recap":
    st.markdown("---")
    st.markdown("## 📆 Yearly Recap")
    show_yearly_recap(df_all)

elif page == "Year-over-Year Comparison":
    st.markdown("---")
    st.markdown("## 📊 Year-over-Year Comparison")
    show_yoy_comparison(df_all)

elif page == "Streak analisis":
    st.markdown("---")
    st.markdown("## 📈 Streak analysis")
    streak_analysis_fun(df_all)

# elif page == "Time Analysis":
#     show_time_analysis(df_all)


# st.sidebar.title("Filters")
# selected_person = st.sidebar.selectbox("Select Person", ["All"] + list(df["Person_id"].unique()))
# selected_date_range = st.sidebar.date_input("Select Date Range", [])



# #endregion
# #region General Trends


# st.markdown("---")
# st.markdown("## ⏳ Time Period Analysis (2025 Only)")

# # Event Distribution
# st.subheader("🔥 Activity Heatmap (Time Period vs. Weekday)")

# # Prepare data for heatmap
# heatmap_data = df.groupby(["Weekday", "Time_period"]).size().unstack().fillna(0)
# heatmap_data = heatmap_data.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

# # Plot heatmap
# fig, ax = plt.subplots(figsize=(10, 5))
# sns.heatmap(heatmap_data, cmap="Blues", linewidths=0.5, annot=True, fmt=".0f", ax=ax)
# ax.set_title("Event Frequency by Time Period & Weekday")

# st.pyplot(fig)

# # Hexagon Plot
# st.subheader("⏳ Timeframe Distribution (Hexagon Plot)")

# # Ensure all time slots are represented
# time_slots = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24"]
# time_counts = df_2025["Time_period"].value_counts().reindex(time_slots, fill_value=0)

# # Radar plot
# fig = go.Figure()
# fig.add_trace(go.Scatterpolar(
#     r=time_counts.values,
#     theta=time_counts.index,
#     fill='toself',
#     name='Overall Activity',
#     line=dict(color="blue")  # Ensure it's visible
# ))
# fig.update_layout(
#     polar=dict(radialaxis=dict(visible=True, range=[0, max(time_counts.values) + 1])),
#     showlegend=False,
#     title="Time Period Presence"
# )

# st.plotly_chart(fig)

# # Invitee vs. Member Activity
# df_feb_2025 = df[(df["Year"] == 2025) & (df["Day"].dt.month == 2)]
# df_feb_2025["Is_Invitee"] = df_feb_2025["Person_id"].str.endswith("c")

# invitee_data = df_feb_2025.groupby("Is_Invitee").size().rename({False: "Members", True: "Invitees"}).reset_index(name="Count")

# fig = px.bar(invitee_data, x="Is_Invitee", y="Count", title="Member vs. Invitee Event Count (Feb 2025)", color="Is_Invitee")
# st.plotly_chart(fig)


# st.subheader("🔍 BFAc Deep Dive: February 2025 Record")

# # Filter to BFAc in Feb 2025
# df_bfac = df[(df["Person_id"] == "BFAc") & (df["Year"] == 2025) & (df["Day"].dt.month == 2)]

# # Count events per day
# bfac_daily = df_bfac.groupby("Day").size().reset_index(name="Count")

# # Line plot of BFAc's activity
# fig = px.line(bfac_daily, x="Day", y="Count", title="BFAc's Event Activity (Feb 2025)", markers=True)
# st.plotly_chart(fig)

# # Compare BFAc to others in Feb 2025
# df_feb_counts = df_feb_2025.groupby("Person_id").size().reset_index(name="Count")
# df_feb_counts = df_feb_counts.sort_values(by="Count", ascending=False)

# fig = px.bar(df_feb_counts, x="Person_id", y="Count", title="Events by Person (Feb 2025)", color="Count")
# st.plotly_chart(fig)
