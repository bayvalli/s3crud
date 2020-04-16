import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)

class Config(object):

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'super-secret-random-key-here'
    DYNAMODB_TABLENAME = 'metadata'
    S3_BUCKET_NAME = 'blghomework1'
    S3_BUCKET_URL = 'http://{}.s3.amazonaws.com'.format(S3_BUCKET_NAME) 
    UPLOAD_FOLDER = 'data/'
    THUMBNAIL_FOLDER = 'data/thumbnail/'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx', 'pdf', 'mp4'])
    IGNORED_FILES = set(['.gitignore'])

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
