from sqlalchemy import create_engine, text
from settings import DB_CONNECTION_STRING
from sqlalchemy import text
import pandas as pd

def fetch_data():
    """Fetch event data from the database."""
    query = text("SELECT g.*, pseudonim FROM Gaioles g join Person p on p.person_id = g.person_id")
    engine = create_engine(DB_CONNECTION_STRING)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    # Convert to datetime
    df["Day"] = pd.to_datetime(df["Day"])
    df["Year"] = df["Day"].dt.year

    # Add Catalan month names
    month_names_cat = {
        1: "Gener", 2: "Febrer", 3: "Març", 4: "Abril",
        5: "Maig", 6: "Juny", 7: "Juliol", 8: "Agost",
        9: "Setembre", 10: "Octubre", 11: "Novembre", 12: "Desembre"
    }
    
    df["Month"] = df["Day"].dt.month.map(month_names_cat)  # Convert month number to name

    weekday_map = {
        "Monday": "Dilluns", "Tuesday": "Dimarts", "Wednesday": "Dimecres",
        "Thursday": "Dijous", "Friday": "Divendres", "Saturday": "Dissabte", "Sunday": "Diumenge"
    }
    df["Weekday"] = df["Weekday"].map(weekday_map)
    
    # Sort for streak analysis
    df = df.sort_values(by=["Person_id", "Day"])
    
    return df