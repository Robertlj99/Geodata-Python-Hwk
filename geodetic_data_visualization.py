import geopandas as gpd
from matplotlib import pyplot as plt

# read GeoPackage
gdf = gpd.read_file("./Data/Geodetic_Data/Geodetic_Control_Points.gpkg")
print("columns of the GeoDataFrame: ", gdf.columns)
gdf.plot()
plt.show()

# create an index for Pitt county
pitt_county_index = gdf["countyname"]=="Pitt"
# subset the points for Pitt count
pitt_county_points = gdf[pitt_county_index]
# plot geometry
pitt_county_points.plot()
plt.show()

# plot with a variable name
pitt_county_points.plot(column="orthoheigh")
plt.show()

# plot with a color mapping and legend
pitt_county_points.plot(column="orthoheigh", cmap="jet", legend=True)
plt.show()

