import requests
import pandas as pd
import os
import sqlite3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_restaurants(api_key, location, radius, keyword):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    #url = 'https://places.googleapis.com/v1/places:searchNearby'
    params = {
        "location": location,
        "radius": radius,
        "type": keyword,
        "key": api_key
    }

    response = requests.get(url, params=params)
    print('reponse:', response)
    results = response.json().get("results", [])

    restaurants = []
    for result in results:
        name = result.get("name")
        address = result.get("vicinity")
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]
        photo = get_photo_url(api_key, result.get("photos", []))
        place_id = result.get("place_id")
        website = get_place_details(api_key, place_id).get("website")
        restaurants.append({
            "name": name,
            "address": address,
            "latitude" : lat,
            "longitude" : lng,
            "photo": photo,
            "website": website
        })

    return restaurants

def get_photo_url(api_key, photos):
    if not photos:
        return None
    photo_reference = photos[0].get("photo_reference")
    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
    return photo_url

def get_place_details(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": api_key,
        "fields": "website"
    }

    response = requests.get(url, params=params)
    result = response.json().get("result", {})
    return result

def dump_to_pandas(restaurants):
    df = pd.DataFrame(restaurants)
    return df

def dump_to_csv(df, file_name):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, file_name)
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved to {file_path}")
    return file_path


def dump_csv_to_sql(csv_file_path, db_name="skiresorts.db"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Add a new column for the auto-incremented restaurant_id
    df['skiresorts_id'] = range(1, len(df) + 1)
    
    # Create a new table with the auto-incremented restaurant_id
    df.to_sql('skiresorts_temp', conn, if_exists='replace', index=False)
    
    # Manually create the new table with restaurant_id as PRIMARY KEY AUTOINCREMENT
    conn.execute('''
        CREATE TABLE IF NOT EXISTS skiresorts (
            skiresorts_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    
    # Copy data from the temporary table to the new table
    conn.execute('''
        INSERT INTO skiresorts (name, address, latitude, longitude)
        SELECT name, address, latitude, longitude FROM skiresort_temp
    ''')
    
    # Drop the temporary table
    conn.execute('DROP TABLE skiresort_temp')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Data from {csv_file_path} dumped to database {db_name} with auto-incremented restaurant_id")




if __name__ == "__main__":
    load_dotenv()
# Coordinates for Breckenridge, Keystone, and Winter Park
    API_KEY = os.getenv('REACT_APP_PLACES_API_KEY')
    LOCATIONS = {
    "arapahoe basin": "39.6426,-105.8719",
    "aspen mountain": "39.1867,-106.8186",
    "beaver creek": "39.6042,-106.5165",
    "breckenridge": "39.4817,-106.0384",
    "copper mountain": "39.5022,-106.1500",
    "crested butte": "38.8998,-106.9650",
    "eldora mountain": "39.9372,-105.5829",
    "keystone": "39.6062,-105.9437",
    "loveland ski area": "39.6800,-105.8974",
    "monarch mountain": "38.5128,-106.3316",
    "powderhorn mountain resort": "39.0690,-108.1503",
    "purgatory resort": "37.6297,-107.8140",
    "silverton mountain": "37.8851,-107.6659",
    "steamboat": "40.4850,-106.8317",
    "telluride": "37.9375,-107.8123",
    "vail": "39.6403,-106.3742",
    "winter park": "39.8917,-105.7631",
    "wolf creek": "37.4720,-106.7934"
}
    
    output_csv = 'coloResorts.csv'
    all_resorts = []
    

    RADIUS = 100  # Radius in meters
    
    for location_name, location_coords in LOCATIONS.items():
        print(f"Searching for: {location_name}")
        resorts = get_restaurants(API_KEY, location_coords, RADIUS, location_name)
        all_resorts.extend(resorts) #add each result to a list 
    df = dump_to_pandas(all_resorts) # convert the accumulated list to a dataframe
    dump_to_csv(df, output_csv) #save to  the specified output csv file

