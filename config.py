import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BLACKFYNN_API_TOKEN = os.environ.get('BLACKFYNN_API_TOKEN', 'local-api-key')
    BLACKFYNN_API_SECRET = os.environ.get('BLACKFYNN_API_SECRET', 'local-secret-key')
    BLACKFYNN_API_HOST = os.environ.get("BLACKFYNN_API_HOST")
    BLACKFYNN_CONCEPTS_API_HOST = os.environ.get("BLACKFYNN_CONCEPTS_API_HOST")
    BLACKFYNN_EMBARGO_TEAM_ID = os.environ.get("BLACKFYNN_EMBARGO_TEAM_ID")
    GRAPHENEDB_BOLT_URL=os.environ.get("GRAPHENEDB_BOLT_URL")
    GRAPHENEDB_BOLT_USER=os.environ.get("GRAPHENEDB_BOLT_USER")
    GRAPHENEDB_BOLT_PASSWORD=os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
    MONGODB_URI=os.environ.get("MONGODB_URI")