from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from shapely.geometry import Point
import pandas as pd
from tqdm import tqdm
import time

geolocator = Nominatim(user_agent="example_07")
# use RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
# read the CSV file into a DataFrame
df = pd.read_csv("./Greenville_address_100.csv")
print("address column:\n", df["address"])
tqdm.pandas()
start_time = time.time()
df["location"] = df["address"].progress_apply(geocode)
end_time = time.time()
df.to_csv("./new_address.csv")
print("time usage: %f seconds" % (end_time - start_time))
