import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from concurrent.futures import ProcessPoolExecutor


def match_address(add_str: str,
                  add_series: pd.Series):
    idx = None
    for i in add_series.index:
        add_gpd = add_series.loc[i]
        # make sure both addresses are in upper case
        if add_str.upper() in add_gpd.upper():
            idx = i
            break
    return idx


if __name__ == "__main__":
    active_voter = pd.read_csv("active_voter.csv")
    add_100 = active_voter["res_street_address"][0:100]

    # convert the Series into a list
    add_list0 = add_100.to_list()
    # trim the tailing space in the addresses
    add_list1 = [add.rstrip() for add in add_list0]

    # read shapefile to get address
    address_gpd = gpd.read_file("./address_4326.gpkg")
    full_address_series = address_gpd["FullAddres"]

    # The following list contains reference of the `full_address_series` instead of values. No worry about memory
    add_serieslist = [full_address_series] * len(add_list1)

    # If a function has multiple arguments, then the map function takes multiple iterables corresponding to the
    # arguments.
    with ProcessPoolExecutor(max_workers=6) as exe:
        returned_index_list = exe.map(match_address, add_list1, add_serieslist)

    final_add_list = []
    final_pnt_list = []

    for add_idx, gpd_idx in enumerate(returned_index_list):
        if gpd_idx is not None:
            final_add_list.append(add_list1[add_idx])
            final_pnt_list.append(address_gpd.loc[gpd_idx, "geometry"])

    add_geo_pd = pd.DataFrame(data={"mail_add": final_add_list,
                                    "geometry": final_pnt_list})
    add_geo_gpd = gpd.GeoDataFrame(data=add_geo_pd, geometry="geometry")
    add_geo_gpd.plot()
    plt.show()
