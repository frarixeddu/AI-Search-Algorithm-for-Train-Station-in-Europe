import numpy as np
import pandas as pd

# importing database from kaggle's .csv file
df = pd.read_csv("train_stations_europe.csv", low_memory=False)

# extracting just the samples where train station is a main station
filtered = df[df["is_main_station"] == True].copy()

# removing rows without coordinates
filtered = filtered.dropna(subset=["latitude", "longitude"])

# sampling for country 
sampled_list = []
for country, group in filtered.groupby("country"):
    sample_size = min(3, len(group))
    sampled_group = group.sample(n=sample_size, random_state=42)
    sampled_list.append(sampled_group)

sampled = pd.concat(sampled_list, ignore_index=True)

# columns we want to pass to Google My Maps
selected = sampled[[
    "name",
    "country",
    "latitude",
    "longitude"
]]

# save the info in a csv file for Google My Maps
selected.to_csv("selected_train_stations.csv", index=False)

# print("File creato con successo!")
# print(f"Numero di stazioni selezionate: {len(selected)}")
# print(f"\nPaesi inclusi:\n{selected['country'].value_counts()}")