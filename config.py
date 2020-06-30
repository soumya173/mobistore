import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = '421B4BB2CE6F1C97F7167BC987D31'

# Connect to the database
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/mobistore'

SQLALCHEMY_TRACK_MODIFICATIONS = True