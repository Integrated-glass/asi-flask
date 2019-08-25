# Creating the app
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Config app
from server.common.config import ProductionConfig as ConfigObject  # noqa

app.config.from_object(ConfigObject)

# DB part
from flask_sqlalchemy import SQLAlchemy  # noqa

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Registring blueprints (modules)
from server.controllers.auth import auth  # noqa
app.register_blueprint(auth)

from server.controllers.startup import startup  # noqa
app.register_blueprint(startup)

from server.controllers.tags import tag  # noqa
app.register_blueprint(tag)

from server.controllers.investor import investorMod  # noqa
app.register_blueprint(investorMod)

from server.controllers.investment import investment  # noqa
app.register_blueprint(investment)

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
