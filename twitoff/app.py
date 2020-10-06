from flask import Flask, render_template
from .db_model import DB, User, Tweet


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
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def add_or_update_user(name=None, message=''):
        name = name or request.values['user_name']

        try:
            if request.method == "POST":
                add_user_tweepy(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.username == name).one().tweets
        except Exception as e:
            print(f'Error adding {name}: {e}')
            tweets = []
        
        return render_template('user.html', title=name, tweets=tweets, message=message)

    return app 


    return app
    #from twitoff.db_model import DB, User, Tweet