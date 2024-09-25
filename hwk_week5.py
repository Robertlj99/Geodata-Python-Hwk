import re
import time
import simplekml
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

start = time.time()

# Read file
pitt_csv = Path("../data/active_verified_pitt.csv")
data = pd.read_csv(pitt_csv)

# Initialize geocoder w/ rate limiter
geolocator = Nominatim(user_agent="homework")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# During testing I've found a need to preprocess the data so that the geocode will work, specifically removing any
# apartment or building numbers (i.e. #6)
def preprocess_address_data(address):
    # I'm using regex to locate and remove hastags and any data with them
    address = re.sub(r'#\d+', '', address)
    # Clean up spacing while im here
    address = address.strip()
    return address

# Geocode function, my original inclination was to do this like I have the previous apply functions I've made for this class,
# but I believe that if I try to bulk geocode the entire series it will violate the rate limiter and lead to issues with errors
# therefore I'm going row by row rather than applying to a series
def code_address(row):
    # Grab the address from the row
    address_dict = {"street": f"{row['res_street_address']}",
                    "city": f"{row['res_city_desc']}",
                    "county": "Pitt",
                    "state": f"{row['state_cd']}",
                    "postalcode": f"{int(row['zip_code'])}"}

    print(f"Geocoding address: {address_dict}")  # Debugging output

    # noinspection PyBroadException
    try:
        # Attempt to geocode it
        location = geolocator.geocode(address_dict)
        if location:
            # If successful return lat and long data
            print(f"Geocoded to: {location.latitude}, {location.longitude}", '\n')
            return pd.Series([location.latitude, location.longitude])
        else:
            # If not return empty series
            print("Geocoding failed: No location found", '\n')
            return pd.Series([None, None])

    except Exception as e:
        print(f"Geocoding error: {e}", '\n')
        return pd.Series([None, None])


if __name__ == "__main__":
    # N is the number of addresses you wish to geocode, to change it simply change n below
    n = 10
    # Filter for last names starting with J, the letter that matches my last name
    matched_data = data[data['last_name'].str.startswith('J')]
    # Grab only the necessary columns
    necessary = ['last_name', 'first_name', 'middle_name', 'res_street_address', 'res_city_desc', 'state_cd', 'zip_code']
    matched_data = matched_data[necessary]
    # Grab the first n instances
    matched_data = matched_data[:n]
    # Preprocess street address data
    matched_data['res_street_address'] = matched_data['res_street_address'].apply(preprocess_address_data)

    # Apply geocoding function with tqdm
    tqdm.pandas(desc="Applying geocoding function")
    matched_data[['latitude', 'longitude']] = matched_data.progress_apply(code_address, axis=1)

    # Generate and save KML file
    kml = simplekml.Kml()
    for _, row in matched_data.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            print('got here')
            name = f"{row['first_name']} {row['middle_name'] or ''} {row['last_name']}".strip()
            print(name, row['longitude'], row['latitude'])
            kml.newpoint(name=name, coords=[(row['longitude'], row['latitude'])])

    # Save the KML file
    kml_addr = Path("../data/voters.kml")
    kml.save(kml_addr)
    print(time.time()-start)