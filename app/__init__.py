from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#init my Database manager
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):

    # Init the app
    app = Flask(__name__)
    #Link in the Config
    app.config.from_object(config_class)

    #Register Plug-in

    db.init_app(app)
    migrate.init_app(app, db)
    
    
    #Configure Some Settings
    

   

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app