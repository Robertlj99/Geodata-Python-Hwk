import geopandas as gpd
from pathlib import Path
from matplotlib import pyplot as plt

# let's use the Path class again
data_path = Path("../Data")
# the "/" operator return a new "Path" object
address_shp_file = data_path / "Beaufort_Count_Streets/addresses.shp"
print("type of address_shp_file: ", type(address_shp_file))

# Pandas and GeoPandas can take "PosixPath" directly
# read more about PosixPath: https://docs.python.org/3/library/pathlib.html
addreess_gdf = gpd.read_file(address_shp_file)
addreess_gdf.plot()
plt.show()

# if we drop "geometry" column, we can convert the GeoDataFrame into a DataFrame
address_df = addreess_gdf.drop(columns=["geometry"])
address_df.to_csv("beaufort_address.csv")

# What if we output the gdf into a CSV file?
addreess_gdf.to_csv("beaufort_address_gdf.csv")
print("CRS: ", addreess_gdf.crs)

# covert the address into WGS84, EPSG:4326
address_4326 = addreess_gdf.to_crs(epsg=4326)

# save the 4326 geodataframe
address_4326.to_csv("address_4326.csv")
address_4326.to_file("address_4326.gpkg", driver="GPKG")