from recommendation_server.app import create_app
from recommendation_server.app.config import HOST, PORT

app = create_app()

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)