from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])
# Fallback hardcoded host just in case
if 'piromail-backend.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('piromail-backend.onrender.com')
# Production specific security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Optionally configure logging for production
CSRF_TRUSTED_ORIGINS = [
    'https://piromail-backend.onrender.com',
    'https://piromail-frontend.onrender.com',
]
