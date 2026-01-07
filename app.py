import requests
from config import port, host, debug
from flask import Flask, render_template, jsonify, request, Response
from functools import wraps
import base64

def get_random_cat_image():
    # No API key needed for basic random search
    resp = requests.get('https://api.thecatapi.com/v1/images/search')
    data = resp.json()
    return data[0]['url']

USERNAME = 'meow'
PASSWORD = 'meow67'

def check_auth(auth_header:str)->bool:
    try:
        schema, credentials = auth_header.split()
        if schema.lower() != 'basic':
            return False
        decoded = base64.b64decode(credentials).decode('utf-8')
        username, password = decoded.split(":", 1)
        return username==USERNAME and password==PASSWORD
    except Exception:
        pass

def authenticate():
    return Response(
        'Authentication required',
        401,
        {"WWW-Authenticate": 'Basic realm="API"'}
    )


def auth_protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not check_auth(auth_header):
            return authenticate()
        return f(*args, **kwargs)
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
def get_cat_url():
    url = get_random_cat_image()
    data = {
        'url':url
    }
    return jsonify(data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)