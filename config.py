# configuration

class Config(object):
	DATABASE = 'data/infohash.db'
	DEBUG = True
	SECRET_KEY = 'development key'
	USERNAME = 'admin'
	PASSWORD = 'default'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/hashdb?charset=utf8'
	#SQLALCHEMY_DATABASE_URI = 'sqlite:///data/infohash.db'
	SQLALCHEMY_ECHO = True

	# Create dummy secrey key so we can use sessions
	SECRET_KEY = '123456790'

	# Flask-Security config
	SECURITY_URL_PREFIX = "/admin"
	SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
	SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

	# Flask-Security URLs, overridden because they don't put a / at the end
	SECURITY_LOGIN_URL = "/login/"
	SECURITY_LOGOUT_URL = "/logout/"
	SECURITY_REGISTER_URL = "/register/"

	SECURITY_POST_LOGIN_VIEW = "/admin/"
	SECURITY_POST_LOGOUT_VIEW = "/admin/"
	SECURITY_POST_REGISTER_VIEW = "/admin/"

	# Flask-Security features
	SECURITY_REGISTERABLE = True
	SECURITY_SEND_REGISTER_EMAIL = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
