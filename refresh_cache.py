from settings import DB_CONNECTION_STRING
from sqlalchemy import create_engine, text
import pandas as pd

query = text("SELECT g.*, pseudonim FROM Gaioles g join Person p on p.person_id = g.person_id")
engine = create_engine(DB_CONNECTION_STRING)
with engine.connect() as conn:
    df = pd.read_sql(query, conn)

df.to_csv("data/database.csv", index=False)
print("Data fetched and saved to 'data/database.csv'.")