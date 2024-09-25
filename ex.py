import pandas as pd
from geopy.geocoders import Nominatim
import simplekml

# Load the CSV file
file_path = 'path_to_your_file/active_verified_pitt.csv'
data = pd.read_csv(file_path)

# Filter the rows where the last name initial is "J"
filtered_data = data[data['last_name'].str.startswith('J')]

# Select the necessary columns
selected_columns = ['last_name', 'first_name', 'middle_name', 'res_street_address', 'res_city_desc', 'state_cd', 'zip_code']
filtered_data = filtered_data[selected_columns]

# Select at least 10 addresses for geocoding
sampled_data = filtered_data.head(10)

# Initialize geocoder
geolocator = Nominatim(user_agent="voter_geocoder")

# Function to geocode an address
def geocode_address(row):
    address = f"{row['res_street_address']}, {row['res_city_desc']}, {row['state_cd']}, {row['zip_code']}"
    try:
        location = geolocator.geocode(address)
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        return pd.Series([None, None])

# Apply geocoding to the sampled data
sampled_data[['latitude', 'longitude']] = sampled_data.apply(geocode_address, axis=1)

# Generate KML file
kml = simplekml.Kml()

for _, row in sampled_data.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        name = f"{row['first_name']} {row['middle_name'] or ''} {row['last_name']}".strip()
        kml.newpoint(name=name, coords=[(row['longitude'], row['latitude'])])

# Save the KML file
kml.save("voters.kml")
