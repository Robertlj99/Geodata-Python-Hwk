import time
import geopandas as gpd
from pathlib import Path
from matplotlib import pyplot as plt

# Paths
start = time.time()
output = Path("../Output")
data = Path("../Data")
gis = data / "GIS_Data"

# Doing this globally so I don't need to pass it
all_voters = gpd.read_file(data / "pitt_voters.gpkg", engine="pyogrio")

# Attempted to refactor this using spatial join
def count_voter_by_polygon(point_gdf: gpd.GeoDataFrame, polygons_gdf: gpd.GeoDataFrame):
    # Convert the voter data from into ESPG:2264
    point_2264 = point_gdf.to_crs("EPSG:2264")

    # Create result GeoDataFrame
    result_gdf = gpd.GeoDataFrame(columns=["Count", "Density"], geometry=polygons_gdf.geometry)

    # Using spatial join to save time for my laptop
    joined = gpd.sjoin(point_2264, polygons_gdf, how="inner", predicate="within")
    counts = joined.groupby("index_right").size()

    # Populate counts
    result_gdf["Count"] = counts.reindex(result_gdf.index).fillna(0)

    # Calculate density person/acre
    result_gdf["Density"] = result_gdf["Count"] / (result_gdf.geometry.area * 3.86102e-7)

    return result_gdf

def main(school_level, poly_file):
    # Read polygon file
    polygons_gdf = gpd.read_file(poly_file)
    # Subset voters according to party
    party_groups = {
        "DEM": all_voters[all_voters["party_cd"] == "DEM"],
        "REP": all_voters[all_voters["party_cd"] == "REP"],
        "UNA": all_voters[all_voters["party_cd"] == "UNA"]
    }

    results = {}

    # Count
    for party, voters in party_groups.items():
        results[party] = count_voter_by_polygon(voters, polygons_gdf)

    # Calculate total
    total_voters_by_district = sum(results[party]["Count"] for party in results)

    # Calculate percent
    for party in results:
        results[party]["Percent"] = 100 * results[party]["Count"] / total_voters_by_district

    # Plot
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))
    cmap = "jet"
    for i, (party, result_gdf) in enumerate(results.items()):
        result_gdf.plot(column="Count", ax=axes[i, 0], legend=True, cmap=cmap)
        result_gdf.plot(column="Density", ax=axes[i, 1], legend=True, cmap=cmap)
        result_gdf.plot(column="Percent", ax=axes[i, 2], legend=True, cmap=cmap)
        axes[i, 0].set_title(f"{party} Count")
        axes[i, 1].set_title(f"{party} Density")
        axes[i, 2].set_title(f"{party} Percentage")

    plt.suptitle(
        f"Pitt County Voter Distribution by {school_level} School Districts, by Robert Johnson (johnsonro18@students.ecu.edu)")
    plt.tight_layout()
    plot_filename = output / f"{school_level.lower()}_school_distribution_Robert_Johnson.jpg"
    plt.savefig(plot_filename, format="jpg")
    plt.show()

if __name__ == "__main__":
    school_levels = ["Elementary", "Middle", "High"]
    for level in school_levels:
        polygons = gis / f"Pitt_County_{level}_School_Attendance_Districts/Pitt_County_{level}_School_Attendance_Districts.shp"
        main(level, polygons)