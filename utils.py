
#utility functions to help with backend
def decode_password(data):
    data = data.to_dict(orient='records')[0]

    if isinstance(data['password'], bytes):
        data['password'] = data['password'].decode('utf-8')
    
    return data