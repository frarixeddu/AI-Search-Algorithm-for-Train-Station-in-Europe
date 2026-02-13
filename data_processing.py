import pandas as pd

def process_stations(input_file, output_file):
    df = pd.read_csv(input_file, low_memory=False)
    
    # filtering by main stations and provided with coordinates
    filtered = df[df["is_main_station"] == True].dropna(subset=["latitude", "longitude"]).copy()
    
    # sampling 3 stations per nation (or less)
    sampled_list = []
    for country, group in filtered.groupby("country"):
        sample_size = min(3, len(group))
        sampled_group = group.sample(n=sample_size, random_state=42)
        sampled_list.append(sampled_group)
    
    sampled = pd.concat(sampled_list, ignore_index=True)

    # reducing feature dataset number size (even for Google My Maps visualization purpose)
    selected = sampled[["name", "country", "latitude", "longitude"]]
    
    selected.to_csv(output_file, index=False)
    return selected.set_index('name')