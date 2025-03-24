import pandas as pd

file = "UNSW_NB15.csv"  # Agar extension .csv hai
df = pd.read_csv(file)

print(df.head())  # Pehli 5 rows print karega
print(df.columns)  # Sare column names dikhayega
