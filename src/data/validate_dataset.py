import pandas as pd

df = pd.read_csv("data/raw/synthetic_tickets.csv")

print("=== TEAM DISTRIBUTION ===")
print(df["queue"].value_counts(), "\n")

print("=== UNIQUE TEXT COUNT ===")
print(df["body"].nunique(), "\n")

print("=== TEXT LENGTH ===")
print(df["body"].str.len().describe(), "\n")

print("=== SAMPLE 5 ROWS ===")
print(df[["subject", "body", "queue"]].sample(5))
