from config import port, host, debug
from flask import Flask, render_template, jsonify
from utils import auth_protected, get_random_cat_image, get_random_string


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
async def get_cat_url():
    url = get_random_cat_image()
    return jsonify({'url': url})

@app.route('/api/v1/register')
async def register():
    token = get_random_string()
    return jsonify({'authorization': token})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)