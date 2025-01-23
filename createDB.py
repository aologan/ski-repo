import pandas as pd
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

def init_db(db_name):
    conn = sqlite3.connect(f'{db_name}.db')
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
            resort_id INTEGER PRIMARY KEY AUTOINCREMENT,
            resortname TEXT NOT NULL,
            reviewscore NOT NULL,
             TEXT NOT NULL,
            created_at TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

def init_ski_review_database(db_name):
    conn = sqlite3.connet(f'{db_name}.db')
    c = conn.cunsor()
    c.execute('''
            CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resort_id INTEGER,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    job_title TEXT,
    hourly_pay REAL,
    tip_amount REAL,
    housing_provided BOOLEAN,
    housing_rating INTEGER CHECK(housing_rating >= 1 and housing_rating <= 5 )
    FOREIGN KEY (resort_id) REFERENCES resorts(id))
              ''')


def init_review_db(db_name):
    conn = sqlite3.connect(f'{db_name}.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT exists reviews  (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        restaurant_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        tip REAL,
        average_pay REAL,
        review_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id))
    ''')
    conn.commit()
    conn.close()


def get_restaurants():
    conn = sqlite3.connect('restaurants.db')
    query = "SELECT name, address, latitude, longitude FROM restaurants"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return jsonify(df.to_dict(orient='records'))

def get_restaurants_by_id(id):
    conn = sqlite3.connect('restaurants.db')
    query = "Select name, address, latitude, logitude where restaurants.name == ?"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return jsonify(df)
    

def get_users():
    conn= sqlite3.connect('users.db')
    query = "INSERT name, email, password FROM users"


def delet_from_users():

    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Delete all entries from the users table
    cursor.execute("DELETE FROM users")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    #init_db('users')
    #init_db('skiresorts_temp')
    init_ski_review_database('reviews')
    #app.run(debug=True)