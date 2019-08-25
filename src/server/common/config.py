import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseFlaskConfig(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SECRET_KEY = "86fa7b2084468af6fb330f8225d86fdea0e4298e96aaa25e818ff645aa0bee63"
  JWT_SECRET_KEY = "86fa7b2084468af6fb330f8225d86fdea0e4298e96aaa25e818ff645aa0bee63"

  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ustart_db")


class ProductionConfig(BaseFlaskConfig):
  DEBUG = False


class StagingConfig(BaseFlaskConfig):
  DEVELOPMENT = True
  DEBUG = True


class DevelopmentConfig(BaseFlaskConfig):
  DEVELOPMENT = True
  DEBUG = True


class TestingConfig(BaseFlaskConfig):
  TESTING = True
