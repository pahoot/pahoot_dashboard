import pandas as pd

def calculate_streaks(df: pd.DataFrame) -> dict:
    """Calculate longest streaks for each person, considering only unique days."""
    streaks = {}

    for person in df["Person_id"].unique():
        # Select unique days per person (ignore Instance column)
        person_df = df[df["Person_id"] == person][["Person_id", "Day"]].drop_duplicates()

        # Ensure sorting by date
        person_df = person_df.sort_values(by="Day").copy()

        # Calculate gaps between consecutive days
        person_df["Gap"] = person_df["Day"].diff().dt.days.fillna(1)

        # Identify streaks where Gap == 1
        person_df["Streak"] = (person_df["Gap"] == 1).astype(int).cumsum()

        # Find the longest streak
        max_streak = person_df.groupby("Streak")["Day"].count().max()
        streaks[person] = max_streak if max_streak else 0

    return streaks
