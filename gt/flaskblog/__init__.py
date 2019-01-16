from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
#from flask_migrate import Migrate

# import logging
# from logging.handlers import RotatingFileHandler
from logging.config import dictConfig
from flask_apscheduler import APScheduler



db = SQLAlchemy()


bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()




dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/tuozhanrms'

    #app.config['WTF_I18N_ENABLED'] = False 
    app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

    app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'static/uploads')
    # app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.root_path, 'static/upload_path/photos')
    # photos = UploadSet('photos', IMAGES)
    # configure_uploads(app, photos)
    # patch_request_class(app)  # set maximum file size, default is 16MB

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.sms.routes import sms
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(sms)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

#migrate = Migrate(app, db)
