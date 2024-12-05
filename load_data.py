import pandas as pd
from sqlalchemy import create_engine

# Load CSV into DataFrame
df = pd.read_csv("predictions.csv")

# Setup SQLite database
engine = create_engine("sqlite:///papers.db")
df.to_sql("papers", engine, if_exists="replace", index=False)

print("Data loaded successfully.")
