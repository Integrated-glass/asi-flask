# Creating the app
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Config app
from server.common.config import ProductionConfig as ConfigObject

app.config.from_object(ConfigObject)

# DB part
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Registring blueprints (modules)
from server.controllers.auth import auth

app.register_blueprint(auth)

# from flask_migrate import Migrate, init as db_init, migrate as db_migrate, upgrade as db_upgrade

# migrate = Migrate(app, db)

# import server.models

# Migrate
# import os.path
# with app.app_context():
#   migrationsDir = "migrations"
#   if not os.path.exists(migrationsDir):
#     db_init(directory=migrationsDir)
#   db_migrate(directory=migrationsDir)
#   db_upgrade(directory=migrationsDir)
