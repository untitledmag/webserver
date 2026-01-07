import random, string, base64, requests  # noqa: E401
from config import port, host, debug
from flask import Flask, render_template, jsonify, request, Response
from functools import wraps
from database import functions as db

def get_random_string(lenght:int=50):
    characters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    random_string = ''.join(random.choices(characters, k=lenght))
    return random_string

def get_random_cat_image():
    # No API key needed for basic random search
    resp = requests.get('https://api.thecatapi.com/v1/images/search')
    data = resp.json()
    return data[0]['url']

async def check_auth(auth_header:str)->bool:
    try:
        schema, credentials = auth_header.split()
        if schema.lower() != 'bearer':
            return False
        decoded = base64.b64decode(credentials).decode('utf-8')
        return await db.is_auth_in_db(decoded)
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
        
        # In your previous code, you were base64 decoding. 
        # Since you generate tokens with get_random_string(), 
        # you should just check the string directly.
        if not auth_header:
            return authenticate()
            
        try:
            schema, token = auth_header.split()
            if schema.lower() != 'bearer' or not await db.is_auth_in_db(token):
                return authenticate()
        except Exception:
            return authenticate()

        return await f(*args, **kwargs) # Added await here
    return decorated


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('page.html')

@app.route('/minecraft')
def minecraft():
    return render_template('minecraft.html')

@app.route('/cs')
def counterstrike():
    return render_template('cs2.html')

@app.route('/cat')
def showcat():
    return render_template('catimg.html')


@app.route('/api/v1/developer')
def get_developer():
    data = {
        'Name':'Manreet Singh',
        'Course':'ICS3U1',
        'Project':'Flask Webserver',
        'Date Started':'Jan 5, 2026',
        'Aim':'To create a full working flask server with webpages and API support'
    }
    return jsonify(data)

@app.route('/api/v1/get-cat')
@auth_protected
async def get_cat_url(): # Changed to async
    url = get_random_cat_image()
    return jsonify({'url': url})

@app.route('/api/v1/register')
async def register(): # Changed to async
    token = get_random_string()
    await db.store_auth_token(token) # Now this works!
    return jsonify({'authorization': token})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)