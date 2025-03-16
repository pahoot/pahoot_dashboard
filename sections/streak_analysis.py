import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def show_streak_analysis(df_all: pd.DataFrame):
    col1, col2 = st.columns([4, 1])  # Adjust column widths

    col1.markdown("## 🔥 Streak analysis")
    # Show button to show/hide invitees
    with col2:
        exclude_invitees = st.checkbox("Excloure convidats", value=True)

    if exclude_invitees:
        df_all = df_all[df_all["Person_id"].str.len() != 4]

    # Sort by Person and Date
    df_sorted = df_all.sort_values(["Person_id", "Day"])

    # Streaks Calculation
    streaks = {}        # Stores longest active streaks
    inactive_streaks = {}  # Stores longest inactivity streaks
    current_streak = {}
    current_inactive = {}
    previous_day = {}

    active_dates = {}  # Stores dates of longest activity streak
    inactive_dates = {}  # Stores dates of longest inactivity streak

    for _, row in df_sorted.iterrows():
        person = row["Person_id"]
        date = row["Day"]
        
        if person not in previous_day:
            current_streak[person] = 1
            current_inactive[person] = 0
            streak_start = date  # Start tracking a new active streak
        else:
            gap = (date - previous_day[person]).days
            
            if gap == 1:
                # Continuing an active streak
                current_streak[person] += 1
            elif gap > 1:
                # Save the previous active streak
                if current_streak[person] > streaks.get(person, 0):
                    streaks[person] = current_streak[person]
                    active_dates[person] = (streak_start, previous_day[person])  # Store active streak dates
                
                # Save the inactive streak
                if gap - 1 > inactive_streaks.get(person, 0):
                    inactive_streaks[person] = gap - 1
                    inactive_dates[person] = (previous_day[person] + pd.Timedelta(days=1), date - pd.Timedelta(days=1))
                
                # Reset active streak tracking
                current_streak[person] = 1
                streak_start = date  # Start new active streak

        previous_day[person] = date

    # Ensure last streak is recorded
    for person in current_streak:
        if current_streak[person] > streaks.get(person, 0):
            streaks[person] = current_streak[person]
            active_dates[person] = (streak_start, previous_day[person])  # Store final active streak dates

    # Save the last streaks
    for person in current_streak:
        streaks[person] = max(streaks.get(person, 0), current_streak[person])
    for person in current_inactive:
        inactive_streaks[person] = max(inactive_streaks.get(person, 0), current_inactive[person])

    # Convert to DataFrames
    streak_df = pd.DataFrame(streaks.items(), columns=["Person_id", "Max_Streak"]).sort_values(by="Max_Streak", ascending=False)
    inactive_df = pd.DataFrame(inactive_streaks.items(), columns=["Person_id", "Max_Inactive_Streak"]).sort_values(by="Max_Inactive_Streak", ascending=False)

    # 📊 Plot Active Streaks
    st.subheader("📈 Longest Consecutive Streak of Activity")
    fig_active = px.bar(streak_df, x="Person_id", y="Max_Streak", color="Max_Streak")
    st.plotly_chart(fig_active)

    # 📉 Plot Inactive Streaks
    st.subheader("🧘 Longest Consecutive Streak of Abstinence")
    fig_inactive = px.bar(inactive_df, x="Person_id", y="Max_Inactive_Streak", color="Max_Inactive_Streak")
    st.plotly_chart(fig_inactive)

    # 👤 **Select a Participant to See Exact Streak Dates**
    st.subheader("🔍 Detall individual")
    selected_person = st.selectbox("Select a participant:", sorted(df_all["Person_id"].unique()))

    # Only proceed if the selected person has any streak data
    if selected_person in streaks or selected_person in inactive_streaks:
        # Gather data
        active_streak = streaks.get(selected_person, "N/A")
        inactive_streak = inactive_streaks.get(selected_person, "N/A")
        active_start, active_end = active_dates.get(selected_person, ("N/A", "N/A"))
        inactive_start, inactive_end = inactive_dates.get(selected_person, ("N/A", "N/A"))

        # Create DataFrame for better visualization
        streak_data = pd.DataFrame({
            "Streak Type": ["🔥 Active Streak", "🧘 Inactive Streak"],
            "Duration (Days)": [active_streak, inactive_streak],
            "Start Date": [active_start, inactive_start],
            "End Date": [active_end, inactive_end]
        })

        # Display as a table
        st.table(streak_data)
    else:
        st.write("⚠️ No streak data available for this participant.")
