from flask import Flask
from .db_model import DB


def create_app():
    '''
    Create and Configure an instance of our Flask Application
    '''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitoff.db'
    app.config
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to Twitoff!'

    @app.route('/<username>/<followers>')
    def add_user(username, followers):
        user = User(username=username, followers=followers)
        DB.sessions.add(user)
        DB.sessions.commit()

        return f'{username} has been added to the DB'

    return app
    #from twitoff.db_model import DB, User, Tweet