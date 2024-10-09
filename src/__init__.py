from flask import Flask
from flask_restful import Api

def create_app():
    app = Flask(__name__)

    #app.config.from_envvar('FLASK_CONFIG')

    api = Api(app)

    return app