# Creating the app
from flask import Flask
app = Flask(__name__)

# Config app
from server.common.confing import ProductionConfig as ConfigObject
app.config.from_object(ConfigObject)

# Registring blueprints (modules)
from server.controllers.test import testMod
app.register_blueprint(testMod)

# DB part
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_migrate import Migrate, init as db_init, migrate as db_migrate, upgrade as db_upgrade
migrate = Migrate(app, db)

import server.models

# Migrate
# import os.path
# with app.app_context():
#   migrationsDir = "migrations"
#   if not os.path.exists(migrationsDir):
#     db_init(directory=migrationsDir)
#   db_migrate(directory=migrationsDir)
#   db_upgrade(directory=migrationsDir)
