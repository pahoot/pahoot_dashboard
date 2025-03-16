
## **📝 Step 2: Define Our To-Do List (Plots & Features)**  

### **📊 1. Basic Stats & Aggregates**  
✅ **Total events per person** (bar chart)  
✅ **Total events per weekday** (bar chart)  
✅ **Average events per day per person**  

---

### **📅 2. Time-Based Analysis**  
✅ **Heatmap of event occurrences by day & time**  
✅ **Weekday behavior comparison**  
✅ **Yearly growth comparison (2023 vs. 2024 vs. 2025)**  
✅ **Monthly trends over time**  

---

### **⏳ 3. Timeframe Distribution (Hexagon Plot)**  
✅ **Hexagonal plot where vertices represent timeframes**  
✅ **Shows how active someone is in each time window**  

---

### **👥 4. Invitee Month (February 2025) Analysis**  
✅ **Compare member vs. invitee total events**  
✅ **Close analysis of `BFAc` (most events in a single month)**  

---

### **📌 5. Interactive Dashboard in Streamlit**  
✅ **Dropdown to select person & compare**  
✅ **Filters for date range & weekdays**  
✅ **Downloadable reports (CSV or images)**  

---

### **📌 6. Activity Patterns & Clusters**  
✅ **K-Means Clustering of Users Based on Activity**  
   - Groups users with **similar event patterns**.  
   - Helps find **“night owls” vs. “early risers” vs. “balanced” users**.  
   - Visualized with a **scatter plot or radar chart**.  

✅ **Most Active Hours per User (Line Chart or Heatmap)**  
   - Shows each person’s **peak activity time**.  
   - Useful for seeing if someone prefers **late nights vs. mornings**.  

✅ **Rolling Averages & Anomalies**  
   - **Rolling 7-day average** to smooth trends.  
   - Detects if someone had **an unusually active period**.  

---

### **📌 7. Invitee Behavior vs. Member Behavior**  
✅ **Ratio of Member vs. Invitee Activity**  
   - Does an invitee tend to be **more or less active** than the member who invited them?  
   - Scatter plot showing **invitee vs. member events**.  

✅ **Did Invitees Mimic the Members? (Timeframe Overlap Heatmap)**  
   - **Heatmap comparing when members & invitees were active**.  
   - Did invitees follow the same time pattern as their inviter?  

---

### **📌 8. Special Events / Outliers**  
✅ **Single-Day Highs & Lows (Biggest Event Spikes)**  
   - What was the **busiest day ever**?  
   - **Did it align with a specific event?**  

✅ **Streak Analysis (Longest Active Streaks per Person)**  
   - Shows **who had the longest unbroken streak of activity**.  
   - Useful for identifying **consistent users**.  

---

### **📌 9. Interactive Network Graph (Who Invited Who?)**  
✅ **Graph visualization of invitee relationships**  
   - Nodes = People, Edges = Who invited whom.  
   - Helps **visualize how the invitee system worked**.  

---