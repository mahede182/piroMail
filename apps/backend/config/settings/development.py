from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])
if 'piromail-backend.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('piromail-backend.onrender.com')

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://piromail-backend.onrender.com',
    'https://piromail-frontend.onrender.com',
]
