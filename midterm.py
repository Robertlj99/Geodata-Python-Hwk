# I discussed this and compared results with Chris Johnson and Marquise Fowler
import time
import pandas as pd
import geopandas as gpd
from pathlib import Path
from multiprocessing import Pool
from matplotlib import pyplot as plt

# Set path variables so files can be accessed regardless of OS
data_path = Path("../midterm-data")
bf_voter_csv = data_path / "beaufort_voter.csv"
active_voters_csv = data_path / "active_voters.csv"
address_shp = data_path / "Beaufort-County-Streets/addresses.shp"
address_csv = data_path / "address_4326.csv"
address_gpkg = data_path / "address_4326.gpkg"
matched_address_gpkg = data_path / "matched_address.gpkg"

def get_active_voters():
    # Read voter file into dataframe
    voter_df = pd.read_csv(bf_voter_csv)
    # Select only active voters
    active_voter_flags = voter_df["voter_status_desc"] == "ACTIVE"
    active_voter_df = voter_df[active_voter_flags]
    # Print total number of active voters and save dataframe to active_voters.csv
    print("Total number of active voters: ", len(active_voter_df))
    active_voter_df.to_csv(active_voters_csv)

def get_address_data():
    # Read address file into GeoDataFrame and convert the geometry from NAD83 to WGS84
    add_gdf = gpd.read_file(address_shp)
    address_4326 = add_gdf.to_crs(epsg=4326)
    # Save address file as GPKG file
    address_4326.to_file(address_gpkg, driver="GPKG")

def preprocess_address_data(address):
    # Remove any double-spaced separations and convert to uppercase
    address = ' '.join(address.split()).upper()
    return address

# This function is directly from your provided code, except I convert to uppercase in the preprocessing
def match_address(add_str: str,            # from voter data
                  add_series: pd.Series):  # from address data
    idx = None
    for i in add_series.index:
        add_gpd = add_series.loc[i]
        if add_str in add_gpd:
            idx = i
            break
    return idx

# I'm using your parallel_computation_1 code as my source code here
def parallel():
    start = time.time()
    # Read in voter and address files
    voters = pd.read_csv(active_voters_csv)
    addresses = gpd.read_file(address_gpkg)
    print("read files done in ", time.time() - start, " seconds")
    # Preprocess the street addresses and convert to list
    processed_voters = voters['res_street_address'].apply(preprocess_address_data)
    processed_voters = processed_voters.to_list()
    print("first preprocess done in ", time.time() - start, " seconds")
    # Preprocess the full addresses
    address_series = addresses['FullAddres'].apply(preprocess_address_data)
    print("second preprocess done in ", time.time() - start, " seconds")
    # Create input list
    input_list = [(add_str, address_series) for add_str in processed_voters]

    # Parallel computation
    with Pool(6) as process_pool:
        returned_index_list = process_pool.starmap(func=match_address, iterable=input_list)
    print("parallel done in ", time.time() - start, " seconds")
    final_add_list = []
    final_geo_list = []

    for add_idx, gpd_idx in enumerate(returned_index_list):
        if gpd_idx is not None:
            final_add_list.append(processed_voters[add_idx])
            final_geo_list.append(addresses.loc[gpd_idx, "geometry"])

    matched_address_df = pd.DataFrame(data={"StreetAddress": final_add_list,
                                            "geometry": final_geo_list})
    total = len(matched_address_df)

    matched_add_gdf = gpd.GeoDataFrame(data=matched_address_df, geometry="geometry")
    matched_add_gdf.to_file(matched_address_gpkg, driver="GPKG")
    matched_add_gdf.plot()
    plt.title(str(total))
    plt.show()
    print(time.time() - start, " seconds")

if __name__ == "__main__":
    #get_active_voters()
    #get_address_data()
    parallel()