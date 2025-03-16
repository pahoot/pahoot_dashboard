import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def streak_analysis_fun(df_all : pd.DataFrame):

    st.subheader("🔥 Streak Analysis: Longest Consecutives Days of Activity")

    # Sort by Person and Date
    df_sorted = df_all.sort_values(["Person_id", "Day"])

    # Calculate streaks
    streaks = {}
    current_streak = {}
    previous_day = {}

    for _, row in df_sorted.iterrows():
        person = row["Person_id"]
        date = row["Day"]
        
        if person not in previous_day:
            current_streak[person] = 1
        else:
            # If the previous day was exactly 1 day before, continue the streak
            if (date - previous_day[person]).days == 1:
                current_streak[person] += 1
            # If the previous day is the same as the current day, do nothing
            elif (date - previous_day[person]).days == 0:
                pass
            else:
                # Streak ended, save the longest streak
                streaks[person] = max(streaks.get(person, 0), current_streak[person])
                current_streak[person] = 1  # Reset streak
        
        previous_day[person] = date

    # Save the last streak
    for person in current_streak:
        streaks[person] = max(streaks.get(person, 0), current_streak[person])

    # Convert to DataFrame and sort
    streak_df = pd.DataFrame(streaks.items(), columns=["Person_id", "Max_Streak"]).sort_values(by="Max_Streak", ascending=False)

    # Plot bar chart
    fig = px.bar(streak_df, x="Person_id", y="Max_Streak", title="Longest Streak by Person", color="Max_Streak")
    st.plotly_chart(fig)
