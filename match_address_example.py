import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt

active_voter = pd.read_csv("active_voter.csv")
add_100 = active_voter["res_street_address"][0:100]
print("Data type of add_100:", type(add_100))

# convert the Series into a list
add_list0 = add_100.to_list()
print("add_list0: \n", add_list0)

# trim the tailing space in the addresses
# The rstrip() method removes any trailing characters (characters at the end a string), space is
# the default trailing character to remove.
add_list1 = [add.rstrip() for add in add_list0]
print("add_list1:\n", add_list1)

# read the address geopackage file
add_gpd = gpd.read_file("address_4326.gpkg")

# contain matched addresses
final_address_list = []

# contain matched geometry
final_geometry_list = []

for add1 in add_list1:   # this is from voter data frame
    for i in add_gpd.index:   # this is from the address geo data frame
        add2 = add_gpd.loc[i, "FullAddres"]
        # make sure both addresses are in upper case
        if add1.upper() in add2.upper():
            final_address_list.append(add1)
            final_geometry_list.append(add_gpd.loc[i, "geometry"])
            break

# create a DataFrame
add_geo_pd = pd.DataFrame(data={"MailAdd": final_address_list,
                                "AddLatLon": final_geometry_list})

# create a GeoDataFrame
add_geo_gpd = gpd.GeoDataFrame(data=add_geo_pd, geometry="AddLatLon")
add_geo_gpd.to_file("add100.gpkg", driver="GPKG")
add_geo_gpd.plot()
plt.show()
