from flask import Flask, jsonify, request
import sqlite3
import pandas as pd
import bcrypt
from functools import wraps
import jwt
import utils as ut

app = Flask(__name__)
SECERT_KEY = "SE"


def get_db_connection(db):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error' : f"{error}: Resouce not found"}), 404


@app.errorhandler(500)
def not_found(error):
    return jsonify({'error' : f'{str(error)}: Internal server error'})


# Middleware to verify JWT

#create authenticte funtion with parameter f
def authenticate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Athentication")

        if not token:
            return jsonify({'message' : 'Token does not exist'})
        
        try:
            token = token.split(' ')[1]
            #decode header data
            data = jwt.decode(token, SECERT_KEY ,algorithm=['HS256'])
            #attach data to user request
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'Expired Signature'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message' : 'Invalid Token Error'}), 403
        return(*args, *kwargs)
    return decorated





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
    query = """ INSERT INTO resorts (name, location, rating, description)
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
@app.route('/api/user/<int:id>', methods=['GET'])
def get_user_by_id(id): 
    conn = get_db_connection('reviews.db')  # Create a connection to the database
    query = "SELECT FROM users WHERE users.id == ?"  # SQL query to get user by ID
    df = pd.read_sql_query(query, conn, params=(id,))  # Execute the query with the ID parameter
    conn.close()  # Close the database connection
    if df.empty:
        return jsonify({"error": "User not found"}), 404  # Return error if user not found
    else:
        return jsonify(df.to_dict(orient='records'))  # Return user data
    
@app.route('/api/users', methods=['POST'])
def add_users():
    data = request.get_json()
    conn = get_db_connection('users.db')
    query = ' INSERT INTO users (username, email, password) VALUES (?, ?, ?, ?)'
    conn.execute(query, (data['username'],
                         data['email'],
                         data['password']))
    
    conn.commit()
    conn.close()


#registar with authentication


@app.route('/api/users/<string:username>', methods=['GET'])
def get_by_username(username):
    conn = get_db_connection('users.db')
    query = 'SELECT * from users where users.username == ?'
    response = pd.read_sql_query(query, conn, params=(username))
    conn.close()

    if response.empty:
        return jsonify({"error": "Resort not found"}), 404
    else:
        return jsonify(response.to_dict(orient='records'))
    
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_users(id):
    conn = get_db_connection('users.db')
    query = "DELETE * FROM users WHERE users.id == ?"  # SQL query to get user by ID
    cursor = conn.cursor()
    cursor.execute(query, (id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': "user not deleted"})
    else:
        conn.close()
        return jsonify({'message': 'user deleted succesfully deleted'})

@app.route('/api/register', methods=['POST'])
def register_user():
    #get incoming data
    data = request.get_json()
    #connect to db
    conn = get_db_connection('users.db')


    #check if te data base if the user exist
    check_existing = 'select * from users WHERE username = ? or email = ?'
    user_condition = pd.read_sql_query(check_existing, conn, params=(data['email'], data['username']))
    username = data['username']
    if user_condition.empty:
        #hash the password
        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        #specify where data will be inserted
        query = "INSERT into users (username, email, password) VALUES (?, ?, ?)"
        conn.execute(query, (data['username'],
                            data['email'],
                            hashed))
        conn.commit()
        conn.close()
        return jsonify({'message' : 'username succefully added'})
    else:
        return jsonify({'message': f"{username} exist"})


@app.route('/api/login', methods=['GET'])
def login_user():

    login_data = request.get_json()

    conn = get_db_connection('users.db')
    
    username = login_data['username']
    login_password = login_data['password']

    query = 'SELECT password from users WHERE username == ?'
    stored_password = pd.read_sql_query(query, conn, params=(username,))


    if stored_password.empty:
        return jsonify({'message' : f"{login_data['username']} does not exist"})
    
    password = stored_password['password'].iloc[0]

 

    #check sql password with login password using brcpyt.checkpwd
    if bcrypt.checkpw(login_password.encode('utf-8'), password):
        token = jwt.encode({'username' : username}, SECERT_KEY, algorithm='HS256')
        message = get_data(username)
        conn.close()
        return jsonify({'message':'Sucessful login', 'token' : token, "user_data" : message}), 200
    else:
        conn.close()
        return jsonify({'message':'Incorrect login'}), 400


def get_data(username):
    
    conn = get_db_connection('users.db')
    query = 'SELECT * FROM users WHERE username == ?'
    user_data = pd.read_sql_query(query, conn, params=(username,))

    conn.close()
    
    if user_data.empty:
        return jsonify({'message' : 'user data does not exist'})
    else:
        data = ut.decode_password(user_data)
        return data



#Code to add login data
@app.route('/api/users/update', methods=['PUT'])
def update_users():
    login_data = request.get_json()
    password = login_data['password']
    email = login_data['email']
    username = login_data['username']
    new_email = login_data['new_email']
    new_username = login_data['new_username']

    query = 'SELECT * from users WHERE username = ?'
    conn = get_db_connection('users.db')
    stored_password = pd.read_sql_query(query, conn, params=(username,))

    if stored_password.empty:
        return jsonify({'message' : 'The username does not exist'})
    else:
        query = 'UPDATE users SET'
        params = {}
        if new_email:
            extend = ',email = ? where username = ?'
            query += extend
            params = {'email' : new_email, 'username' : username }
        if new_username:
            extend = ''
        
        new_query = query.replace(",", " ")
        print(new_query)
        conn.execute(new_query, tuple(params))
        conn.commit()
        conn.close()
        return jsonify({'message' : 'succefully update user'})




    

    
    







    





    



if __name__ == '__main__':
    app.run(debug=True)