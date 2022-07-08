from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO


UPLOAD_FOLDER = 'static/uploads/'

db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app():

    app = Flask(__name__)
    CORS(app, resources=r'/*')
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = 'your uri',
        SECRET_KEY = 'your key',
        UPLOAD_FOLDER = 'static/uploads/',
        #旧的sqlite数据库
        # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    )

    @app.route('/home/test')
    def test():
        return render_template('talk.html')

    socketio = SocketIO(app, cors_allowed_origins = '*')

    

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskBlog.users.routes import users
    from flaskBlog.posts.routes import posts
    from flaskBlog.main.routes import main
    from flaskBlog.errors.routes import errors
    from flaskBlog.api.resources import api_bp
    # from flaskBlog.socketio.routes import talk


    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(api_bp)
    # app.register_blueprint(talk)

    from flaskBlog.talk import MyCustom
    socketio.on_namespace(MyCustom('/test'))
    return app


# app = Flask(__name__)

# app.config['SECRET_KEY'] = 'a5w0aer0rta53e0arf0a'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'

# from flaskBlog.users.routes import users
# from flaskBlog.posts.routes import posts
# from flaskBlog.main.routes import main

# app.register_blueprint(users)
# app.register_blueprint(posts)
# app.register_blueprint(main)
