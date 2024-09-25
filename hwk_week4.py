import time
import pandas as pd
import numpy as np
import geopandas as gpd
from tqdm import tqdm
from pathlib import Path
from matplotlib import pyplot as plt

start = time.time()
# You may have to adjust these for this to work for you
parcels_shp = Path("../data/Beaufort-County-Parcels/parcels.shp")
addresses_shp = Path("../data/Beaufort-County-Streets/addresses.shp")
parcel_list = gpd.read_file(parcels_shp)
address_list = gpd.read_file(addresses_shp)
print("Read files complete in %f seconds" % (time.time() - start))

# Convert the area from square meters to acres
def convert_area(series):
    return series.area * 0.000247105

def acre_diff():
    # Convert parcel data to ESPG:5070
    parcel_5070 = parcel_list.to_crs(epsg=5070)

    # Convert the area
    tqdm.pandas(desc="Converting Areas")
    parcel_5070["Acre_5070"] = parcel_5070["geometry"].progress_apply(convert_area)

    # Calculate the difference
    parcel_5070["Acre_Diff"] = parcel_5070["Acre_5070"] - parcel_list["CalcAcres"]
    filtered_parcel = parcel_5070[(parcel_5070["Acre_Diff"] > 3.0) & (parcel_5070["Acre_Diff"] < 4.0)]

    # Plot the dataframe
    fig, ax = plt.subplots(1)
    filtered_parcel.plot(ax=ax, column='Acre_Diff', cmap='jet', legend=True)
    plt.title("Filtered Parcels with Acre_Diff between 3.0 and 4.0")
    plt.savefig("../data/acre_diff.jpg")
    plt.show()
    print(time .time()-start)

def match_address():
    # Make sure both data frames use the same crs
    address = address_list.to_crs(parcel_list.crs)
    address = address[:100]

    # I'm attempting to use pandas as often as possible for speed, so I'm using a spatial join here
    # I'm not entirely sure if the predicate should be within or intersects here and for the second one
    # I'm not sure if it should be intersects or covers but this plot looks good
    # Attempting to use a progress bar on the spatial joins
    tqdm.pandas(desc="Matching Addresses")
    matched_address_list = gpd.sjoin(address.progress_apply(lambda x: x), parcel_list, how='inner', predicate='within')
    tqdm.pandas(desc="Matching Parcels")
    matched_parcel_list = gpd.sjoin(parcel_list.progress_apply(lambda x: x), address, how='inner', predicate='covers')

    # Plot the dataframes
    fig, ax = plt.subplots(1)
    matched_parcel_list.plot(ax=ax, edgecolor='black', facecolor='none')
    matched_address_list.plot(ax=ax, color='red', marker='+', markersize=10)
    plt.title("Matched Addresses")
    plt.ticklabel_format(axis='both', style='sci', scilimits=(0, 0))
    plt.savefig("../data/match_address.jpg", )
    plt.show()
    print(time.time()-start)

# I didn't realize originally you wanted just one plot with both things implemented, so I updated it to have that
def final():
    # Convert both gdf's to ESPG:5070
    parcel_5070 = parcel_list.to_crs(epsg=5070)
    address_5070 = address_list.to_crs(epsg=5070)


    # Convert the area
    tqdm.pandas(desc="Converting Areas")
    parcel_5070["Acre_5070"] = parcel_5070["geometry"].progress_apply(convert_area)

    # Calculate the difference
    parcel_5070["Acre_Diff"] = parcel_5070["Acre_5070"] - parcel_list["CalcAcres"]
    filtered_parcel = parcel_5070[(parcel_5070["Acre_Diff"] > 3.0) & (parcel_5070["Acre_Diff"] < 4.0)]

    # Match using spatial join
    tqdm.pandas(desc="Matching Addresses")
    matched_address_list = gpd.sjoin(address_5070.progress_apply(lambda x: x), filtered_parcel, how='inner', predicate='within')

    # Plot the dataframes
    fig, ax = plt.subplots(1)
    filtered_parcel.plot(ax=ax, edgecolor='black', facecolor='none')
    matched_address_list.plot(ax=ax, color='red', marker='+', markersize=10)
    plt.title("Filtered Parcels w/ Address Matching")
    plt.ticklabel_format(axis='both', style='sci', scilimits=(0, 0))
    plt.savefig("../data/match_and_acre_diff.jpg")
    plt.show()
    print(time.time() - start)

if __name__ == "__main__":
    #acre_diff()
    #match_address()
    final()