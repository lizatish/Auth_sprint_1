from gevent import monkey

monkey.patch_all()
from main import app
from gevent.pywsgi import WSGIServer

http_server = WSGIServer(('', 4555), app)
http_server.serve_forever()
