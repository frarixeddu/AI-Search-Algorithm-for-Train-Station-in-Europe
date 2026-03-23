# this module just takes the complete station dataset and 
# provides a filtered version with lower number of stations 

import pandas as pd

def process_stations(input_file, output_file):
    df = pd.read_csv(input_file, low_memory=False)
    
    # filtering df by "is_main_stations" feature and provided with coordinates
    filtered = df[df["is_main_station"] == True].dropna(subset=["latitude", "longitude"]).copy()
    
    # sampling 3 stations for each country 
    sampled_list = []
    # When we loop filtered DF, Pandas returns a pair (tuple) of objects
    # the first object is a key value of the grouping that we put in "Country" and acts as a temporaneous variable 
    # the second object is a little DF that we put in "country_group" that will contain only the rows belonging to "countries"
    for Country, country_group in filtered.groupby("country"): 
        sample_size = min(3, len(country_group))            # if 3 stations are not possible, allow to take less)
        sampled_group = country_group.sample(n=sample_size, random_state=42)    # sample by "country" with the computed size
        sampled_list.append(sampled_group)      # list composed by little DataFrames [DF1, DF2, DF3, ...] thanks to .append method
    
    sampled = pd.concat(sampled_list, ignore_index=True)    # the previous list is converted in a big and unique DataFrame. The little DataFrames are vertically stacked to create the final DF "sampled"

    # extracting only attributes we are interested in (done also for Google My Maps visualization purpose)
    selected = sampled[["name", "country", "latitude", "longitude"]]
    
    # index=False to avoid indexing (we'll use the name as index)
    selected.to_csv(output_file, index=False)
    return selected.set_index('name')