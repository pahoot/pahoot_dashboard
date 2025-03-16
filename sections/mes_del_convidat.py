import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def show_mes_del_convidat(df):

    df_feb_2025 = df[(df["Day"].dt.month == 2) & (df['Day'].dt.year == 2025)].copy()  # Filter for February 2025
    df_feb_2025["Is_Invitee"] = df_feb_2025["Person_id"].astype(str).str.endswith("c")
    invitee_data = df_feb_2025.groupby("Is_Invitee").size().rename({False: "Members", True: "Invitees"}).reset_index(name="Count")

    st.markdown("## 👥 Mes del convidat")

    # 📊 Invitee vs. Member Activity
    st.subheader("Gaioles dels membres vs convidats")

    convidat_amount = df[df["Person_id"].str.len() == 4]["Person_id"].nunique()
    member_amount = df[df["Person_id"].str.len() == 3]["Person_id"].nunique()
    gaiola_convidat_dia = round(df_feb_2025[df_feb_2025["Is_Invitee"] == True].shape[0] / convidat_amount, 2)
    gaiola_member_dia = round(df_feb_2025[df_feb_2025["Is_Invitee"] == False].shape[0] / member_amount, 2)
    st.write(f"Cal tenir en compte que hi havien {convidat_amount} convidats i {member_amount} membres durant el mes del convidat, cosa que vol dir que en termes de gaioles per dia els convidats {gaiola_convidat_dia} guanyen els membres {gaiola_member_dia}.")


    fig = px.bar(invitee_data, x="Is_Invitee", y="Count", title="Member vs. Invitee Event Count (Feb 2025)", color="Is_Invitee")
    st.plotly_chart(fig)

    # 🔍 **BFAc Deep Dive in February 2025**
    st.subheader("🔍 BFAc Deep Dive: February 2025 Record")

    # Ensure BFAc data exists
    df_bfac = df_feb_2025[df_feb_2025["Person_id"] == "BFAc"].copy()

    if not df_bfac.empty:
        # Count events per day
        bfac_daily = df_bfac.groupby("Day").size().reset_index(name="Count")

        # Line plot of BFAc's activity
        fig = px.line(bfac_daily, x="Day", y="Count", title="BFAc's Event Activity (Feb 2025)", markers=True)
        st.plotly_chart(fig)
    else:
        st.write("❌ No event data available for BFAc in February 2025.")

    # 📊 Compare BFAc to others in Feb 2025
    st.subheader("📊 Event Participation in February 2025")

    df_feb_counts = df_feb_2025.groupby("Person_id").size().reset_index(name="Count")
    df_feb_counts = df_feb_counts.sort_values(by="Count", ascending=False)

    fig = px.bar(df_feb_counts, x="Person_id", y="Count", title="Events by Person (Feb 2025)", color="Count")
    st.plotly_chart(fig)
