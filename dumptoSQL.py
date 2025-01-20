import sqlite3
import pandas as pd

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('ski_resorts.db')  # Create a new database
    cursor = conn.cursor()
    
    # Create a table for ski resorts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resorts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            latitude REAL,
            longitude REAL,
            address TEXT,
            photo TEXT,
            website TEXT, 
            rating REAL
        )
    ''')
    conn.commit()
    conn.close()

# Dump CSV contents into the database
def dump_csv_to_db(df):
    conn = sqlite3.connect('ski_resorts.db')
    df.to_sql('resorts', conn, if_exists='append', index=False)
    conn.close()


#edit csv file to be dumped into sql database
def edit_csv(csv_file):
    df = pd.read_csv(csv_file)
    #df['location'] = list(zip(df['latitude'], df['longitude']))  # Create a tuple of (lat, lon)
    #df.drop(columns=['latitude', 'longitude'], inplace=True)  # Remove the original columns if
    return df
# Main execution
if __name__ == "__main__":
    initialize_database()
    df = edit_csv('coloResorts.csv')
    dump_csv_to_db(df)
