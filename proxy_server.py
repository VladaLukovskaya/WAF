from flask import Flask, request, Response
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
import requests
import os

app = Flask(__name__)
bootstrap = Bootstrap(app=app)
csrf = CSRFProtect(app=app)

# where is the data come from
SITE_NAME = 'http://localhost:5000/'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE'])
def proxy(path):
    global SITE_NAME
    if request.method == 'GET':
        resp = requests.get(f'{SITE_NAME}{path}')
        # print(resp.text)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method == 'POST':
        resp = requests.post(f'{SITE_NAME}{path}', json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method == 'DELETE':
        resp = requests.delete(f'{SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response


if __name__ == '__main__':
    app.run(debug=True, port=8080)
