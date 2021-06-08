from flask import Flask, request, Response, abort
from detect import Signatures
import requests
import logging
import yaml

app = Flask(__name__, static_folder=None)
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


class DefaultConfig:
    WAF_PORT = 80
    APP_URL = ''
    CHECK_OUTPUT = False
    LOGFILE = None


class Config(DefaultConfig):
    def __init__(self, cfg_path):
        with open(cfg_path, 'r') as f:
            self._config = yaml.safe_load(f)

    def __getattribute__(self, item):
        cfg = super().__getattribute__('_config')
        if item.lower() in cfg:
            return cfg[item.lower()]
        else:
            return super().__getattribute__(item)


def load_config(filename) -> Config:
    return Config(filename)


@app.route('/', methods=HTTP_METHODS, defaults={'path': ''})
@app.route('/<path:path>', methods=HTTP_METHODS)
def index(path):
    if signatures.detect(request):
        abort(403)
    resp = requests.request(
        method=request.method,
        url=f"{config.APP_URL}/{path}",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        params=request.values,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    if config.CHECK_OUTPUT:
        if signatures.detect_output(response):
            abort(403)
    return response


# @app.route('/static')
# def static():
#     resp = requests.get()


@app.errorhandler(403)
def forbidden(e):
    return 'Alarm, an attack was detected!', 403


if __name__ == '__main__':
    config = load_config('settings.yml')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-15s %(message)s',
                        filename=config.LOGFILE)
    signatures = Signatures()
    app.run(host="0.0.0.0", port=config.WAF_PORT, debug=True)
