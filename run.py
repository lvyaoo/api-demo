from os import getenv

from app import create_app


app = create_app(getenv('FLASK_CONFIG'))

if __name__ == '__main__':
    app.run()
