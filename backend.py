from flask import Flask, jsonify, request
import sqlite3
import pandas as pd


app = Flask(__name__)


def get_db_connection(db):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/resorts', methods=['GET'])
def get_resorts():
    '''
    Get all ski resorts and their associated data from ski-resorts.db
    '''
    conn = get_db_connection('ski_resorts.db')
    query = "SELECT * from resorts"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/resorts/<int:id>', methods=['GET']) #establish id parameter
def get_resorts_by_id(id): #accept the id parameter
    conn = get_db_connection('ski_resorts.db') #create the connection to the id parameter
    query = "SELECT * FROM resorts WHERE resorts.id == ?"
    df = pd.read_sql_query(query, conn, params=(id,))
    conn.close()
    if df.empty:
        return jsonify({"error": "Resort not found"}), 404
    else:
        return jsonify(df.to_dict(orient='records'))


@app.route('/api/resorts/name/<string:name>', methods=['GET']) #establish the parameter
def get_resort_by_name(name): #save name as parameter
    conn = get_db_connection('ski_resorts.db')
    query = "SELECT * FROM resorts WHERE resorts.name == ?"
    df = pd.read_sql_query(query, conn, params=(name,)) #place name as parameter
    conn.close()
    if df.empty:
        return jsonify({"error": "Resort not found"}), 404
    else:
        return jsonify(df.to_dict(orient='records'))


@app.route('/api/resorts/<int:id>', methods=['DELETE'])
def delete_by_id(id):
    conn = get_db_connection('ski_resorts.db')
    query = 'DELETE FROM resorts where resorts.id == ?'
    cursor = conn.cursor()
    cursor.execute(query, (id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': "Resorts"})
    else:
        conn.close()
        return jsonify({'message': 'resort succesfully deleted'})
    

@app.route('/api/resorts', methods=['POST'])
def add_resort():
    resort_data = request.get_json()  # Get the resort data from the request
    conn = get_db_connection('ski_resorts.db')
    
    # SQL query to insert a new resort
    query = """
    INSERT INTO resorts (name, location, rating, description)
    VALUES (?, ?, ?, ?)
    """
    
    # Execute the query with the provided data
    conn.execute(query, (
        resort_data['name'],        # Resort name
        resort_data['location'],    # Resort location
        resort_data['rating'],      # Resort rating
        resort_data.get('description', '')  # Optional description
    ))
    
    conn.commit()  # Commit the transaction
    conn.close()   # Close the connection
    
    return jsonify({"message": "Resort added successfully"}), 201  # Return success message



#All CRUD FUNCTIONALITY FOR USERS
@app.route('/api/routes/user/<int:id>', methods=['GET'])
def get_user_by_id(id): 
    conn = get_db_connection('reviews.db')  # Create a connection to the database
    query = "SELECT FROM users WHERE users.id == ?"  # SQL query to get user by ID
    df = pd.read_sql_query(query, conn, params=(id,))  # Execute the query with the ID parameter
    conn.close()  # Close the database connection
    if df.empty:
        return jsonify({"error": "User not found"}), 404  # Return error if user not found
    else:
        return jsonify(df.to_dict(orient='records'))  # Return user data
    
@app.route('/api/routes/users', methods=['POST'])
def add_users():
    data = request.get_json()
    conn = get_db_connection('users.db')
    query = ' INSERT INTO users (username, email, password) VALUES (?, ?, ?, ?)'
    conn.execute(query, (data['username'],
                         data['email'],
                         data['password']))
    
    conn.commit()
    conn.close()


@app.route('api/routes/users/<string:username>', methods=['GET'])
def get_by_username(username):
    conn = get_db_connection('users.db')
    query = 'SELECT * from users where users.username == ?'
    response = pd.read_sql_query(query, conn, params=(username))
    conn.close()

    if response.empty:
        return jsonify({"error": "Resort not found"}), 404
    else:
        return jsonify(response.to_dict(orient='records'))
    
app.route('api/route/users/<int:id>', methods=['DELETE'])
def delete_users(id):
    conn = get_db_connection('users.db')
    query = "DELETE * FROM users WHERE users.id == ?"  # SQL query to get user by ID
    query = 'DELETE FROM resorts where resorts.id == ?'
    cursor = conn.cursor()
    cursor.execute(query, (id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': "user not deleted"})
    else:
        conn.close()
        return jsonify({'message': 'user deleted succesfully deleted'})
    





    



if __name__ == '__main__':
    app.run(debug=True)