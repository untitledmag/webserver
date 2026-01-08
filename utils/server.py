import random, string, requests # noqa: E401
from flask import Response, request
from functools import wraps
import base64
import logging
import httpx

logging = logging.getLogger(__name__)

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


async def get_ip_info(ip: str):
    url = f'http://ip-api.com/json/{ip}'
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            # Check if the external API itself is down
            if resp.status_code != 200:
                return {"error": f"External API returned {resp.status_code}"}, 502
            
            data = resp.json()

        if data.get('status') == 'fail':
            logging.error(f"IP-API Error: {data.get('message')}")
            return {'error': data.get('message'), 'code': 400}

        fields = ["query", "country", "countryCode", "region", "regionName", 
                  "city", "zip", "lat", "lon", "timezone", "isp", "org", "as"]

        rdata = {field: data.get(field, 'Unknown') for field in fields}
        return rdata

    except Exception as e:
        logging.error(f"Connection error: {e}")
        return {"error": "Internal connection failed"}