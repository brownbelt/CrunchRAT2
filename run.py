from gevent.wsgi import WSGIServer
from app import app

if __name__ == "__main__":
    # starts Flask server
    server = WSGIServer(("0.0.0.0", 80), app)
    server.serve_forever()
