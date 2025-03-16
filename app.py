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

df_all = df  # All years for general plots

# Dashboard Title
st.title("📊 Pahoot: Event Dashboard")

# KPI Metrics
col1, col2 = st.columns(2)
col1.metric(label="Gaioles totals", value=len(df))
# Count number of days from 1-1-2023
col2.metric(label="Dies desde l'inici de Pahoot", value=(datetime.today() - datetime(2023,1,1)).days)
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Yearly Recap", "Year-over-Year Comparison", "Streak analisis", "Time Analysis", 'Mes del Convidat'])

# if page == "General Overview":
#     show_general_overview(df_all)

if page == "Yearly Recap":
    show_yearly_recap(df_all)

elif page == "Year-over-Year Comparison":
    show_yoy_comparison(df_all)

elif page == "Streak analisis":
    show_streak_analysis(df_all)

# Hide for the moment as it is in development
# elif page == "Time Analysis":
#     show_time_analysis(df_all)

elif page == 'Mes del Convidat':
    show_mes_del_convidat(df_all)

