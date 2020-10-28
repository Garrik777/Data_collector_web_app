class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123@localhost/height_collector'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './uploaded'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
