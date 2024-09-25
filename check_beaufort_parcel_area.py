import time
import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path

start = time.time()
parcels_shp = Path("../data/Beaufort-County-Parcels/parcels.shp")

# read the parcel records into a GeoDataFrame
parcel = gpd.read_file(parcels_shp)

# reproject the parcel data into EPSG:5070, NAD83/Conus Albert CRS
parcel_5070 = parcel.to_crs("EPSG:5070")

# create a new Series for area
area_5070 = pd.Series(0.0, index=parcel_5070.index, dtype=np.float64)

# create a new Series for area difference
area_diff = pd.Series(0.0, index=parcel_5070.index, dtype=np.float64)

# calculate area with NAD83/CONUS Albert project
for i in parcel_5070.index:
    area_5070.loc[i] = parcel_5070.loc[i, "geometry"].area * 0.000247105  # square meters to acres
    area_diff.loc[i] = area_5070.loc[i] - parcel.loc[i, "CalcAcres"]
# add a new column to the GeoDataFrame
parcel_5070["Acre_5070"] = area_5070
parcel_5070["Acre_Diff"] = area_diff

fig, ax = plt.subplots(1)
parcel_5070[(parcel_5070["Acre_Diff"] > 3.0) & (parcel_5070["Acre_Diff"] < 4.0)].plot(ax=ax, column="Acre_Diff",
                                                                                  cmap="jet", legend=True)
ax.set_title("3 < Acre Differences < 4")
plt.show()

if __name__ == "__main__":
    print(time.time() - start)