import random, string, requests # noqa: E401
from flask import Response, request
from functools import wraps
import base64


allowed_tokens = [
    'GViuroCFjGJnrn0p6AproeuCDGgMDZMSQMV1SRM1yIQhG7JrnT',
]

def get_random_string(lenght:int=50):
    characters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    random_string = ''.join(random.choices(characters, k=lenght))
    return random_string

def get_random_cat_image():
    # No API key needed for basic random search
    resp = requests.get('https://api.thecatapi.com/v1/images/search')
    data = resp.json()
    return data[0]['url']

def check_auth(auth_header:str)->bool:
    try:
        schema, credentials = auth_header.split()
        if schema.lower() != 'bearer':
            return False
        decoded = base64.b64decode(credentials).decode('utf-8')
        return decoded in allowed_tokens
    except Exception:
        pass

def authenticate():
    return Response(
        'Authentication required',
        401,
        {"WWW-Authenticate": 'Bearer realm="API"'}
    )

def auth_protected(f):
    @wraps(f)
    async def decorated(*args, **kwargs): # Added async here
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return authenticate()
        try:
            schema, token = auth_header.split()
            if schema.lower() != 'bearer' or not check_auth(auth_header):
                return authenticate()
        except Exception:
            return authenticate()

        return await f(*args, **kwargs) # Added await here
    return decorated