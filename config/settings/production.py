import os
from .base import *

# Ensure DEBUG is turned off for production
DEBUG = False

# Do not commit your secret key to the repository
# Load from environment variables or a local file
SECRET_KEY = os.environ['SECRET_KEY']

# Uncomment below to load secret key from a file
# with open('/etc/secret_key.txt') as f:
#     SECRET_KEY = f.read().strip()

# You should change the static root directory depending
# on your configuration

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Set cookies to only transfer over https

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True


# Add your production settings here
